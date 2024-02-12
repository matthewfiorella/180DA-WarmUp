#include <ArduinoMqttClient.h>
#include <Arduino_LSM6DS3.h>
#include <WiFiNINA.h>
#include "Wifi_Secret.h"

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char broker[] = "test.mosquitto.org";
int port = 1883;
const char topic[] = "mfio/topic1";
const char topic2[] = "topic2";
const char topic3[] = "topic3";

const long interval = 8000;
unsigned long previousMillis = 0;

int count = 0;

void setup() {
  // Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect
  }

  // attempt to connect to Wifi network:
  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }

  Serial.println("You're connected to the network");
  Serial.println();

  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    while (1);
  }

  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();
}

void loop() {
  // call poll() regularly to allow the library to send MQTT keep alive
  // avoids being disconnected by the broker
  mqttClient.poll();

  unsigned long currentMillis = millis();

  float x, y, z;
  if (IMU.accelerationAvailable() && currentMillis - previousMillis >= interval) {
    // save the last time a message was sent
    previousMillis = currentMillis;
    IMU.readAcceleration(x, y, z);

    Serial.print("Sending message to topic: ");
    Serial.println(topic);
    Serial.println(x);

    Serial.println("Sending message to topic: ");
    Serial.println(topic);
    Serial.println(y);

    Serial.print("Sending message to topic: ");
    Serial.println(topic);
    Serial.println(z);

    // send message, the Print interface can be used to set the message
    mqttClient.beginMessage(topic);
    mqttClient.print("x accel: ");
    mqttClient.print(x);
    mqttClient.endMessage();

    mqttClient.beginMessage(topic);
    mqttClient.print("y accel: ");
    mqttClient.print(y);
    mqttClient.endMessage();

    mqttClient.beginMessage(topic);
    mqttClient.print("z accel: ");
    mqttClient.print(z);
    mqttClient.endMessage();

    Serial.println();
  }

}
