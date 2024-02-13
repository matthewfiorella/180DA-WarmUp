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
int total_circular;
int RUNS = 1000;
int WINDOW_SIZE = 5;

float average(float arr[], int len);

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
  int count_forward_motion = 0;
  int count_upward_motion = 0;
  float windowX[WINDOW_SIZE], windowY[WINDOW_SIZE], windowZ[WINDOW_SIZE];
  float windowRx[WINDOW_SIZE], windowRy[WINDOW_SIZE], windowRz[WINDOW_SIZE];
  int i = 0;
  while (count < RUNS) {
    if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable() && i < WINDOW_SIZE) {
      IMU.readAcceleration(x, y, z);
      IMU.readGyroscope(rx, ry, rz);
      float squared_accel = pow(x,2) + pow(y,2) + pow(z,2);
      if (x > 1.2 || x < -1.2 || rz > 20 || rz < -20) {
        count_forward_motion += 1;
      }
      if (y > 1.2 || y < -1.2 || rz > 20 || rz < -20) {
        count_forward_motion += 1;
      }
      if (z > 1.2 || z < -1.2) {
        count_upward_motion += 1;
      }
      windowX[i] = x;
      windowY[i] = y;
      windowZ[i] = z;
      windowRx[i] = rx;
      windowRy[i] = ry;
      windowRz[i] = rz;
      /*
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
      */
      i++;
    }
    else if (i == WINDOW_SIZE) {
      float avg_x = average(windowX, WINDOW_SIZE);
      float avg_y = average(windowY, WINDOW_SIZE);
      float avg_z = average(windowZ, WINDOW_SIZE);
      float avg_rx = average(windowRx, WINDOW_SIZE);
      float avg_ry = average(windowRy, WINDOW_SIZE);
      float avg_rz = average(windowRz, WINDOW_SIZE);
      Serial.print(avg_x);
      Serial.print("\t");
      Serial.print(avg_y);
      Serial.print("\t");
      Serial.print(avg_z);
      Serial.println("\t");

      float squared_accel = pow(avg_x, 2) + pow(avg_y, 2) + pow(avg_z, 2);
      float x_y_accel = pow(avg_x, 2) + pow(avg_y, 2);
      float z_accel = pow(avg_z, 2);
      float angular_vel = 0;
      // Check if Idle
      if (squared_accel < 1.2) {
          Serial.println("idle");
          total_idle += 1;
      }
      // Not Idle
      else {
          // Forward Push?
          if (x_y_accel >= 0.8) {
            Serial.println("Forward Push");
            total_forward += 1;
          }
          else {
            // Upward?
            if (z_accel >= 0.8) {
              Serial.println("Upward Lift");
              total_upward += 1;
            }
            else {
              if (avg_rx >= 100 || avg_ry >= 100 || avg_rx <= -100 || avg_ry <= -100) {
                Serial.println("circular motion");
                total_circular += 1;
              }
            }
          }
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
      i = 0;
    }
  }

}

float average(float x[], int len) {
  float sum = 0;
  for(int i = 0; i < len; i++) {
    sum += x[i];
  }
  return sum / len;
}