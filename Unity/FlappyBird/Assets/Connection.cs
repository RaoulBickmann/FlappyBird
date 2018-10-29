using System.Collections;
using System.Collections.Generic;
using System.IO.Ports;
using UnityEngine;

public class Connection {

    SerialPort stream = new SerialPort("COM4", 9600); //Set the port (com4) and the baud rate (9600, is standard on most devices)

    public Connection()
    {
        stream.Open(); //Open the Serial Stream.
    }

    public void readSerial()
    {
        for(int i = 0; i < 5; i++) {
            Debug.Log(stream.ReadLine());
        }
    }
}
