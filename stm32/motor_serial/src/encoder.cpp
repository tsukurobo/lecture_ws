#include "encoder.hpp"

STM32Encoder::STM32Encoder(TIM_TypeDef *instance, uint32_t pinA, uint32_t pinB)
    : _instance(instance), _pinA(pinA), _pinB(pinB), _timer(nullptr) {}

STM32Encoder::~STM32Encoder() {
  if (_timer != nullptr) {
    delete _timer;
  }
}

void STM32Encoder::begin() {
  _timer = new HardwareTimer(_instance);
  _timer->setMode(1, TIMER_INPUT_CAPTURE_BOTHEDGE, _pinA);
  _timer->setMode(2, TIMER_INPUT_CAPTURE_BOTHEDGE, _pinB);

  TIM_HandleTypeDef *htim = _timer->getHandle();

  TIM_Encoder_InitTypeDef sConfig = {0};
  sConfig.EncoderMode = TIM_ENCODERMODE_TI12;
  sConfig.IC1Polarity = TIM_ICPOLARITY_RISING;
  sConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
  sConfig.IC1Prescaler = TIM_ICPSC_DIV1;
  sConfig.IC1Filter = 0;
  sConfig.IC2Polarity = TIM_ICPOLARITY_RISING;
  sConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
  sConfig.IC2Prescaler = TIM_ICPSC_DIV1;
  sConfig.IC2Filter = 0;

  HAL_TIM_Encoder_Init(htim, &sConfig);
  HAL_TIM_Encoder_Start(htim, TIM_CHANNEL_ALL);
}

int16_t STM32Encoder::getCount() {
  if (_timer == nullptr) {
    return 0;
  }
  return (int16_t)_timer->getCount();
}

void STM32Encoder::reset() {
  if (_timer != nullptr) {
    _timer->setCount(0);
  }
}
