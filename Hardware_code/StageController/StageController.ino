const int en=11;
const int stp=5;
const int dir=7;
const int pos=3;
const int enLED=13;
int Homming = 0;
int angleTest = 0;
int posVal;
int ptn;
//int val=0;
int steps;
int angleToRotate;
volatile int delayTime;


void setup() {
  Serial.begin(9600);
  pinMode(en, OUTPUT);
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(pos, INPUT);
  pinMode(enLED, OUTPUT);
  digitalWrite(en, LOW);
  digitalWrite(enLED, HIGH);
}

void loop() {
  if (Homming == 0){
    posVal= digitalRead(pos);
    Serial.println(posVal);
    if (posVal==1){
      digitalWrite(dir, HIGH);
      for(int i =0; i<=1000;i++){
        digitalWrite(stp, HIGH);
        delayMicroseconds(900);
        digitalWrite(stp, LOW);
        delayMicroseconds(900);
      }
    }
    if (posVal==0 && Homming==0){
      digitalWrite(dir, LOW);
      while(posVal == 0){
        digitalWrite(stp, HIGH);
        delayMicroseconds(1000);
        digitalWrite(stp, LOW);
        delayMicroseconds(1000);
        posVal= digitalRead(pos);
      }
      digitalWrite(dir, LOW);
      for(int i =0; i<=410;i++){
      digitalWrite(stp, HIGH);
      delayMicroseconds(1200);
      digitalWrite(stp, LOW);
      delayMicroseconds(1200);
      }
      Homming=1;
      Serial.println("Loop 2");
      ptn = 0;
      delay(5000);
      }
    } 
  else{
    Serial.println("ready");
    String Conn = Serial.readString();
    if (Conn == "rdy"){
      Serial.println("Starting");
      while(true){
          String val = Serial.readString();
          Serial.println(val);
          int valInt = int(val.toInt());
          
          if (valInt>0 && valInt<=360){
            if (valInt!=ptn){
              angleToRotate = (valInt-ptn);
              ptn = valInt;
            }
             else{
              angleToRotate = 0;
            }            
            if (angleToRotate>180){
              angleToRotate = angleToRotate-360;
            }
            if (angleToRotate<-180){
              angleToRotate = 360+angleToRotate;
            }
            steps = angleToRotate*50;
            if (angleToRotate>0){
              digitalWrite(dir, LOW);
              for(int i =0; i<=steps;i++){
                digitalWrite(stp, HIGH);
                delayMicroseconds(900);
                digitalWrite(stp, LOW);
                delayMicroseconds(900);
              }
            }
            if (angleToRotate<0){
              digitalWrite(dir, HIGH);
              for(int i =0; i<=abs(steps);i++){
                digitalWrite(stp, HIGH);
                delayMicroseconds(900);
                digitalWrite(stp, LOW);
                delayMicroseconds(900);
              }
            }
            
            delayTime = abs(angleToRotate)*10;
            delay(delayTime);
            
            Serial.println("done");
            if (ptn==360){
              ptn=0;
            }
            Serial.println(ptn);
            
          }
          if (valInt<0 && valInt>=-360){
            valInt = 360 + valInt;
            if (valInt!=ptn){
              angleToRotate = 360-(valInt-ptn);
              ptn = valInt;
            }
             else{
              angleToRotate = 0;
            }
            if (angleToRotate>360){
              angleToRotate = -720+angleToRotate;
            }
            
            if (angleToRotate>180){
              angleToRotate = angleToRotate-360;
            }
            if (angleToRotate<-180){
              angleToRotate = 360+angleToRotate;
            }
            steps = angleToRotate*50;
            if (angleToRotate>0){
              digitalWrite(dir, HIGH);
              for(int i =0; i<=abs(steps);i++){
                digitalWrite(stp, HIGH);
                delayMicroseconds(900);
                digitalWrite(stp, LOW);
                delayMicroseconds(900);
              }
            }
            if (angleToRotate<0){
              digitalWrite(dir, LOW);
              for(int i =0; i<=abs(steps);i++){
                digitalWrite(stp, HIGH);
                delayMicroseconds(900);
                digitalWrite(stp, LOW);
                delayMicroseconds(900);
              }
            }
            delayTime = abs(angleToRotate)*10;
            delay(delayTime);
            
            Serial.println("done");
//            if (ptn==360){
//              ptn=0;
//            }
            Serial.println(ptn);
          }
        }
      }
   }
  }
