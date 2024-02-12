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
int total_idle;
int total_forward;
int total_upward;
int RUNS = 1000;
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
  total_idle = 0;
  total_forward = 0;
  total_upward = 0;
}

void loop() {
  float x, y, z;
  float rx, ry, rz;
  int count_stationary_linear = 0;
  int count_stationary_rotation = 0;
  int count_forward_motion = 0;
  int count_upward_motion = 0;
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable() && count < RUNS) {
    IMU.readAcceleration(x, y, z);
    IMU.readGyroscope(rx, ry, rz);
    if (x < 1.2 && x > - 1.2) {
      count_stationary_linear += 1;
    }
    if (y < 1.2 && y > - 1.2) {
      count_stationary_linear += 1;
    }
    if (z < 1.2 && z > - 1.2) {
      count_stationary_linear += 1;
    }
    if (rx < 20 && rx > - 20) {
      count_stationary_rotation += 1;
    }
    if (ry < 20 && ry > - 20) {
      count_stationary_rotation += 1;
    }
    if (rz < 20 && rz > - 20) {
      count_stationary_rotation += 1;
    }
    if (x > 1.2 || x < -1.2) {
      count_forward_motion += 1;
    }
    if (y > 1.2 || y < -1.2) {
      count_forward_motion += 1;
    }
    if (z > 1.2 || z < -1.2) {
      count_upward_motion += 1;
    }
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
   if (count_stationary_linear >= 2 && count_stationary_rotation == 3) {
      Serial.println("idle");
      total_idle += 1;
   }
   else {
      if (count_forward_motion != 0) {
        if (count_upward_motion != 0) {
          Serial.println("Upward Lift");
          total_upward += 1;
        }
        else {
          Serial.println("Forward Push");
          total_forward += 1;
        }
      }
      Serial.println("Generic Non-Idle");
   }
    count++;
    if (count == RUNS) {
      Serial.print("total idle: ");
      Serial.println(total_idle);
      Serial.print("total forward: ");
      Serial.println(total_forward);
      Serial.print("total upward: ");
      Serial.println(total_upward);
      int non_stationary = count - total_idle - total_forward - total_upward;
      Serial.print("total generic non-idle: ");
      Serial.println(non_stationary);
    }
  }

}
