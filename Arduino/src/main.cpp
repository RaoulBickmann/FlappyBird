#include <Arduino.h>

const int triggerPin = 7;
const int echoPin = 8;    

long duration;
long distance;

void setup() {
    pinMode(triggerPin, OUTPUT);
    pinMode(echoPin, INPUT);
    Serial.begin(9600); 
}

void printDistance() {
    digitalWrite(triggerPin, LOW);
    delayMicroseconds(2);

    digitalWrite(triggerPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPin, LOW);

    duration = pulseIn(echoPin, HIGH);

    distance = duration * 0.034/2;

    Serial.print("Distance: ");
    Serial.println(duration);  
}

void loop() {
    delay(50);
    printDistance();
}
