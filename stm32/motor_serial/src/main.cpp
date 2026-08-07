#include <Arduino.h>
#include <CytronMotorDriver.h>

// CytronMD(制御方式, PWMピン, DIRピン)
CytronMD motor1(PWM_DIR, 5, 6);
CytronMD motor2(PWM_DIR, 9, 10);

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    // ROSから「モータ1,モータ2\n」の形式で受信
    String data = Serial.readStringUntil('\n');

    // コンマの位置を探して、2つの値に分ける
    int commaPosition = data.indexOf(',');
    int motor1Speed = data.substring(0, commaPosition).toInt();
    int motor2Speed = data.substring(commaPosition + 1).toInt();

    // -255～255の値でモータを回す
    motor1.setSpeed(motor1Speed);
    motor2.setSpeed(motor2Speed);

    Serial.print("Motor 1 Speed: ");
    Serial.print(motor1Speed);
    Serial.print(", Motor 2 Speed: ");
    Serial.println(motor2Speed);
  }
}
