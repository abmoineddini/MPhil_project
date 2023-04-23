
void setup() {
  // put your setup code here, to run once:
  Serial.begin(2000000);
  pinMode(A5, INPUT);
  pinMode(A8, INPUT);
  pinMode(A12, INPUT);
  pinMode(A14, INPUT);  

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print(analogRead(A5));
  Serial.print(",");
  Serial.print(analogRead(A8));
  Serial.print(",");
  Serial.print(analogRead(A12));
  Serial.print(",");
  Serial.println(analogRead(A12));

}
