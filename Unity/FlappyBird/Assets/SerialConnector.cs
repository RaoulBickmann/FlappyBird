using System.Collections;
using System.IO.Ports;

using UnityEngine;

public class SerialConnector : MonoBehaviour {



    // Use this for initialization
    void Start () {
        Connection connection = new Connection();
        connection.readSerial();
	}
}
