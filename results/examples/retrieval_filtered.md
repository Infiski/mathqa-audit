# Retrieved training questions (filtered split, test set)

## New wording (Rule 2)

Bands are by TF-IDF similarity to the picked training question.

### TF-IDF similarity 0.00 to 0.50 (214 new test questions)

**Test question 668**: how many 5 - digit numbers are there , if the two leftmost digits are even , the other digits are odd and the digit 2 can not appear more than once in the number .
- reference value 2375
- **TF-IDF** (similarity 0.328): how many 4 - digit numbers are there such that all 3 digits are different and the first digit and last digit is not zero ?
  - its program: `( Mult  ( Pow  ( Sub  10 1 ) ( Div  4 2 ) ) ( Pow  ( Sub  ( Sub  10 1 ) 1 ) ( Div  4 2 ) ) )`
  - run on the test numbers: 43987.7 -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.806): how many even 4 - digit numbers can be formed , so that the numbers are divisible by 4 and no two digits are repeated ?
  - its program: `( Add  ( Mult  ( Mult  ( Sub  ( Sub  10 2 ) 1 ) ( Sub  ( Sub  10 2 ) 1 ) ) ( Sub  ( Sub  ( Div  100 4 ) 3 ) ( Mult  2 3 ) ) ) ( Mult  ( Mult  ( Sub  10 2 ) ( Sub  ( Sub  10 2 ) 1 ) ) ( Mult  2 3 ) ) )`
  - run on the test numbers: 875 -> **wrong**

**Test question 726**: niall ' s income is 60 % less than rex ' s income , and sam ' s income is 25 % less than niall ' s income . if rex gave 60 % of his income to sam and 40 % of his income to niall , niall ' s new income would be what fraction of sam ' s new income ?
- reference value 0.888889
- **TF-IDF** (similarity 0.260): if 25 % of x is 15 less than 15 % of 1500 , then x is ?
  - its program: `( Div  ( Sub  ( Mult  1500 ( Div  15 100 ) ) 15 ) ( Div  25 100 ) )`
  - run on the test numbers: -1.66667 -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.662): the monthly incomes of a and b are in the ratio 5 : 2 . b ' s monthly income is 12 % more than c ' s monthly income . if c ' s monthly income is rs . 17000 , then find the annual income of a ?
  - its program: `( Mult  ( Mult  ( Mult  17000 ( Add  1 ( Div  12 100 ) ) ) ( Div  5 2 ) ) 12 )`
  - run on the test numbers: 9216 -> **wrong**

**Test question 1435**: if x and y are integers such that x ^ 2 = y and xy = 27 , then x – y = ?
- reference value 6
- **TF-IDF** (similarity 0.350): if a and b are integers and ( a * b ) ^ 5 = 128 y , y could be :
  - its program: `( Mult  ( Div  128 ( Pow  2 5 ) ) 2 )`
  - run on the test numbers: 13.5 -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.843): if xy = 1 , x / y = 36 , for positive numbers x and y , y = ?
  - its program: `( Pow  ( Div  1 36 ) 0.5 )`
  - run on the test numbers: 0.272166 -> **wrong**

### TF-IDF similarity 0.50 to 0.70 (37 new test questions)

**Test question 116**: 3 people candidates contested an election and they received 1136 , 7636 and 11628 votes respectively . what is the percentage of the total votes did the winning candidate get ?
- reference value 57
- **TF-IDF** (similarity 0.660): 3 candidates in an election and received 1000 , 2000 and 4000 votes respectively . what % of the total votes did the winning candidate got in that election ?
  - its program: `( Mult  ( Div  4000 ( Add  ( Add  1000 2000 ) 4000 ) ) 100 )`
  - run on the test numbers: 57 -> **right**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.976): 3 candidates in an election and received 1000 , 2000 and 4000 votes respectively . what % of the total votes did the winning candidate got in that election ?
  - its program: `( Mult  ( Div  4000 ( Add  ( Add  1000 2000 ) 4000 ) ) 100 )`
  - run on the test numbers: 57 -> **right**

**Test question 862**: liz drove from point a to point b at 40 km / h . on her way back she drove at 50 km / h and therefore her way back lasted one hour less . what is the distance ( in km ) between a and b ?
- reference value 200
- **TF-IDF** (similarity 0.589): a train travelled from point a to point b at 160 km / h . on its way back the train travelled at 120 km / h and therefore the trip back lasted one hour longer . what is the distance ( in km ) between a and b ?
  - its program: `( Mult  ( Add  ( Div  120 ( Sub  160 120 ) ) 1 ) 120 )`
  - run on the test numbers: -200 -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.816): a train travelled from point a to point b at 160 km / h . on its way back the train travelled at 120 km / h and therefore the trip back lasted one hour longer . what is the distance ( in km ) between a and b ?
  - its program: `( Mult  ( Add  ( Div  120 ( Sub  160 120 ) ) 1 ) 120 )`
  - run on the test numbers: -200 -> **wrong**

**Test question 1485**: it costs $ 2 for the first 15 minutes to use the bumper cars at a fair ground . after the first 15 minutes it costs $ 6 per hour . if a certain customer uses the bumper cars for 3 hours and 25 minutes , how much will it cost him ?
- reference value 21
- **TF-IDF** (similarity 0.670): it costs $ 6 for the first 1 / 4 hour to use the copier at kinkos . after the first ¼ hour it costs $ 8 per hour . if a certain customer uses the copier for 4 hours and 25 minutes , how much will it cost him ?
  - its program: `( Add  ( Add  ( Add  25 8 ) 6 ) ( Div  ( Add  25 8 ) 100 ) )`
  - run on the test numbers: 33.31 -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.752): it costs $ 6 for the first 1 / 4 hour to use the copier at kinkos . after the first ¼ hour it costs $ 8 per hour . if a certain customer uses the copier for 4 hours and 25 minutes , how much will it cost him ?
  - its program: `( Add  ( Add  ( Add  25 8 ) 6 ) ( Div  ( Add  25 8 ) 100 ) )`
  - run on the test numbers: 33.31 -> **wrong**

### TF-IDF similarity 0.70 to 0.85 (43 new test questions)

**Test question 859**: a piece of work can finish by a certain number of men in 100 days . if however , there were 10 men less , it would take 10 days more for the work to be finished . how many men were there originally ?
- reference value 110
- **TF-IDF** (similarity 0.741): a certain number of men can finish a piece of work in 10 days . however , if there were 10 less men it will take 10 days more for the work to be finished . how many men were there originally ?
  - its program: `( Div  10 ( Sub  1 ( Div  10 ( Add  10 10 ) ) ) )`
  - run on the test numbers: 110 -> **right**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.993): a certain number of men can finish a piece of work in 10 days . however , if there were 10 less men it will take 10 days more for the work to be finished . how many men were there originally ?
  - its program: `( Div  10 ( Sub  1 ( Div  10 ( Add  10 10 ) ) ) )`
  - run on the test numbers: 110 -> **right**

**Test question 1001**: 7 m - 20 = 2 m , then m + 7 is equal to ?
- reference value 11
- **TF-IDF** (similarity 0.816): ( 51 + 52 + 53 + … … … + 100 ) is equal to :
  - its program: `( Sub  ( Div  ( Mult  100 ( Add  100 1 ) ) 2 ) ( Div  ( Mult  ( Sub  51 1 ) 51 ) 2 ) )`
  - run on the test numbers: 7 -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.879): ( 51 + 52 + 53 + … … … + 100 ) is equal to :
  - its program: `( Sub  ( Div  ( Mult  100 ( Add  100 1 ) ) 2 ) ( Div  ( Mult  ( Sub  51 1 ) 51 ) 2 ) )`
  - run on the test numbers: 7 -> **wrong**

**Test question 1316**: 7 carpet - weavers can weave 7 carpets in 7 days . at the same rate , how many carpets would be woven by 14 carpet - weavers in 14 days ?
- reference value 28
- **TF-IDF** (similarity 0.734): 4 weavers can weave 4 mats in 4 days . at the same rate , how many mats would be woven by 6 weavers in 6 days ?
  - its program: `( Mult  6 ( Mult  6 ( Div  4 ( Mult  4 4 ) ) ) )`
  - run on the test numbers: 28 -> **right**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.875): 4 weavers can weave 4 mats in 4 days . at the same rate , how many mats would be woven by 6 weavers in 6 days ?
  - its program: `( Mult  6 ( Mult  6 ( Div  4 ( Mult  4 4 ) ) ) )`
  - run on the test numbers: 28 -> **right**

### TF-IDF similarity 0.85 to 1.00 (165 new test questions)

**Test question 967**: rs . 385 were divided among x , y , z in such a way that x had rs . 20 more than y and z had rs 15 more than x . how much was y ’ s share ?
- reference value 145
- **TF-IDF** (similarity 1.000): rs . 770 were divided among a , b , c in such a way that a had rs . 40 more than b and c had rs 30 more than a . how much was b â € ™ s share ?
  - its program: `( Add  ( Add  ( Div  ( Sub  770 ( Add  ( Add  40 40 ) 30 ) ) 3 ) 30 ) 40 )`
  - run on the test numbers: 145 -> **right**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.828): if x gets 25 % more than y and y gets 20 % more than z , the share of z out of rs . 555 will be :
  - its program: `( Div  555 ( Add  ( Add  ( Mult  ( Add  1 ( Div  25 100 ) ) ( Add  1 ( Div  20 100 ) ) ) ( Add  1 ( Div  20 100 ) ) ) 1 ) )`
  - run on the test numbers: 1.87032 -> **wrong**

**Test question 1155**: company t produces two kinds of stereos : basic and deluxe . of the stereos produced by company t last month , 2 / 3 were basic and the rest were deluxe . if it takes 7 / 5 as many hours to produce a deluxe stereo as it does to produce a basic stereo , then the number of hours it took to produce the deluxe stereos last month was what fraction of the total number of hours it took to produce all the stereos ?
- reference value 0.411765
- **TF-IDF** (similarity 1.000): company m produces two kinds of stereos : basic and deluxe . of the stereos produced by company m last month , 2 / 3 were basic and the rest were deluxe . if it takes 7 / 5 as many hours to produce a deluxe stereo as it does to produce a basic stereo , then the number of hours it took to produce the deluxe stereos last month was what fraction of the total number of hours it took to produce all the stereos ?
  - its program: `( Div  7 ( Add  ( Add  ( Div  ( Mult  ( Mult  3 5 ) 2 ) 3 ) 7 ) 5 ) )`
  - run on the test numbers: 0.318182 -> **wrong**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.976): company m produces two kinds of stereos : basic and deluxe . of the stereos produced by company m last month , 2 / 3 were basic and the rest were deluxe . if it takes 7 / 5 as many hours to produce a deluxe stereo as it does to produce a basic stereo , then the number of hours it took to produce the deluxe stereos last month was what fraction of the total number of hours it took to produce all the stereos ?
  - its program: `( Div  7 ( Add  ( Add  ( Div  ( Mult  ( Mult  3 5 ) 2 ) 3 ) 7 ) 5 ) )`
  - run on the test numbers: 0.318182 -> **wrong**

**Test question 1444**: a soccer store typically sells replica jerseys at a discount of 30 percent to 50 percent off list price . during the annual summer sale , everything in the store is an additional 20 percent off the original list price . if a replica jersey ' s list price is $ 80 , approximately what y percent of the list price is the lowest possible sale price ?
- reference value 40
- **TF-IDF** (similarity 1.000): a soccer store typically sells replica jerseys at a discount of 30 percent to 50 percent off list price . during the annual summer sale , everything in the store is an additional 20 percent off the original list price . if a replica jersey ' s list price is $ 80 , approximately what percent q of the list price is the lowest possible sale price ?
  - its program: `( Div  80 2 )`
  - run on the test numbers: 40 -> **right**
- **BERT (all-MiniLM-L6-v2)** (similarity 0.984): a soccer store typically sells replica jerseys at a discount of 30 percent to 70 percent off list price . during the annual summer sale , everything in the store is an additional 20 percent off the original list price . if a replica jersey ' s list price is $ 80 , approximately what percent of the list price is the lowest possible sale price ?
  - its program: `( Div  80 2 )`
  - run on the test numbers: 40 -> **right**

## Seen wording (Rule 1)

**Test question 401**: in triangle pqr , the angle q = 90 degree , pq = 5 cm , qr = 8 cm . x is a variable point on pq . the line through x parallel to qr , intersects pr at y and the line through y , parallel to pq , intersects qr at z . find the least possible length of xz
- reference value 4
- training questions with the same template: 3
  - in triangle pqr , the angle q = 90 degree , pq = 2 cm , qr = 8 cm . x is a variable point on pq . the line through x parallel to qr , intersects pr at y and the line through y , parallel to pq , intersects qr at z . find the least possible length of xz
  - in triangle pqr , the angle q = 90 degree , pq = 7 cm , qr = 8 cm . x is a variable point on pq . the line through x parallel to qr , intersects pr at y and the line through y , parallel to pq , intersects qr at z . find the least possible length of xz
  - in triangle pqr , the angle q = 90 degree , pq = 3 cm , qr = 8 cm . x is a variable point on pq . the line through x parallel to qr , intersects pr at y and the line through y , parallel to pq , intersects qr at z . find the least possible length of xz
- most common training program run on the test numbers: 4 -> **right**

**Test question 629**: if john makes a contribution to a charity fund at school , the average contribution size will increase by 50 % reaching $ 75 per person . if there were 4 other contributions made before john ' s , what is the size of his donation ?
- reference value 175
- training questions with the same template: 2
  - if john makes a contribution to a charity fund at school , the average contribution size will increase by 50 % reaching $ 75 per person . if there were 6 other contributions made before john ' s , what is the size of his donation ?
  - if john makes a contribution to a charity fund at school , the average contribution size will increase by 50 % reaching $ 75 per person . if there were 2 other contributions made before john ' s , what is the size of his donation ?
- most common training program run on the test numbers: 175 -> **right**

**Test question 1447**: jar a has 6 % more marbles than jar b . what percent of marbles from jar a need to be moved into jar b so that both jars have equal marbles ?
- reference value 2.83019
- training questions with the same template: 1
  - jar a has 26 % more marbles than jar b . what percent of marbles from jar a need to be moved into jar b so that both jars have equal marbles ?
- most common training program run on the test numbers: 2.83019 -> **right**

