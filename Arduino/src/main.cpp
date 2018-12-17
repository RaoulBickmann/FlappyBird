#include <Arduino.h>
#include <time.h>

const int triggerPin = 7;
const int echoPin = 8;    

long duration;
float distance;

long lastMillis;


void setup() {
    pinMode(triggerPin, OUTPUT);
    pinMode(echoPin, INPUT);
    Serial.begin(9600);
    Serial.println("millis,cm");
}

void printDuration() {


    if(millis() - lastMillis >= 20) {
        digitalWrite(triggerPin, LOW);
        delayMicroseconds(2);

        digitalWrite(triggerPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(triggerPin, LOW);
        
        duration = pulseIn(echoPin, HIGH, 190000);
        distance = duration * 0.0343/2;

        lastMillis = millis();
        Serial.print(lastMillis);
        Serial.print(", ");
        Serial.println(distance, 4);
    }
}

void loop() {
    printDuration();
}
