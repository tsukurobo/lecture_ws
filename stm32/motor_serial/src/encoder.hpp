#pragma once
#include <Arduino.h>

class STM32Encoder {
public:
  STM32Encoder(TIM_TypeDef *instance, uint32_t pinA, uint32_t pinB);
  ~STM32Encoder();

  void begin();
  int16_t getCount();
  void reset();

private:
  TIM_TypeDef *_instance;
  uint32_t _pinA;
  uint32_t _pinB;
  HardwareTimer *_timer;
};
