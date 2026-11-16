# DeductReasoner examples (filtered test set)

## Right, and the template is in training (1068 questions)

**Test question 233**: a spirit and water solution is sold in a market . the cost per liter of the solution is directly proportional to the part ( fraction ) of spirit ( by volume ) the solution has . a solution of 1 liter of spirit and 1 liter of water costs 40 cents . how many cents does a solution of 1 liter of spirit and 2 liters of water cost ?
- numbers: [1.0, 1.0, 40.0, 1.0, 2.0], reference value 40
- reference steps: 1 + 2 = 3; 1 / 3 = 0.333333; 0.333333 * 40 = 13.3333; 3 * 13.3333 = 40
- training question with the same template: a spirit and water solution is sold in a market . the cost per liter of the solution is directly proportional to the part ( fraction ) of spirit ( by volume ) the solution has . a solution of 1 liter of spirit and 1 liter of water costs 60 cents . how many cents does a solution of 1 liter of spirit and 2 liters of water cost ?
- its program on the test numbers: 1 + 2 = 3; 1 / 3 = 0.333333; 0.333333 * 40 = 13.3333; 3 * 13.3333 = 40
- DeductReasoner's steps: 1 + 2 = 3; 1 / 3 = 0.333333; 0.333333 * 40 = 13.3333; 13.3333 * 3 = 40
- same steps as the training program: yes

**Test question 1500**: a train running at the speed of 162 km / hr crosses a pole in 9 seconds . find the length of the train .
- numbers: [162.0, 9.0], reference value 405
- reference steps: 162 * 1000 = 162000; 162000 / 3600 = 45; 45 * 9 = 405
- training question with the same template: a train running at the speed of 72 km / hr crosses a pole in 8 seconds . find the length of the train .
- its program on the test numbers: 162 * 1000 = 162000; 162000 / 3600 = 45; 45 * 9 = 405
- DeductReasoner's steps: 1000 * 162 = 162000; 162000 / 3600 = 45; 45 * 9 = 405
- same steps as the training program: yes

**Test question 2266**: one fourth of a solution that was 10 % salt by weight was replaced by a second solution resulting in a solution that was 16 percent sugar by weight . the second solution was what percent salt by weight ?
- numbers: [10.0, 16.0], reference value 34
- reference steps: 16 / 100 = 0.16; 10 / 100 = 0.1; 0.16 * 4 = 0.64; 0.1 * 4 = 0.4; 0.4 - 0.1 = 0.3; 0.64 - 0.3 = 0.34; 0.34 * 100 = 34
- training question with the same template: one fourth of a solution that was 12 % salt by weight was replaced by a second solution resulting in a solution that was 16 percent sugar by weight . the second solution was what percent salt by weight ?
- its program on the test numbers: 16 / 100 = 0.16; 10 / 100 = 0.1; 0.16 * 4 = 0.64; 0.1 * 4 = 0.4; 0.4 - 0.1 = 0.3; 0.64 - 0.3 = 0.34; 0.34 * 100 = 34
- DeductReasoner's steps: 16 / 100 = 0.16; 10 / 100 = 0.1; 0.16 * 4 = 0.64; 0.1 * 4 = 0.4; 0.4 - 0.1 = 0.3; 0.64 - 0.3 = 0.34; 0.34 * 100 = 34
- same steps as the training program: yes

**Test question 2443**: a brick measures 20 cm * 10 cm * 7.5 cm how many bricks will be required for a wall 28 m * 2 m * 0.75 m ?
- numbers: [20.0, 10.0, 7.5, 28.0, 2.0, 0.75], reference value 28000
- reference steps: 28 * 100 = 2800; 2 * 100 = 200; 0.75 * 100 = 75; 2800 * 200 = 560000; 75 * 560000 = 4.2e+07; 4.2e+07 / 20 = 2.1e+06; 2.1e+06 / 10 = 210000; 210000 / 7.5 = 28000
- training question with the same template: a brick measures 20 cm * 10 cm * 7.5 cm how many bricks will be required for a wall 27 m * 2 m * 0.75 m ?
- its program on the test numbers: 28 * 100 = 2800; 2 * 100 = 200; 0.75 * 100 = 75; 2800 * 200 = 560000; 75 * 560000 = 4.2e+07; 4.2e+07 / 20 = 2.1e+06; 2.1e+06 / 10 = 210000; 210000 / 7.5 = 28000
- DeductReasoner's steps: 100 * 28 = 2800; 100 * 2 = 200; 100 * 0.75 = 75; 200 * 2800 = 560000; 560000 * 75 = 4.2e+07; 4.2e+07 / 20 = 2.1e+06; 2.1e+06 / 10 = 210000; 210000 / 7.5 = 28000
- same steps as the training program: yes

**Test question 2940**: 32.32 / 2000 is equal to :
- numbers: [32.32, 2000.0], reference value 0.01616
- reference steps: 32.32 / 2000 = 0.01616
- training question with the same template: 25.25 / 1500 is equal to :
- its program on the test numbers: 32.32 / 2000 = 0.01616
- DeductReasoner's steps: 32.32 / 2000 = 0.01616
- same steps as the training program: yes

## Right, with new wording (171 questions)

**Test question 1474**: together , 15 type a machines and 7 type b machines can complete a certain job in 4 hours . together 8 type b machines and 15 type c machines can complete the same job in 11 hours . how many hours e would it take one type a machine , one type b machine , and one type c machine working together to complete the job ( assuming constant rates for each machine ) ?
- numbers: [15.0, 7.0, 4.0, 8.0, 15.0, 11.0], reference value 44
- reference steps: 1 / 4 = 0.25; 1 / 11 = 0.0909091; 0.25 + 0.0909091 = 0.340909; 0.340909 / 15 = 0.0227273; 1 / 0.0227273 = 44
- most similar training question (TF-IDF): together , 15 type a machines and 7 type b machines can complete a certain job in 4 hours . together 8 type b machines and 15 type c machines can complete the same job in 11 hours . how many hours r would it take one type a machine , one type b machine , and one type c machine working together to complete the job ( assuming constant rates for each machine ) ?
- its program on the test numbers: 1 / 4 = 0.25; 1 / 11 = 0.0909091; 0.25 + 0.0909091 = 0.340909; 0.340909 / 15 = 0.0227273; 1 / 0.0227273 = 44
- DeductReasoner's steps: 1 / 4 = 0.25; 1 / 11 = 0.0909091; 0.0909091 + 0.25 = 0.340909; 0.340909 / 15 = 0.0227273; 1 / 0.0227273 = 44
- same steps as the training program: yes

**Test question 1756**: a taxi leaves point a 2 hours after a bus left the same spot . the bus is traveling 20 mph slower than the taxi . find the speed of the taxi , if it overtakes the bus in two hours .
- numbers: [2.0, 20.0], reference value 40
- reference steps: 2 + 2 = 4; 2 * 20 = 40; 40 + 40 = 80; 4 - 2 = 2; 80 / 2 = 40
- most similar training question (TF-IDF): a taxi leaves point a 3 hours after a bus left the same spot . the bus is traveling 30 mph slower than the taxi . find the speed of the taxi , if it overtakes the bus in three hours .
- its program on the test numbers: 2 + 2 = 4; 2 * 20 = 40; 40 + 40 = 80; 4 - 2 = 2; 80 / 2 = 40
- DeductReasoner's steps: 2 + 2 = 4; 2 * 20 = 40; 40 + 40 = 80; 4 - 2 = 2; 80 / 2 = 40
- same steps as the training program: yes

**Test question 1869**: the smallest value of n , for which 2 n + 1 is not a prime number is
- numbers: [2.0, 1.0], reference value 4
- reference steps: 2 + 2 = 4
- most similar training question (TF-IDF): the smallest value of n , for which 2 n + 1 is not a prime number , is
- its program on the test numbers: 2 + 2 = 4
- DeductReasoner's steps: 2 + 2 = 4
- same steps as the training program: yes

**Test question 2158**: calculate the area of a triangle , if the sides of are 52 cm , 48 cm and 20 cm , what is its area ?
- numbers: [52.0, 48.0, 20.0], reference value 480
- reference steps: 48 / 2 = 24; 24 * 20 = 480
- most similar training question (TF-IDF): calculate the area of a triangle , if the sides are 13 cm , 12 cm and 5 cm , what is its area ?
- its program on the test numbers: 48 / 2 = 24; 24 * 20 = 480
- DeductReasoner's steps: 48 / 2 = 24; 24 * 20 = 480
- same steps as the training program: yes

**Test question 2198**: in a simultaneous throw of pair of dice . find the probability of getting the total more than 7
- numbers: [7.0], reference value 0.416667
- reference steps: 7 + 4 = 11; 2 + 4 = 6; 11 + 4 = 15; 6 * 6 = 36; 15 / 36 = 0.416667
- most similar training question (TF-IDF): in a simultaneous throw of pair of dice . find the probability of getting the total more than 7 ?
- its program on the test numbers: 7 + 4 = 11; 2 + 4 = 6; 11 + 4 = 15; 6 * 6 = 36; 15 / 36 = 0.416667
- DeductReasoner's steps: 4 + 7 = 11; 2 + 4 = 6; 11 + 4 = 15; 6 * 6 = 36; 15 / 36 = 0.416667
- same steps as the training program: yes

## Wrong, although the template is in training (78 questions)

**Test question 573**: two employees x and y are paid a total of rs . 506 per week by their employer . if x is paid 120 percent of the sum paid to y , how much is y paid per week ?
- numbers: [506.0, 120.0], reference value 230
- reference steps: 1 + 4 = 5; 5 * 2 = 10; 10 + 1 = 11; 10 * 506 = 5060; 11 * 2 = 22; 5060 / 22 = 230
- training question with the same template: two employees x and y are paid a total of rs . 572 per week by their employer . if x is paid 120 percent of the sum paid to y , how much is y paid per week ?
- its program on the test numbers: 1 + 4 = 5; 5 * 2 = 10; 10 + 1 = 11; 10 * 506 = 5060; 11 * 2 = 22; 5060 / 22 = 230
- DeductReasoner's steps: 1 + 4 = 5; 5 * 2 = 10; 10 * 100 = 1000; 10 * 506 = 5060; 1000 * 2 = 2000; 5060 / 2000 = 2.53
- same steps as the training program: no
- what went wrong: same number of steps, different operations

**Test question 1200**: some persons can do a piece of work in 32 days . two times the number of these people will do half of that work in ?
- numbers: [32.0], reference value 8
- reference steps: 1 / 2 = 0.5; 0.5 * 32 = 16; 0.5 * 16 = 8
- training question with the same template: some persons can do a piece of work in 20 days . two times the number of these people will do half of that work in ?
- its program on the test numbers: 1 / 2 = 0.5; 0.5 * 32 = 16; 0.5 * 16 = 8
- DeductReasoner's steps: 1 + 4 = 5; 5 * 32 = 160; 160 * 5 = 800
- same steps as the training program: no
- what went wrong: same number of steps, different operations

**Test question 1450**: find the number of different prime factors of 25650
- numbers: [25650.0], reference value 4
- reference steps: 2 + 2 = 4
- training question with the same template: find the number of different prime factors of 6440
- its program on the test numbers: 2 + 2 = 4
- DeductReasoner's steps: 1 + 4 = 5; 5 * 2 = 10; 10 * 100 = 1000; 1000 * 2 = 2000; 2000 + 3 = 2003; 2003 / 1000 = 2.003; 2.003 * 2 = 4.006; 4.006 * 60 = 240.36; 240.36 / 100 = 2.4036; 2.4036 + 5 = 7.4036
- same steps as the training program: no
- what went wrong: too many steps

**Test question 2723**: of 70 players on a football team , 43 are throwers . the rest of the team is divided so one third are left - handed and the rest are right handed . assuming that all throwers are right handed , how many right - handed players are there total ?
- numbers: [70.0, 43.0], reference value 61
- reference steps: 1 / 3 = 0.333333; 70 - 43 = 27; 1 - 0.333333 = 0.666667; 27 * 0.666667 = 18; 18 + 43 = 61
- training question with the same template: of 70 players on a football team , 28 are throwers . the rest of the team is divided so one third are left - handed and the rest are right handed . assuming that all throwers are right handed , how many right - handed players are there total ?
- its program on the test numbers: 1 / 3 = 0.333333; 70 - 43 = 27; 1 - 0.333333 = 0.666667; 27 * 0.666667 = 18; 18 + 43 = 61
- DeductReasoner's steps: 1 + 4 = 5; 70 - 43 = 27; 1 - 5 = -4; -4 * 27 = -108; -108 + 43 = -65
- same steps as the training program: no
- what went wrong: same number of steps, different operations

**Test question 2807**: the calendar of the year 2040 can be used again in the year ?
- numbers: [2040.0], reference value 2068
- reference steps: 4 * 4 = 16; 16 - 2 = 14; 14 * 2 = 28; 28 + 2040 = 2068
- training question with the same template: the calendar of the year 2060 can be used again in the year ?
- its program on the test numbers: 4 * 4 = 16; 16 - 2 = 14; 14 * 2 = 28; 28 + 2040 = 2068
- DeductReasoner's steps: 1 + 4 = 5; 5 * 2 = 10; 10 * 100 = 1000; 1000 + 2040 = 3040
- same steps as the training program: no
- what went wrong: same number of steps, different operations

## Wrong, with new wording (288 questions)

**Test question 517**: 3 pounds of 05 grass seed contain 1 percent herbicide . a different type of grass seed , 20 , which contains 20 percent herbicide , will be mixed with 3 pounds of 05 grass seed . how much grass seed of type 20 should be added to the 3 pounds of 05 grass seed so that the mixture contains 15 percent herbicide ?
- numbers: [3.0, 5.0, 1.0, 20.0, 20.0, 3.0, 5.0, 20.0, 3.0, 5.0, 15.0], reference value 8.4
- reference steps: 3 * 15 = 45; 20 - 15 = 5; 45 - 3 = 42; 42 / 5 = 8.4
- DeductReasoner's steps: 5 + 3 = 8; 20 / 100 = 0.2; 20 / 100 = 0.2; 0.2 * 3 = 0.6; 0.2 * 3 = 0.6; 0.6 + 0.6 = 1.2; 1.2 + 3 = 4.2; 4.2 - 20 = -15.8; -15.8 / 100 = -0.158
- same steps as the training program: no
- what went wrong: too many steps

**Test question 725**: there is a lot of speculation that the economy of a country depends on how fast people spend their money in addition to how much they save . auggie was very curious to test this theory . auggie spent all of his money in 5 stores . in each store , he spent rs . 4 more than one - half of what he had when he went in . how many rupees did auggie have when he entered the first store ?
- numbers: [5.0, 4.0], reference value 248
- reference steps: 4 * 2 = 8; 8 + 4 = 12; 12 * 2 = 24; 24 + 4 = 28; 28 * 2 = 56; 56 + 4 = 60; 60 * 2 = 120; 120 + 4 = 124; 124 * 2 = 248
- most similar training question (TF-IDF): little roshini had $ 10.50 . he spent some money on sweets and gave to his two friends $ 3.40 each . how much money was spent for sweets ?
- its program on the test numbers: 4 * 2 = 8; 5 - 8 = -3
- DeductReasoner's steps: 1 + 4 = 5; 1 / 5 = 0.2; 5 + 1 = 6; 6 + 4 = 10; 10 + 0.2 = 10.2; 4 / 10.2 = 0.392157; 0.392157 * 5 = 1.96078
- same steps as the training program: no
- what went wrong: too few steps

**Test question 1294**: the sum q of prime numbers that are greater than 60 but less than 70 is
- numbers: [60.0, 70.0], reference value 128
- reference steps: 60 + 1 = 61; 70 - 3 = 67; 61 + 67 = 128
- most similar training question (TF-IDF): the average of first 3 prime numbers greater than 20 is ?
- its program on the test numbers: 70 + 3 = 73; 73 + 4 = 77; 77 + 2 = 79; 73 + 79 = 152; 79 + 2 = 81; 152 + 81 = 233; 233 / 60 = 3.88333
- DeductReasoner's steps: 1 + 60 = 61; 1 + 2 = 3; 3 + 61 = 64; 3 + 2 = 5; 5 + 64 = 69; 5 + 1 = 6; 6 + 69 = 75; 6 + 1 = 7; 7 + 75 = 82; 7 + 1 = 8
- same steps as the training program: no
- what went wrong: too many steps

**Test question 1467**: if 28 % of a number exceeds 18 % of it by 7.2 , then find the number ?
- numbers: [28.0, 18.0, 7.2], reference value 90
- reference steps: 28 - 18 = 10; 10 / 100 = 0.1; 7.2 / 0.1 = 72; 72 + 18 = 90
- most similar training question (TF-IDF): if 16 % of 40 % of a number is 6 , then the number is
- its program on the test numbers: 28 / 100 = 0.28; 18 / 100 = 0.18; 0.28 * 0.18 = 0.0504; 7.2 / 0.0504 = 142.857
- DeductReasoner's steps: 18 * 7.2 = 129.6; 129.6 / 100 = 1.296; 1.296 + 7.2 = 8.496; 8.496 * 100 = 849.6; 849.6 / 28 = 30.3429
- same steps as the training program: no
- what went wrong: too many steps

**Test question 2972**: if a and b are positive integers , and a = 5 b + 20 , the greatest common divisor of a and b can not be
- numbers: [5.0, 20.0], reference value 6
- reference steps: 20 / 5 = 4; 4 + 2 = 6
- most similar training question (TF-IDF): if x and y are positive integers , and y = x ^ 2 + 8 , the greatest common divisor of a and b can not be
- its program on the test numbers: 20 + 1 = 21
- DeductReasoner's steps: 1 + 20 = 21
- same steps as the training program: yes
- what went wrong: too few steps

