#include <Arduino.h>
#include <CytronMotorDriver.h>

// CytronMD(制御方式, PWMピン, DIRピン)
CytronMD leftMotor(PWM_DIR, 5, 6);
CytronMD rightMotor(PWM_DIR, 9, 10);

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    // ROSから「左モータ,右モータ\n」の形式で受信
    String data = Serial.readStringUntil('\n');

    // コンマの位置を探して、左右の値に分ける
    int commaPosition = data.indexOf(',');
    int leftSpeed = data.substring(0, commaPosition).toInt();
    int rightSpeed = data.substring(commaPosition + 1).toInt();

    // -255～255の値でモータを回す
    leftMotor.setSpeed(leftSpeed);
    rightMotor.setSpeed(rightSpeed);

    Serial.print("Left Motor Speed: ");
    Serial.print(leftSpeed);
    Serial.print(", Right Motor Speed: ");
    Serial.println(rightSpeed);
  }
}
