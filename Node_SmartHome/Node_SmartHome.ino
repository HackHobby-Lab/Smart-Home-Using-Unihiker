
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <WiFiClientSecure.h>
#include <WiFiUdp.h>
#include <PubSubClient.h>
#include "DHT.h"
// WiFi
const char* ssid = "Hackhobby_Lab";                
const char* wifi_password = "80601002";
// MQTT
const char* mqtt_server = "192.168.X.XX"; 
const char* one_topic = "esp pub topic"; //Topic name
const char* mqtt_username = "ali"; // MQTT username
const char* mqtt_password = "786"; // MQTT password
const char* clientID = "Esp8266Client"; // MQTT client ID
const char* two_topic = "esp sub topic"; // Second Topic name

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
// 1884 is the listener port for the Broker
PubSubClient client(mqtt_server, 1884, wifiClient);


//Pin Defination
#define DHTPIN D2
int Out1 = D4;
int Out2 = D5;
int Out3 = D1;
//Debuging
int counter = 0;

#define DHTTYPE DHT11 
DHT dht(DHTPIN, DHTTYPE); 
// function to connect to mqtt broker
void connect_MQTT(){
 
  client.setCallback(callback);
  // Connect to MQTT Broker
  if (client.connect(clientID, mqtt_username, mqtt_password)) {
    //Serial.println("Connected to MQTT Broker!");
    if(client.subscribe(two_topic)){
      //Serial.println("subscribed");
    }
    else{
      Serial.println("Subscription Failed");
    }
  }
  else {
    Serial.println("Connection to MQTT Broker failed…");
  }
}

void setup() {

   pinMode(Out1, OUTPUT);
   pinMode(Out2, OUTPUT);
   pinMode(Out3, OUTPUT);
   
   Serial.begin(9600);
   dht.begin();
   Serial.print("Connecting to ");
   Serial.println(ssid);

    // Connect to the WiFi
   WiFi.begin(ssid, wifi_password);

      // Wait until the connection is confirmed
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
      }

    // Debugging
    Serial.println("Wifi Connected");
    Serial.print("Ip address: ");
    Serial.println(WiFi.localIP());
    

}
 
void loop() {

  connect_MQTT();
  Serial.setTimeout(2000);
  client.loop();

  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  int t = dht.readTemperature();
  Serial.print(F("Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));

  //counter++;
  if (client.publish(one_topic, String(t).c_str())) {
    //Serial.println("Sent the text");
    //Serial.println(counter);
  }
  else {
    Serial.println("Failed to send the text. Attempting to reconnect....");
    client.connect(clientID, mqtt_username, mqtt_password);
    delay(10); 
    client.publish(one_topic, String("Again!").c_str());
  }
    delay(100);

  //client.disconnect();  // disconnect from the MQTT broker
}

void callback(char* two_topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(two_topic);
  
  Serial.print("Message: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  //Statement comparison and State declaration for outputs
  // Checking if received data has our expected values
  if (strstr((char*)payload, "B1N") != NULL) {
    Serial.println("OUT1 On");
    //client.publish(one_topic, String("1000").c_str());
    digitalWrite(Out1, HIGH);

  }
  else { Serial.println("------------");} //this is not necessary but makes debugging easier
// Checking if received data has our expected values
  if (strstr((char*)payload, "B1F") != NULL) {
    Serial.println("OUT1 OFF");
    digitalWrite(Out1, LOW);
  }



  //Statement comparison and State declaration for outputs
  // Checking if received data has our expected values
  if (strstr((char*)payload, "B2N") != NULL) {
    Serial.println("OUT2 On");
    //client.publish(one_topic, String("1000").c_str());
    digitalWrite(Out2, HIGH);

  }
  else { Serial.println("------------");} //this is not necessary but makes debugging easier
// Checking if received data has our expected values
  if (strstr((char*)payload, "B2F") != NULL) {
    Serial.println("OUT2 OFF");
    digitalWrite(Out2, LOW);
  }



  //Statement comparison and State declaration for outputs
  // Checking if received data has our expected values
  if (strstr((char*)payload, "B3N") != NULL) {
    Serial.println(" OUT3 On");
    //client.publish(one_topic, String("1000").c_str());
    digitalWrite(Out3, HIGH);

  }
  else { Serial.println("------------");} //this is not necessary but makes debugging easier
// Checking if received data has our expected values
  if (strstr((char*)payload, "B3F") != NULL) {
    Serial.println("OUT3 OFF");
    digitalWrite(Out3, LOW);
  }
}