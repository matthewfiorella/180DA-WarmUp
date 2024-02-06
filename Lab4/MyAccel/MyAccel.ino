/*
  Arduino LSM6DS3 - Simple Accelerometer

  This example reads the acceleration values from the LSM6DS3
  sensor and continuously prints them to the Serial Monitor
  or Serial Plotter.

  The circuit:
  - Arduino Uno WiFi Rev 2 or Arduino Nano 33 IoT

  created 10 Jul 2019
  by Riccardo Rizzo

  This example code is in the public domain.
*/

#include <Arduino_LSM6DS3.h>
int count;
void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Acceleration in g's, Angular Velocity in dps");
  Serial.println("X\tY\tZ\trX\trY\tRZ");
  count = 0;
}

void loop() {
  float x, y, z;
  float rx, ry, rz;
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable() && count < 100) {
    IMU.readAcceleration(x, y, z);
    IMU.readGyroscope(rx, ry, rz);
    Serial.print(x);
    Serial.print('\t');
    Serial.print(y);
    Serial.print('\t');
    Serial.print(z);
    Serial.print('\t');
    Serial.print(rx);
    Serial.print('\t');
    Serial.print(ry);
    Serial.print('\t');
    Serial.println(rz);
    count++;
  }

}
