#include <Arduino.h>
#include <CytronMotorDriver.h>
#include "pin_def.h"
#include "encoder.hpp"

// CytronMD(制御方式, PWMピン, DIRピン)
CytronMD motor1(PWM_DIR, PWM_CH1, DIR_CH1);
CytronMD motor2(PWM_DIR, PWM_CH2, DIR_CH2);
CytronMD motor3(PWM_DIR, PWM_CH3, DIR_CH3);
CytronMD motor4(PWM_DIR, PWM_CH4, DIR_CH4);
STM32Encoder encoder1(ENCODER_CH1_TIM, ENCODER_CH1A, ENCODER_CH1B);
STM32Encoder encoder2(ENCODER_CH2_TIM, ENCODER_CH2A, ENCODER_CH2B);
STM32Encoder encoder3(ENCODER_CH3_TIM, ENCODER_CH3A, ENCODER_CH3B);
STM32Encoder encoder4(ENCODER_CH4_TIM, ENCODER_CH4A, ENCODER_CH4B);


void setup() {
  Serial.begin(115200);
  // encoder1.begin();
  // encoder2.begin();
  // encoder3.begin();
  // encoder4.begin();
}

void loop() {
  if (Serial.available() > 0) {
    // 改行までデータを読み取る
    String data = Serial.readStringUntil('\n');
    // コンマの位置を探す
    int commaPosition1 = data.indexOf(',');
    int commaPosition2 = data.indexOf(',', commaPosition1+1);
    int commaPosition3 = data.indexOf(',', commaPosition2+1);
    // コンマの前後を整数へ変換する
    //String motor
    int motor1Speed = (data.substring(0, commaPosition1)).toInt();
    int motor2Speed = (data.substring(commaPosition1+1,commaPosition2)).toInt();
    int motor3Speed = (data.substring(commaPosition2+1,commaPosition3)).toInt();
    int motor4Speed = (data.substring(commaPosition3+1)).toInt();
    // 2つのモータへ指令値を渡す
    motor1.setSpeed(motor1Speed);
    motor2.setSpeed(motor2Speed);
    motor3.setSpeed(motor3Speed);
    motor4.setSpeed(motor4Speed);

    //デバック用
    // Serial.print(motor1Speed);
    // Serial.print(",");
    // Serial.print(motor2Speed);
    // Serial.print(",");
    // Serial.print(motor3Speed);
    // Serial.print(",");
    // Serial.println(motor4Speed);

    // int16_t count1 = encoder1.getCount();
    // int16_t count2 = encoder2.getCount();
    // int16_t count3 = encoder3.getCount();
    // int16_t count4 = encoder4.getCount();

    // Serial.print(count1);
    // Serial.print(",");
    // Serial.print(count2);
    // Serial.print(",");
    // Serial.print(count3);
    // Serial.print(",");
    // Serial.println(count4);
  }
}
