#include <Arduino.h>
#include <time.h>

const int triggerPin = 7;
const int echoPin = 8;    

long duration;
float distance;

unsigned long lastMillis;


void setup() {
    pinMode(triggerPin, OUTPUT);
    pinMode(echoPin, INPUT);
    lastMillis = 0;
    Serial.begin(9600);
    Serial.println("time,cm");
}

void loop() {
    unsigned long currentMillis = millis();

    if(currentMillis - lastMillis >= 20) {
        lastMillis = currentMillis;

        digitalWrite(triggerPin, LOW);
        delayMicroseconds(2);

        digitalWrite(triggerPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(triggerPin, LOW);
        
        duration = pulseIn(echoPin, HIGH, 9000);
        distance = duration * 0.0343/2;
        if(distance == 0) {
            distance = 200;
        }

        Serial.print(currentMillis);
        Serial.print(", ");
        Serial.println(distance, 4);
    }
}
