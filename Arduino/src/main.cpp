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
    Serial.println("time,distance");
}

void printDuration() {


    if(millis() - lastMillis >= 500) {
        digitalWrite(triggerPin, LOW);
        delayMicroseconds(2);

        digitalWrite(triggerPin, HIGH);
        delayMicroseconds(10);
        digitalWrite(triggerPin, LOW);
        
        duration = pulseIn(echoPin, HIGH, 3333);
        distance = duration * 0.034/2;

        Serial.print(millis());
        Serial.print(", ");
        Serial.println(duration);
        lastMillis = millis();

    }
}

void loop() {
    printDuration();
}
