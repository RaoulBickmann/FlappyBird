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
using Kalman;

/**
 * When creating your message listeners you need to implement these two methods:
 *  - OnMessageArrived
 *  - OnConnectionEvent
 */
public class MessageListener : MonoBehaviour
{
    // Invoked when a line of data is received from the serial device.
    void OnMessageArrived(string msg)
    {
        Regex regex = new Regex(",");
        string[] pos = regex.Split(msg);
        Debug.Log("Message arrived: " + pos[1]);
        if(pos[1] != "cm")
        {
            transform.position = new Vector3(0f, float.Parse(pos[1]), 0f);
        }
    }

    float KalmanFilter(float[] y, int N, float Ts)
    {

        SimpleKalmanWrapper filter = new SimpleKalmanWrapper();

        //Ad, C, Gd = GiveNumericalMatrices(Ts)

        float Q = 100000;               //Prozessrauschen in cm/s^3 ??
        float R_good = 0.68f;         //Sensorrauschen in cm^2 ??
        float R_bad = 100000000;

        float[,,] x_post = new float[3,1, N];
        float[,,] P_post = new float[3,3, N];

        float[,] x_post_last = new float[,] { { 0 }, { 0 }, { 0 } };
        float[,] P_post_last = new float[,] { { 100, 0, 0 }, { 0, 9, 0 }, { 0, 0, 1 } };



       
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
}
