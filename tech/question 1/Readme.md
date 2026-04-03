# TECH

## QUESTION 1

1.ERC is planning to introduce a fun weekend project where participants build an
interactive microcontroller-based gadget or game on their own. Think beyond basic
circuits—this could be something like a Flappy Bird-style game, a reaction timer
challenge, a memory game, or any engaging system using a microcontroller along with
simple peripherals such as LEDs, buttons, buzzers, displays, or sensors etc. Your design
should be easy to assemble, intuitive for beginners, and exciting to use, while staying
within a budget of 1k per kit. (Don’t restrict yourself to the given example think out of
the box)

#### 
## ANSWER 1

### What is the game?
WHACK-A-LED !!!
#### it would be a fun interactive reaction based game -
whack-a-LED is a reaction based game. six LEDs are placed on a breadboard, each with a button below it. a random LED lights up and you have to press the button below it as fast as you can. score a point for every correct hit, but lose a life if you press the wrong button or react too slowly. you get three lives, and the game gets faster with every point you score. your final score and best reaction time are shown on the LCD when the game ends.

## BILL

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

<img width="1132" height="542" alt="image" src="https://github.com/user-attachments/assets/fd91000e-f86e-4429-b39b-158047c50e93" />

### simulated the game in tinkercad 

## CODE 
```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ── Pin definitions ──────────────────────────────────────────────
const int LED_PINS[6]    = {2, 3, 4, 5, 6, 7};
const int BTN_PINS[6]    = {8, 9, 10, 11, 12, 13};
const int BUZZER_PIN     = A0;

// ── LCD (I2C address 0x27, 16 cols, 2 rows) ──────────────────────
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ── Game config ───────────────────────────────────────────────────
const int   MAX_LIVES        = 3;
const long  START_WINDOW_MS  = 1500;   // ms to react at level 1
const long  MIN_WINDOW_MS    = 400;    // fastest allowed window
const long  SPEED_STEP_MS    = 50;     // window shrinks by this each point

// ── Game state ────────────────────────────────────────────────────
int   score          = 0;
int   lives          = MAX_LIVES;
long  windowMs       = START_WINDOW_MS;
long  bestTimeMs     = 99999;
int   activeLED      = -1;
long  ledOnTime      = 0;
bool  waitingForHit  = false;
bool  gameOver       = false;

// ── Helper: tone shortcuts ────────────────────────────────────────
void beepOK()   { tone(BUZZER_PIN, 1200, 80);  }
void beepFail() { tone(BUZZER_PIN, 200,  300); }
void beepStart(){ 
  tone(BUZZER_PIN, 880, 100); delay(120);
  tone(BUZZER_PIN, 1100, 100); delay(120);
  tone(BUZZER_PIN, 1400, 150);
}

// ── Turn all LEDs off ─────────────────────────────────────────────
void allLedsOff() {
  for (int i = 0; i < 6; i++) digitalWrite(LED_PINS[i], LOW);
}

// ── Show score + lives on LCD ─────────────────────────────────────
void updateLCD() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Score:");
  lcd.print(score);
  lcd.setCursor(9, 0);
  lcd.print("Lives:");
  lcd.print(lives);
  lcd.setCursor(0, 1);
  lcd.print("Best:");
  if (bestTimeMs == 99999) lcd.print("--");
  else { lcd.print(bestTimeMs); lcd.print("ms"); }
}

// ── Light a random LED and start the reaction window ─────────────
void lightRandomLED() {
  activeLED   = random(0, 6);
  ledOnTime   = millis();
  waitingForHit = true;
  digitalWrite(LED_PINS[activeLED], HIGH);
}

// ── Handle a miss (timeout or wrong button) ───────────────────────
void handleMiss() {
  allLedsOff();
  waitingForHit = false;
  lives--;
  beepFail();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("  MISS! ");
  lcd.print(lives);
  lcd.print(" lives");
  delay(800);
  if (lives <= 0) {
    gameOver = true;
  } else {
    updateLCD();
    delay(random(600, 1400));   // unpredictable gap before next LED
    lightRandomLED();
  }
}

// ── Handle a correct hit ──────────────────────────────────────────
void handleHit(long reactionMs) {
  allLedsOff();
  waitingForHit = false;
  score++;
  if (reactionMs < bestTimeMs) bestTimeMs = reactionMs;

  // Shrink the reaction window as score goes up
  windowMs = max(MIN_WINDOW_MS, START_WINDOW_MS - (long)score * SPEED_STEP_MS);

  beepOK();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("  HIT! ");
  lcd.print(reactionMs);
  lcd.print("ms");
  lcd.setCursor(0, 1);
  lcd.print("Score: ");
  lcd.print(score);
  delay(600);
  updateLCD();
  delay(random(500, 1200));
  lightRandomLED();
}

// ── Game-over screen ──────────────────────────────────────────────
void showGameOver() {
  allLedsOff();
  // Sad descending tones
  tone(BUZZER_PIN, 600, 200); delay(250);
  tone(BUZZER_PIN, 400, 200); delay(250);
  tone(BUZZER_PIN, 200, 400); delay(500);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("  GAME OVER!");
  lcd.setCursor(0, 1);
  lcd.print("Score:");
  lcd.print(score);
  lcd.print(" Best:");
  if (bestTimeMs == 99999) lcd.print("--");
  else { lcd.print(bestTimeMs); lcd.print("ms"); }

  // Flash all LEDs 3 times
  for (int f = 0; f < 3; f++) {
    for (int i = 0; i < 6; i++) digitalWrite(LED_PINS[i], HIGH);
    delay(300);
    allLedsOff();
    delay(300);
  }

  // Wait for any button press to restart
  lcd.setCursor(0, 1);
  lcd.print("Press any btn...");
  bool waiting = true;
  while (waiting) {
    for (int i = 0; i < 6; i++) {
      if (digitalRead(BTN_PINS[i]) == HIGH) { waiting = false; break; }
    }
    delay(50);
  }

  // Reset game
  score     = 0;
  lives     = MAX_LIVES;
  windowMs  = START_WINDOW_MS;
  bestTimeMs= 99999;
  gameOver  = false;

  // Countdown 3-2-1 on LCD
  for (int c = 3; c >= 1; c--) {
    lcd.clear();
    lcd.setCursor(7, 0);
    lcd.print(c);
    tone(BUZZER_PIN, 800, 150);
    delay(700);
  }
  beepStart();
  updateLCD();
  delay(random(600, 1200));
  lightRandomLED();
}

// ─────────────────────────────────────────────────────────────────
void setup() {
  for (int i = 0; i < 6; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    pinMode(BTN_PINS[i], INPUT);    // external 10k pull-down used
  }
  pinMode(BUZZER_PIN, OUTPUT);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(2, 0);
  lcd.print("Whack-a-LED!");
  lcd.setCursor(3, 1);
  lcd.print("Get ready...");

  randomSeed(analogRead(A1));       // floating pin for entropy

  beepStart();
  delay(1500);
  updateLCD();
  delay(random(800, 1600));
  lightRandomLED();
}

void loop() {
  if (gameOver) { showGameOver(); return; }

  if (waitingForHit) {
    long now     = millis();
    long elapsed = now - ledOnTime;

    // Check all buttons
    for (int i = 0; i < 6; i++) {
      if (digitalRead(BTN_PINS[i]) == HIGH) {
        if (i == activeLED) {
          handleHit(elapsed);     // correct button
        } else {
          handleMiss();           // wrong button pressed
        }
        return;
      }
    }

    // Timed out
    if (elapsed >= windowMs) {
      handleMiss();
    }
  }
}
```

# WORKING 

## How the circuit works

The circuit is built around an Arduino Uno which acts as the brain of the entire game. Six LEDs are connected to digital pins D2 through D7, with each LED having a 220 ohm resistor in series to limit the current so the LED does not burn out. Six push buttons are connected to digital pins D8 through D13. Each button uses a 10k ohm pull down resistor connected between the signal pin and GND. This means when the button is not pressed the Arduino reads zero, and when it is pressed 5V flows through and the Arduino reads one. A passive piezo buzzer is connected to pin A0 with its positive leg on the pin and negative leg on GND, which lets the Arduino play different tones for correct hits, wrong presses and game over. The LCD display uses the I2C communication protocol with only two data wires, SDA connected to A4 and SCL connected to A5, along with 5V and GND for power. All GND connections across every component share a common GND rail on the breadboard and similarly all 5V connections share a common 5V rail.

## How the code works 

When the Arduino powers on it initialises the LCD, sets all LED pins as outputs and all button pins as inputs. The game then waits a random amount of time and lights up one randomly chosen LED. A timer starts the moment the LED turns on. The code then continuously checks all six buttons in a loop. If the player presses the button that matches the lit LED before the time window runs out, the code records the reaction time, plays a short high pitched beep, adds one point to the score and displays everything on the LCD. If the player presses the wrong button or does not press anything before the timer runs out, the code plays a low pitched fail sound and removes one life. After every correct hit the time window shrinks by 50 milliseconds making the game progressively faster. When all three lives are lost the game over sequence plays a descending tone, flashes all LEDs three times and displays the final score and best reaction time on the LCD. The player can then press any button to restart the game from the beginning.



