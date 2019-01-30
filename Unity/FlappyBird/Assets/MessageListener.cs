/**
 * Ardity (Serial Communication for Arduino + Unity)
 * Author: Daniel Wilches <dwilches@gmail.com>
 *
 * This work is released under the Creative Commons Attributions license.
 * https://creativecommons.org/licenses/by/2.0/
 */

using UnityEngine;
using System.Collections;
using System.Text.RegularExpressions;
using System;
using System.IO;
using System.Text;
using Kalman;

/**
 * When creating your message listeners you need to implement these two methods:
 *  - OnMessageArrived
 *  - OnConnectionEvent
 */
public class MessageListener : MonoBehaviour
{
    private MatrixKalmanWrapper kalman;
    private StreamReader streamReader;
    FileStream fileStream = new FileStream(@"E:\Projekte\FlappyBird\Python\PythonApplication1\data_movie2.csv", FileMode.Open, FileAccess.Read);

    public GameObject cube1;
    public GameObject cube2;

    void Start()
    {
        streamReader = new StreamReader(fileStream, Encoding.UTF8);
        kalman = new MatrixKalmanWrapper();
    }

    void Update()
    {
        test();
    }

    // Invoked when a line of data is received from the serial device.
    void OnMessageArrived(string msg)
    {
        Regex regex = new Regex(",");
        string[] pos = regex.Split(msg);
        Debug.Log("Message arrived: " + pos[1]);
        if(pos[1] != "cm")
        {
            transform.position = kalman.Update(new Vector3(0f, float.Parse(pos[1]), 0f));
        }
    }

    // Invoked when a connect/disconnect event occurs. The parameter 'success'
    // will be 'true' upon connection, and 'false' upon disconnection or
    // failure to connect.
    void OnConnectionEvent(bool success)
    {
        if (success)
            Debug.Log("Connection established");
        else
            Debug.Log("Connection attempt failed or disconnection detected");
    }

    void test()
    {

        string line;
        if ((line = streamReader.ReadLine()) != null)
        {
            Debug.Log(line);
            Regex regex = new Regex(",");
            string[] pos = regex.Split(line);
            if (pos[1] != "cm")
            {
                cube1.transform.position = kalman.Update(new Vector3(0f, float.Parse(pos[1]), 0f));
                cube2.transform.position = new Vector3(-3f, float.Parse(pos[1]), 0f);
            }
        }
        
    }
}
