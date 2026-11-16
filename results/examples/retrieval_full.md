# Retrieved training questions (full split, test set)

## New wording (Rule 2)

Bands are by TF-IDF similarity to the picked training question.

### TF-IDF similarity 0.00 to 0.50 (244 new test questions)

**Test question 1147**: paul sells encyclopedias door - to - door . he earns $ 150 on every paycheck , regardless of how many sets he sells . in addition , he earns commission as follows : commission sales 10 % $ 0.00 - $ 10 , 000.00 5 % $ 10 , 000.01 - - - > he does not earn double commission . that is , if his sales are $ 12,000 , he earns 10 % on the first $ 10,000 and 5 % on the remaining $ 2,000 . his largest paycheck of the year was $ 1,320 . what were his sales for that pay period ?
- correct option a (a ) 13,400 , b ) 14,800 , c ) 16,400 , d ) 15,800 , e ) 19,600)
- **TF-IDF**: no training question with the same count of numbers in the top 50 -> **wrong**
- **BERT (all-MiniLM-L6-v2)**: no training question with the same count of numbers in the top 50 -> **wrong**

**Test question 2284**: a certain scholarship committee awarded scholarships in the amounts of $ 1250 , $ 2500 and $ 4000 . the committee awarded twice as many $ 2500 scholarships as $ 4000 and it awarded 3 times as many $ 1250 scholarships as $ 2500 scholarships . if the total of $ 75000 was awarded in $ 1250 scholarships , how many $ 4000 scholarships were awarded ?
- correct option d (a ) 5 , b ) 6 , c ) 9 , d ) 10 , e ) 15)
- **TF-IDF**: no training question with the same count of numbers in the top 50 -> **wrong**
- **BERT (all-MiniLM-L6-v2)**: no training question with the same count of numbers in the top 50 -> **wrong**

**Test question 2632**: if a train runs at 40 kmph , it reach its destination late by 11 minutes but if it runs at 50 kmph it is late by 5 minutes only . the correct time for a train to complete its journey is ? let the correct time to complete the journey be x min distance covered in ( x + 11 ) min . at 40 kmph distance covered in ( x + 5 ) min . at 50 kmph ( x + 11 ) / 60 * 40 = ( x + 5 ) / 60 * 50 x = 19 min
- correct option a (a ) 19 min , b ) 19 hrs , c ) 52 min , d ) 126 min , e ) 52 min)
- **TF-IDF**: no training question with the same count of numbers in the top 50 -> **wrong**
- **BERT (all-MiniLM-L6-v2)**: no training question with the same count of numbers in the top 50 -> **wrong**

### TF-IDF similarity 0.50 to 0.70 (53 new test questions)

**Test question 227**: if twice of a number divided by 3 d gives 20 as the remainder , and 5 times of the same number gives 32 as the remainder . what will be the value of d ?
- correct option b (a ) 11 , b ) 12 , c ) 15 , d ) 14 , e ) 18)
- **TF-IDF** (similarity 0.532): a number when divided by 45 , gives 30 as quotient and 0 as remainder . what will be the remainder when dividing the same number by 15
  - its program: `multiply(n0,n1)|divide(#0,n3)`
  - run on the test numbers: 1.875, closest option a -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.740): what is the remainder when 14452 × 15652 × 16781 is divided by 5 ?
  - its program: `multiply(n0,n1)|multiply(n2,#0)|reminder(#1,n3)`
  - run on the test numbers: 12, closest option b -> **right**

**Test question 952**: 6 people can do work in 80 days how much people they required to complete the work in 16 days ?
- correct option c (a ) 10 , b ) 20 , c ) 30 , d ) 40 , e ) 50)
- **TF-IDF** (similarity 0.564): a can do a work in 7 days b in 12 days and c in 5 days . if they work on it together then in how many days required to complete the work ?
  - its program: `add(n0,n1)|multiply(n0,n1)|add(n2,#0)|multiply(n2,#1)|multiply(n0,#2)|divide(#3,#4)|`
  - run on the test numbers: 12.549, closest option a -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.837): 10 men do a work in 10 days . how many men are needed to finish the work in 2 days ?
  - its program: `multiply(n0,n1)|divide(#0,n2)|`
  - run on the test numbers: 30, closest option c -> **right**

**Test question 1678**: a and b together do a work in 20 days . b and c together in 15 days and c and a in 12 days . so a , b and c together finish same work in how many days ?
- correct option d (a ) 12 , b ) 15 , c ) 8 , d ) 10 , e ) 11)
- **TF-IDF** (similarity 0.616): a and b can do a work in 8 days , b and c can do the same work in 12 days . a , b and c together can finish it in 6 days . a and c together will do it in how many days ?
  - its program: `divide(n0,const_2)|add(#0,const_2)|multiply(n0,#1)|divide(#2,n2)|`
  - run on the test numbers: 20, closest option b -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.963): a and b can do a work in 8 days , b and c can do the same work in 12 days . a , b and c together can finish it in 6 days . a and c together will do it in how many days ?
  - its program: `divide(n0,const_2)|add(#0,const_2)|multiply(n0,#1)|divide(#2,n2)|`
  - run on the test numbers: 20, closest option b -> **wrong**

### TF-IDF similarity 0.70 to 0.85 (76 new test questions)

**Test question 2036**: the product of two numbers is 192 and the sum of these two numbers is 28 . what is the smaller of these two numbers ?
- correct option b (a ) 10 , b ) 12 , c ) 14 , d ) 15 , e ) 16)
- **TF-IDF** (similarity 0.839): the product of two numbers is 168 and the sum of these two numbers is 26 . what is the largest of these two numbers ?
  - its program: `multiply(n0,const_4)|multiply(n0,const_2)|subtract(n1,#1)|sqrt(#2)|power(#3,const_2)|add(#0,#4)|sqrt(#5)|`
  - run on the test numbers: no value -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.902): sum of two numbers is 25 and their difference is 13 . find their product .
  - its program: `divide(n1,const_2)|subtract(n0,#0)|divide(#1,const_2)|subtract(n0,#2)|`
  - run on the test numbers: 103, closest option e -> **wrong**

**Test question 2581**: a batsman had a certain average of runs for 16 innings . in the 17 th innings , he made a score of 87 runs thereby increasing his average by 3 . what is his average after 17 innings ?
- correct option a (a ) 39 , b ) 88 , c ) 266 , d ) 278 , e ) 221)
- **TF-IDF** (similarity 0.802): suraj has a certain average of runs for 16 innings . in the 17 th innings he scores 112 runs thereby increasing his average by 6 runs . what is his average after the 17 th innings ?
  - its program: `multiply(n0,n3)|subtract(n1,n0)|subtract(n2,#0)|divide(#2,#1)|`
  - run on the test numbers: 39, closest option a -> **right**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.915): suraj has a certain average of runs for 16 innings . in the 17 th innings he scores 112 runs thereby increasing his average by 6 runs . what is his average after the 17 th innings ?
  - its program: `multiply(n0,n3)|subtract(n1,n0)|subtract(n2,#0)|divide(#2,#1)|`
  - run on the test numbers: 39, closest option a -> **right**

**Test question 2701**: in a fuel station the service costs $ 1.50 per car , every liter of fuel costs 0.35 $ . assuming that you own 3 limos and 2 fleet vans and all fuel tanks are empty . how much will it cost to fuel all cars together if a limo tank is 32 liters and an fleet van tank is 75 % bigger ?
- correct option a (a ) $ 78.80 , b ) $ 79.80 , c ) $ 78.90 , d ) $ 79.90 , e ) $ 77.80)
- **TF-IDF** (similarity 0.777): in a fuel station the service costs $ 1.15 per car , every liter of fuel costs 0.4 $ . assuming that you own 2 sports cars and 2 executive cars and all fuel tanks are empty . how much will it cost to fuel all cars together if a sports car tank is 32 liters and an executive car tank is 75 % bigger ?
  - its program: `multiply(n4,n5)|multiply(n2,n4)|divide(#0,const_100)|multiply(n1,#1)|add(n4,#2)|multiply(n3,#4)|multiply(n1,#5)|add(#6,#3)|`
  - run on the test numbers: 72.8, closest option e -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.923): in a fuel station the service costs $ 1.15 per car , every liter of fuel costs 0.4 $ . assuming that you own 2 sports cars and 2 executive cars and all fuel tanks are empty . how much will it cost to fuel all cars together if a sports car tank is 32 liters and an executive car tank is 75 % bigger ?
  - its program: `multiply(n4,n5)|multiply(n2,n4)|divide(#0,const_100)|multiply(n1,#1)|add(n4,#2)|multiply(n3,#4)|multiply(n1,#5)|add(#6,#3)|`
  - run on the test numbers: 72.8, closest option e -> **wrong**

### TF-IDF similarity 0.85 to 1.00 (313 new test questions)

**Test question 1559**: in an examination , the percentage of students qualified to the students appeared from school ' p ' is 70 % . in school ' q ' , the number of students appeared is 30 % more than the students appeared from school ' p ' and the number of students qualified from school ' q ' is 50 % more than the students qualified from school ' p ' . what is the % of students qualified to the number of students appeared from school ' q ' ?
- correct option b (a ) 80.78 % , b ) 80.76 % , c ) 80.72 % , d ) 80.79 % , e ) 80.74 %)
- **TF-IDF** (similarity 0.992): in an examination , the percentage of students qualified to the number of students appeared from school a is 70 % . in school b , the number of students appeared is 20 % more than the students appeared from school a and the number of students qualified from school b is 50 % more than the students qualified from school a . what is the percentage of students qualified to the number of students appeared from school b ?
  - its program: `multiply(const_0_25,const_2)|subtract(n0,n1)|subtract(n2,#0)|subtract(#2,const_12)|add(#1,#3)`
  - run on the test numbers: 77.5, closest option c -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.907): in an examination , the percentage of students qualified to the number of students appeared from school a is 70 % . in school b , the number of students appeared is 20 % more than the students appeared from school a and the number of students qualified from school b is 50 % more than the students qualified from school a . what is the percentage of students qualified to the number of students appeared from school b ?
  - its program: `multiply(const_0_25,const_2)|subtract(n0,n1)|subtract(n2,#0)|subtract(#2,const_12)|add(#1,#3)`
  - run on the test numbers: 77.5, closest option c -> **wrong**

**Test question 1852**: a library has an average of 510 visitors on sunday and 240 on other days . the average number of visitors per day in a month of 30 days beginning with a sunday is
- correct option d (a ) 250 , b ) 276 , c ) 280 , d ) 285 , e ) none)
- **TF-IDF** (similarity 1.000): a library has an average of 510 visitors on sunday and 240 on other days . the average number of visitors per day in a month of 30 days beginning with a sunday is :
  - its program: `add(const_1,const_4)|multiply(n0,#0)|multiply(#0,#0)|multiply(n1,#2)|add(#1,#3)|divide(#4,n2)|`
  - run on the test numbers: 285, closest option d -> **right**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.998): a library has an average of 510 visitors on sunday and 240 on other days . the average number of visitors per day in a month of 30 days beginning with a sunday is :
  - its program: `add(const_1,const_4)|multiply(n0,#0)|multiply(#0,#0)|multiply(n1,#2)|add(#1,#3)|divide(#4,n2)|`
  - run on the test numbers: 285, closest option d -> **right**

**Test question 2326**: the distance between two cities a and b is 330 km . a train starts from a at 8 a . m . and travels towards b at 60 km / hr . another train starts from b at 9 a . m . and travels towards a at 75 km / hr . at what time do they meet ?
- correct option c (a ) 12 , b ) 10 , c ) 11 , d ) 09 , e ) 03)
- **TF-IDF** (similarity 0.957): the distance between two cities a and b is 465 km . a train starts from a at 8 a . m . and travel towards b at 60 km / hr . another train starts from b at 9 a . m and travels towards a at 75 km / hr . at what time do they meet ?
  - its program: `add(n0,n4)|add(n2,n4)|divide(#0,#1)|add(n1,#2)|`
  - run on the test numbers: 11, closest option c -> **right**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.999): the distance between two cities a and b is 465 km . a train starts from a at 8 a . m . and travel towards b at 60 km / hr . another train starts from b at 9 a . m and travels towards a at 75 km / hr . at what time do they meet ?
  - its program: `add(n0,n4)|add(n2,n4)|divide(#0,#1)|add(n1,#2)|`
  - run on the test numbers: 11, closest option c -> **right**

## Seen wording (Rule 1)

**Test question 742**: cole drove from home to work at an average speed of 60 kmh . he then returned home at an average speed of 100 kmh . if the round trip took a total of 2 hours , how many minutes did it take cole to drive to work ?
- correct option d (a ) 66 , b ) 70 , c ) 72 , d ) 75 , e ) 78)
- training questions with the same template: 9
  - cole drove from home to work at an average speed of 75 kmh . he then returned home at an average speed of 105 kmh . if the round trip took a total of 1 hours , how many minutes did it take cole to drive to work ?
  - cole drove from home to work at an average speed of 60 kmh . he then returned home at an average speed of 90 kmh . if the round trip took a total of 2 hours , how many minutes did it take cole to drive to work ?
  - cole drove from home to work at an average speed of 80 kmh . he then returned home at an average speed of 120 kmh . if the round trip took a total of 3 hours , how many minutes did it take cole to drive to work ?
- most common training program run on the test numbers: 75, closest option d -> **right**

**Test question 1156**: if john makes a contribution to a charity fund at school , the average contribution size will increase by 50 % reaching $ 75 per person . if there were 4 other contributions made before john ' s , what is the size of his donation ?
- correct option b (a ) $ 100 , b ) $ 175 , c ) $ 200 , d ) $ 250 , e ) $ 450)
- training questions with the same template: 2
  - if john makes a contribution to a charity fund at school , the average contribution size will increase by 50 % reaching $ 75 per person . if there were 6 other contributions made before john ' s , what is the size of his donation ?
  - if john makes a contribution to a charity fund at school , the average contribution size will increase by 50 % reaching $ 75 per person . if there were 2 other contributions made before john ' s , what is the size of his donation ?
- most common training program run on the test numbers: 175, closest option b -> **right**

**Test question 2681**: sonika deposited rs . 8000 which amounted to rs . 9200 after 3 years at simple interest . had the interest been 1.5 % more . she would get how much ?
- correct option a (a ) 9560 , b ) 96288 , c ) 26667 , d ) 1662 , e ) 2882)
- training questions with the same template: 14
  - sonika deposited rs . 8000 which amounted to rs . 11200 after 3 years at simple interest . had the interest been 2 % more . she would get how much ?
  - sonika deposited rs . 12000 which amounted to rs . 19500 after 4 years at simple interest . had the interest been 3 % more . she would get how much ?
  - sonika deposited rs . 8000 which amounted to rs . 9200 after 3 years at simple interest . had the interest been 3 % more . she would get how much ?
- most common training program run on the test numbers: 9560, closest option a -> **right**

