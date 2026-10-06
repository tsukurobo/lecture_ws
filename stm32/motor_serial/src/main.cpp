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
    // TODO
    // 改行までデータを読み取る
    String data = Serial.________________________;

    // TODO
    // コンマの位置を探す
    int commaPosition = data.________________________;

    // TODO
    // コンマの前後を整数へ変換する
    int motor1Speed = ________________________________;
    int motor2Speed = ________________________________;

    // TODO
    // 2つのモータへ指令値を渡す
    _________________________________________________;
    _________________________________________________;
  }
}
