#include <Arduino.h>

#define OTUKA
// #define HONMA

#ifdef OTUKA
    #define ENCODER_CH1_TIM TIM1
    #define ENCODER_CH2_TIM TIM2
    #define ENCODER_CH3_TIM TIM3
    #define ENCODER_CH4_TIM TIM4

    #define DIR_CH1 PC0
    #define DIR_CH2 PC1
    #define DIR_CH3 PC2
    #define DIR_CH4 PC3
    #define ENCODER_CH1A PA8
    #define ENCODER_CH1B PA9
    #define ENCODER_CH2A PA0
    #define ENCODER_CH2B PA1
    #define ENCODER_CH3A PA6
    #define ENCODER_CH3B PA7_ALT1
    #define ENCODER_CH4A PB6
    #define ENCODER_CH4B PB7
    #define LED1 PB12
    #define LED2 PB13
    #define LED3 PB14
    #define LED4 PB15
    #define PWM_CH1 PC6
    #define PWM_CH2 PC7
    #define PWM_CH3 PC8
    #define PWM_CH4 PC9
    #define SW1 PB0
    #define SW2 PB1
    #define SW3 PB2
    #define SWO PB3
    #define TCK PA14
    #define TMS PA13
    #define USART_RX PA3
    #define USART_TX PA2
#endif

#ifdef HONMA
    #define ENCODER_CH1_TIM TIM1
    #define ENCODER_CH2_TIM TIM2
    #define ENCODER_CH3_TIM TIM3
    #define ENCODER_CH4_TIM TIM4

    #define DIR_CH1 PC0
    #define DIR_CH2 PC1
    #define DIR_CH3 PC2
    #define DIR_CH4 PC3
    #define ENCODER_CH1A PA8
    #define ENCODER_CH1B PA9
    #define ENCODER_CH2A PA0
    #define ENCODER_CH2B PA1
    #define ENCODER_CH3A PA6
    #define ENCODER_CH3B PA7_ALT1
    #define ENCODER_CH4A PB6
    #define ENCODER_CH4B PB7
    #define LED1 PB12
    #define LED2 PB13
    #define LED3 PB14
    #define LED4 PB15
    #define PWM_CH1 PC6
    #define PWM_CH2 PC7
    #define PWM_CH3 PC8
    #define PWM_CH4 PC9
    #define SW1 PB0
    #define SW2 PB1
    #define SW3 PB2
    #define SWO PB3
    #define TCK PA14
    #define TMS PA13
    #define USART_RX PA3
    #define USART_TX PA2
#endif
