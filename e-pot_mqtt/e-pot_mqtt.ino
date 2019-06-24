#include <WiFi101.h>
#include <PubSubClient.h>

#define CT_SENSOR_PIN A5
#define LED_PIN 14

//WiFi
char ssid[] = "*****";
char pass[] = "*******";

//MQTT
char host[] = "172.29.156.107";
char topic[] = "****/e-pot";
int port = 1883;

//Flag
boolean is_turn_off = true;

WiFiClient wificlient;
PubSubClient mqttClient(wificlient);

inline int getCurrentlymA() {
  int observed_value;
  int max_val = 0;
  int min_val = 32767;

  for (int i = 0; i < 1000; i++) {
    observed_value = analogRead(CT_SENSOR_PIN);
    if (max_val < observed_value) max_val = observed_value;
    if (min_val > observed_value) min_val = observed_value;
  }
  observed_value = max_val;

  return observed_value * 103.889627659574;
}

void setup() {
  Serial.begin(9600);
  
  // connect WiFi
  connectWiFi();

  //connect MQTT
  connectMqtt();
  mqttClient.publish(topic, "e-pot.connected");
  Serial.println("connected");

  pinMode(LED_PIN, OUTPUT);
}

void loop() {

  if ( WiFi.status() == WL_CONNECTED) connectWiFi();
  if ( !mqttClient.connected()) connectMqtt();

  Serial.println(getCurrentlymA());

  // put your main code here, to run repeatedly:
  if (getCurrentlymA() > 15000 && is_turn_off) {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("on");
    mqttClient.publish(topic, "{'electric_pot':'on'}");
    is_turn_off = false;
    delay(1200);
    digitalWrite(LED_BUILTIN, LOW);
  }
  else if (getCurrentlymA() < 10000 && !is_turn_off) {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("off");
    mqttClient.publish(topic, "{'electric_pot':'off'}");
    is_turn_off = true;
    delay(1200);
    digitalWrite(LED_BUILTIN, LOW);
  }

   mqttClient.loop();  
}


void connectWiFi(){
  while ( WiFi.status() != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    WiFi.begin(ssid, pass);
    // wait 10 seconds for connection:
    delay(10000);
  }
  Serial.print(" connected. ");
}

void connectMqtt(){
  mqttClient.setServer(host, port);
  while( ! mqttClient.connected() ) {
    Serial.println("Connecting to MQTT...");
    if ( mqttClient.connect(topic) ) {
      Serial.println("connected"); 
    }
    delay(1000);
    randomSeed(micros());
  }
}
