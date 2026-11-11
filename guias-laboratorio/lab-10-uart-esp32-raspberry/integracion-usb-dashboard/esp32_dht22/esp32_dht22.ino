/*
  Módulo DHT22 compatible 3,3 V, con pull-up integrado.
  VCC→3V3, GND→GND, DATA→GPIO4 del ESP32-S3 (verificar pinout).
  Bibliotecas: DHT sensor library by Adafruit y Adafruit Unified Sensor.
  Seleccionar el USB/puerto adecuado en Arduino IDE; leer la guía.
*/
#include <Arduino.h>
#include <DHT.h>

constexpr uint8_t PIN_DHT = 4;
constexpr uint32_t INTERVALO_MS = 3000;  // DHT22: no leer más rápido que cada 2 s
constexpr bool PROBAR_TRAMA_INVALIDA = false;  // Activar solo para prueba identificada
const char *NODO = "esp32-01";
DHT dht(PIN_DHT, DHT22);
uint32_t ultimaLectura = 0;
uint32_t secuencia = 0;

void setup() {
  Serial.begin(115200);
  const uint32_t inicio = millis();
  while (!Serial && millis() - inicio < 3000) {
    delay(10);  // No bloquear para siempre si no hay monitor
  }
  dht.begin();
  ultimaLectura = millis();
}

void loop() {
  const uint32_t ahora = millis();
  if (ahora - ultimaLectura < INTERVALO_MS) {
    delay(1);
    return;
  }
  ultimaLectura = ahora;
  const float temperatura = dht.readTemperature();
  const float humedad = dht.readHumidity();
  secuencia++;

  if (PROBAR_TRAMA_INVALIDA && secuencia == 2) {
    Serial.println("{\"valor\":\"dato_invalido\"}");
    return;  // La siguiente lectura vuelve a la ruta normal
  }

  if (isnan(temperatura) || isnan(humedad)) {
    Serial.printf(
      "{\"nodo\":\"%s\",\"variable\":\"temperatura\",\"valor\":null,"
      "\"unidad\":\"C\",\"secuencia\":%lu,\"estado\":\"ERROR\","
      "\"detalle\":\"No se pudo leer el DHT22\"}\n",
      NODO, (unsigned long)secuencia
    );
    return;
  }

  // Un JSON por línea; evitar otros Serial.print de texto en este puerto.
  Serial.printf(
    "{\"nodo\":\"%s\",\"variable\":\"temperatura\",\"valor\":%.2f,"
    "\"unidad\":\"C\",\"secuencia\":%lu,\"estado\":\"OK\","
    "\"humedad_pct\":%.2f}\n",
    NODO, temperatura, (unsigned long)secuencia, humedad
  );
}
