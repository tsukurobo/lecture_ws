#include <Arduino.h>
#include "Adafruit_VL53L0X.h"

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

void setup() {
  Serial.begin(115200);

  while (!Serial) {
    delay(1);
  }

  if (!lox.begin()) {
    while (1) {
      delay(10);
    }
  }
}

void loop() {
  VL53L0X_RangingMeasurementData_t measure;

  lox.rangingTest(&measure, false);

  if (measure.RangeStatus != 4) {
    Serial.println(measure.RangeMilliMeter);
  }

  delay(100);
}
