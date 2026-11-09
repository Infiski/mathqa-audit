"""What differs between the two versions of MathQA: templates, programs and answer checking."""
import json
import math
import re

from .interpreter import run_full_program, safe_run_filtered

NUMBER = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?|\.\d+")


def clean_text(record):
    return " ".join(record["Problem"].lower().split())


class FilteredDataset:
    """Answers are correct if they are within 0.0001 of the value of the question's own program."""

    @staticmethod
    def template(record):
        text = re.sub(r"temp_[a-z]+", "<num>", record["text"].lower())
        return " ".join(text.split())

    @staticmethod
    def number_count(record):
        return len(record["num_list"])

    @staticmethod
    def program_key(record):
        return json.dumps(record["equation_layer"])

    @staticmethod
    def run(program_key, record):
        return safe_run_filtered(json.loads(program_key), record["num_list"])

    @staticmethod
    def gold_value(record):
        return safe_run_filtered(record["equation_layer"], record["num_list"])

    @classmethod
    def is_right(cls, value, record):
        gold = cls.gold_value(record)
        for v in (value, gold):
            if v is None or isinstance(v, complex) or math.isnan(v):
                return False
        return abs(value - gold) < 1e-4


class FullDataset:
    """Answers are multiple choice: the computed value selects the closest option."""

    @staticmethod
    def template(record):
        text = NUMBER.sub("<num>", record["Problem"].lower())
        return " ".join(text.split())

    @staticmethod
    def numbers(record):
        return [float(x.replace(",", "")) for x in NUMBER.findall(record["Problem"])]

    @classmethod
    def number_count(cls, record):
        return len(cls.numbers(record))

    @staticmethod
    def program_key(record):
        return record["linear_formula"]

    @classmethod
    def run(cls, program_key, record):
        return run_full_program(program_key, cls.numbers(record))

    @classmethod
    def reference_value(cls, record):
        return run_full_program(record["linear_formula"], cls.numbers(record))

    @staticmethod
    def option_values(record):
        values = {}
        for letter, text in re.findall(r"([a-e]) \) (.*?)(?= , [a-e] \) |$)", record["options"]):
            clean = text.replace(",", "")
            fraction = re.search(r"(\d+(?:\.\d+)?) ?/ ?(\d+(?:\.\d+)?)", clean)
            number = re.search(r"-?\d+(?:\.\d+)?|-?\.\d+", clean)
            if fraction and float(fraction.group(2)) != 0:
                values[letter] = float(fraction.group(1)) / float(fraction.group(2))
            elif number:
                values[letter] = float(number.group())
        return values

    @classmethod
    def choose_option(cls, value, record):
        options = cls.option_values(record)
        if value is None or not options or isinstance(value, complex) or math.isnan(value) or math.isinf(value):
            return None
        return min(options, key=lambda letter: abs(options[letter] - value))

    @classmethod
    def is_right(cls, value, record, tolerance=None):
        """With a tolerance (0.01 = 1%), the value must also be that close to the chosen option."""
        letter = cls.choose_option(value, record)
        if letter is None or letter != record["correct"]:
            return False
        if tolerance is None:
            return True
        target = cls.option_values(record)[letter]
        return abs(value - target) <= tolerance * max(abs(target), 1e-9)
