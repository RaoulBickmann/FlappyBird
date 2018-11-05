#include <Arduino.h>

const int triggerPin = 7;
const int echoPin = 8;    

long duration;
float distance;


void setup() {
    pinMode(triggerPin, OUTPUT);
    pinMode(echoPin, INPUT);
    Serial.begin(9600);
    Serial.println("time,distance");
}

void printDuration() {
    digitalWrite(triggerPin, LOW);
    delayMicroseconds(2);

    digitalWrite(triggerPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPin, LOW);

    duration = pulseIn(echoPin, HIGH);

    distance = duration * 0.034/2;

    Serial.print(millis());
    Serial.print(", ");
    Serial.println(duration);
}

void loop() {
    printDuration();
}
