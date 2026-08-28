/*
 * Agri Gram AI - IoT Sensor Node (Wokwi Simulation)
 * ESP32 + DHT22 (temp/humidity) + Soil Moisture Sensor
 * Sends data to Agri Gram AI backend every 10 seconds.
 * Author: Abinaya K
 *
 * WOKWI SETUP:
 *   - ESP32 board
 *   - DHT22 sensor: VCC->3V3, GND->GND, DATA->GPIO 15
 *   - Soil Moisture (analog): VCC->3V3, GND->GND, AO->GPIO 34
 *   - Use Wokwi built-in WiFi ("Wokwi-GUEST", no password)
 *
 * NOTE: For Wokwi to reach your backend, host it publicly
 * (ngrok / Render) and paste that URL below.
 * For local demo, this code prints data to Serial Monitor.
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

#define DHTPIN 15
#define DHTTYPE DHT22
#define SOIL_PIN 34

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "Wokwi-GUEST";
const char* password=[REDACTED_PASSWORD]

// Backend URL - replace with your Render URL or ngrok URL
const char* serverURL = "http://YOUR_BACKEND_URL/api/iot/push";

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(SOIL_PIN, INPUT);

  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int soilRaw = analogRead(SOIL_PIN);
  float soilMoisture = map(soilRaw, 4095, 0, 0, 100); // invert: dry=high ADC

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read DHT sensor!");
    delay(2000);
    return;
  }

  // Build JSON
  String payload = "{";
  payload += "\"device\":\"ESP32-01\",";
  payload += "\"temperature\":" + String(temperature, 1) + ",";
  payload += "\"humidity\":" + String(humidity, 1) + ",";
  payload += "\"soil_moisture\":" + String(soilMoisture, 1);
  payload += "}";

  Serial.println("Sending: " + payload);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");
    int code = http.POST(payload);
    if (code > 0) {
      Serial.printf("Response: %d\n", code);
    } else {
      Serial.printf("Error: %s\n", http.errorToString(code).c_str());
    }
    http.end();
  }

  delay(10000); // send every 10 seconds
}
