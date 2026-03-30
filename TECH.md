# TECH

## QUESTION 1

#### 1.ERC is planning to introduce a fun weekend project where participants build an
interactive microcontroller-based gadget or game on their own. Think beyond basic
circuits—this could be something like a Flappy Bird-style game, a reaction timer
challenge, a memory game, or any engaging system using a microcontroller along with
simple peripherals such as LEDs, buttons, buzzers, displays, or sensors etc. Your design
should be easy to assemble, intuitive for beginners, and exciting to use, while staying
within a budget of 1k per kit. (Don’t restrict yourself to the given example think out of
the box)

#### 
## ANSWER1

### What is the game?
WHACK-A-LED !!!
#### it would be a fun interactive reaction based game -
whack-a-LED is a reaction based game. six LEDs are placed on a breadboard, each with a button below it. a random LED lights up and you have to press the button below it as fast as you can. score a point for every correct hit, but lose a life if you press the wrong button or react too slowly. you get three lives, and the game gets faster with every point you score. your final score and best reaction time are shown on the LCD when the game ends.

##BILL

### Sr Number || name of component || total units required || price 
1 || Arduino UNO R3 with cable || 1 || INR 494.01
2 || LCD1602 (11C/12C) || 1 || INR 177
3 || Push Buttons || 6 || INR 32.88  ( A kit of 25 would cost 137 INR )
4 || breadboard || 1 || INR 36
5 || passive buzzer || 1 || INR 23
6 || LED's || 6 || INR 12.7 approx ( a kit of hundred would cost 209 INR )

 ## TOTAL COST= INR 775.59
 <img width="992" height="808" alt="image" src="https://github.com/user-attachments/assets/47a69030-f39e-4897-9687-0d057590baff" />

source : https://robu.in/

### why the passive buzzer?

#### we are using the passive buzzer over the active buzzer primarily because of two reasons 
1)Can play different frequencies/notes — essential for a piano
2)Can produce musical notes (Do, Re, Mi... / C, D, E, F, G, A, B)-  ARDUINO'S IDE has the tone() function which helps produce different sounds 

### why the arduino UNO R3 ?

#### we are preferring the arduino UNO R3 over other sensors because-
1)The UNO R3 fully supports Arduino's built-in tone() function ( the leonardo chip supports partial tone function )
-This function generates PWM signals at specific frequencies,exactly what a passive buzzer needs to play different notes represneting a different LED
2) having enough digital pins (We would be needing 6 pins for the led connections and 6 pins for push button connections , UNOR3 having 14 digi pins solves this problem unlike Nano which is smaller)
3) Affordable , easy available and beginner friendly ( arduino mega is just overkill )
UNO R3 aint the only option but its perfect for beginners.



