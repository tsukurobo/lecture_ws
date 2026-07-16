#include <Arduino.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

int n = 0;

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(n);
  n++;
  
  // 遅延
  delay(1000);
}