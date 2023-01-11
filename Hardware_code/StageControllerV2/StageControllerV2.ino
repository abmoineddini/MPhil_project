const int en=4;         //Enable Pin
const int stp=5;        // Step Pin
const int dir=7;        // Direction
const int pos=3;       // Sensor Position
const int enLED=13;     // On Board LED
int Homming = 0;        // Check if the stage is homed
int angleTest = 0;  
int posVal;             // Homming Sensor Reading
int posCurr;            // Current Position
int steps;              // Number of Steps to trun
int angleToRotate;      // Angle 
volatile int delayTime;


void setup() {
  // Seeting up 
  Serial.begin(9600);
  pinMode(en, OUTPUT);
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(pos, INPUT);
  pinMode(enLED, OUTPUT);
  digitalWrite(en, LOW);
  digitalWrite(enLED, HIGH);
  attachInterrupt(digitalPinToInterrupt(interruptPin), Calibration, CHANGE);
  HomeStage()
}

void loop() {
  
  

}

int HomeStage(){
  
}
