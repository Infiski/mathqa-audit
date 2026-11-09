"""Calculators that run MathQA solution programs on a question's numbers.

The two versions of the dataset write programs differently, so there are two interpreters.

Filtered:  [["b", "100.0", "+"], ["a", "100.0", "-_rev"], ["m_1", "100.0", "*"], ...]
Full:      add(n1,const_100)|subtract(const_100,n0)|multiply(#0,const_100)|...

Both return None when a program cannot be run, and the question then counts as wrong.
"""
import math
import re


# ---------------------------------------- filtered data ----------------------------------------
def run_filtered_program(steps, numbers):
    results = []

    def value(token):
        if token.startswith("m_"):               # result of an earlier step: m_1, m_2, ...
            return results[int(token[2:]) - 1]
        if len(token) == 1 and token.isalpha():  # a number from the question: a, b, c, ...
            return numbers[ord(token) - ord("a")]
        return float(token)                      # a constant such as 100.0

    for left, right, op in steps:
        a, b = value(left), value(right)
        if op.endswith("_rev"):                  # "_rev" means swap the two inputs
            a, b = b, a
            op = op[:-4]
        if op == "+":
            results.append(a + b)
        elif op == "-":
            results.append(a - b)
        elif op == "*":
            results.append(a * b)
        elif op == "/":
            results.append(a / b)
        elif op == "^":
            results.append(a ** b)
    return results[-1]


def safe_run_filtered(steps, numbers):
    try:
        return run_filtered_program(steps, numbers)
    except (IndexError, ZeroDivisionError, OverflowError):
        return None


# ------------------------------------------ full data ------------------------------------------
PI = math.pi


def combination(n, k):
    return float(math.comb(int(n), int(k)))


def permutation(n, k):
    return float(math.perm(int(n), int(k)))


# MathQA lists operation names but no formulas, so these are written from the names.
# Misspellings such as "circumface" and "reminder" are how the dataset spells them.
# "log" is base 2 because that matched the training data best, on weak evidence.
# "sine" and "tangent" are left out: each appears once in training and no formula helped.
OPERATIONS = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide": lambda a, b: a / b,
    "power": lambda a, b: a ** b,
    "sqrt": lambda a: math.sqrt(a),
    "log": lambda a: math.log2(a),
    "factorial": lambda a: float(math.factorial(int(a))),
    "gcd": lambda a, b: float(math.gcd(int(a), int(b))),
    "lcm": lambda a, b: float(math.lcm(int(a), int(b))),
    "max": lambda a, b: max(a, b),
    "min": lambda a, b: min(a, b),
    "reminder": lambda a, b: a % b,
    "negate": lambda a: -a,
    "inverse": lambda a: 1 / a,
    "round": lambda a: float(round(a)),
    "floor": lambda a: float(math.floor(a)),
    "choose": combination,
    "combination": combination,
    "permutation": permutation,
    "circle_area": lambda r: PI * r * r,
    "circumface": lambda r: 2 * PI * r,
    "circle_arc": lambda r, deg: 2 * PI * r * deg / 360,
    "semi_circle_perimiter": lambda r: PI * r + 2 * r,
    "circle_sector_area": lambda r, deg: PI * r * r * deg / 360,
    "rectangle_perimeter": lambda a, b: 2 * (a + b),
    "rectangle_area": lambda a, b: a * b,
    "square_perimeter": lambda a: 4 * a,
    "square_area": lambda a: a * a,
    "trapezium_area": lambda a, b, h: (a + b) * h / 2,
    "rhombus_perimeter": lambda a: 4 * a,
    "rhombus_area": lambda a, b: a * b / 2,
    "quadrilateral_area": lambda d, a, b: d * (a + b) / 2,
    "volume_cone": lambda r, h: PI * r * r * h / 3,
    "volume_rectangular_prism": lambda a, b, c: a * b * c,
    "volume_cube": lambda a: a ** 3,
    "volume_sphere": lambda r: 4 / 3 * PI * r ** 3,
    "volume_cylinder": lambda r, h: PI * r * r * h,
    "surface_cylinder": lambda r, h: 2 * PI * r * (r + h),
    "surface_cube": lambda a: 6 * a * a,
    "surface_rectangular_prism": lambda a, b, c: 2 * (a * b + b * c + a * c),
    "surface_sphere": lambda r: 4 * PI * r * r,
    "cube_edge_by_volume": lambda v: v ** (1 / 3),
    "diagonal": lambda a, b: a * b / 2,
    "square_edge_by_perimeter": lambda p: p / 4,
    "square_edge_by_area": lambda a: math.sqrt(a),
    "triangle_perimeter": lambda a, b, c: a + b + c,
    "triangle_area": lambda b, h: b * h / 2,
    "triangle_area_three_edges": lambda a, b, c: math.sqrt(
        max(0, ((a + b + c) / 2) * ((b + c - a) / 2) * ((a + c - b) / 2) * ((a + b - c) / 2))
    ),
    "negate_prob": lambda p: 1 - p,
    "percent": lambda a: a / 100,
    "p_after_gain": lambda g, p: (1 + g / 100) * p,
    "speed": lambda d, t: d / t,
    "stream_speed": lambda a, b: (a + b) / 2,
    "original_price_before_gain": lambda g, p: p / (1 + g / 100),
    "original_price_before_loss": lambda l, p: p / (1 - l / 100),
    "speed_in_still_water": lambda a, b: (a + b) / 2,
    "cosine": lambda a: math.cos(a),
}

CONSTANTS = {"pi": PI, "deg_to_rad": PI / 180}


def _value_of(token, numbers, results):
    token = token.strip()
    if token.startswith("n") and token[1:].isdigit():  # a number from the question: n0, n1, ...
        return numbers[int(token[1:])]
    if token.startswith("#"):                          # result of an earlier step: #0, #1, ...
        return results[int(token[1:])]
    if token.startswith("const_"):                     # const_100, const_0_25, const_m1, const_pi
        name = token[6:]
        if name in CONSTANTS:
            return CONSTANTS[name]
        return float(name.replace("m", "-").replace("_", "."))
    return float(token)


def run_full_program(formula, numbers):
    results = []
    try:
        for step in formula.strip().strip("|").split("|"):
            name, args = re.match(r"(\w+)\((.*)\)", step.strip()).groups()
            values = [_value_of(a, numbers, results) for a in args.split(",")]
            results.append(float(OPERATIONS[name](*values)))
    except Exception:  # unknown operation, bad number position, divide by zero, ...
        return None
    return results[-1] if results else None
