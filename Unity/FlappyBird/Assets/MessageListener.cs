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
    private MatrixKalmanWrapper kalman1;
    private MatrixKalmanWrapper kalman2;
    private MatrixKalmanWrapper kalman3;
    private StreamReader streamReader;
    FileStream fileStream = new FileStream(@"D:\Projekte\FlappyBird\Python\PythonApplication1\data_movie2.csv", FileMode.Open, FileAccess.Read);

    public GameObject cube;
    public GameObject cube1;
    public GameObject cube2;
    public GameObject cube3;

    void Start()
    {
        streamReader = new StreamReader(fileStream, Encoding.UTF8);
        kalman1 = new MatrixKalmanWrapper(100000);
        kalman2 = new MatrixKalmanWrapper(1000000);
        kalman3 = new MatrixKalmanWrapper(10000);
    }

    void Update()
    {
        //test();
    }

    // Invoked when a line of data is received from the serial device.
    void OnMessageArrived(string msg)
    {
        Regex regex = new Regex(",");
        string[] pos = regex.Split(msg);
        Debug.Log("Message arrived: " + pos[1]);
        if(pos[1] != "cm")
        {
            cube.transform.position = new Vector3(cube.transform.position.x, float.Parse(pos[1]), cube.transform.position.z);
            cube1.transform.position = kalman1.Update(new Vector3(cube1.transform.position.x, float.Parse(pos[1]), cube1.transform.position.z));
            cube2.transform.position = kalman2.Update(new Vector3(cube2.transform.position.x, float.Parse(pos[1]), cube2.transform.position.z));
            cube3.transform.position = kalman3.Update(new Vector3(cube3.transform.position.x, float.Parse(pos[1]), cube3.transform.position.z));
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
                cube1.transform.position = kalman1.Update(new Vector3(0f, float.Parse(pos[1]), 0f));
                cube2.transform.position = new Vector3(-3f, float.Parse(pos[1]), 0f);
            }
        }
        
    }
}
