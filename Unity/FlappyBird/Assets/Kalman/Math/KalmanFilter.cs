﻿using UnityEngine;

namespace Kalman
{
    public sealed class KalmanFilter
    {
        //System matrices
        public Matrix X0 { get; private set; }	// predicted state
        public Matrix P0 { get; private set; }	// predicted covariance

        public Matrix F { get; private set; }	// factor of real value to previous real value
        public Matrix B { get; private set; }	// the control-input model which is applied to the control vector uk;
        public Matrix U { get; private set; }	// the control-input model which is applied to the control vector uk;
        public Matrix Q { get; private set; }	// measurement noise
        public Matrix H { get; private set; }	// factor of measured value to real value
        public Matrix R_good { get; private set; }	// environment noise
        public Matrix R_bad { get; private set; }	// environment noise

        public Matrix State { get; private set; } 
        public Matrix Covariance { get; private set; }

        public KalmanFilter(Matrix f, Matrix b, Matrix u, Matrix q, Matrix h, Matrix r_good, Matrix r_bad)
        {
            F = f;
            B = b;
            U = u;
            Q = q;
            H = h;
            R_good = r_good;
            R_bad = r_bad;
        }
       
        public void SetState(Matrix state, Matrix covariance)
        {
            // Set initial state
            State = state;
            Covariance = covariance;
        }

        public void Correct (Matrix z)
		{
			// Predict
			//X0 = F * State +(B * U);
			X0 = F * State;
			P0 = F * Covariance * F.Transpose () + Q;

            //Debug.Log(z - (H * X0));
            Matrix R;

            if (Mathf.Abs((float)(z - (H * X0)).Det()) > 5 * (H * P0 * H.Transpose() + R_good).Det())
            {
                R = R_bad;
            } else
            {
                R = R_good;
            }

            // Correct
            //var k = P0 * H.Transpose() * (H * P0 * H.Transpose() + R).Inverse(); // kalman gain
            var k = P0 * H.Transpose () * (H * P0 * H.Transpose () + R).Invert (); // kalman gain
			State = X0 + (k * (z - (H * X0)));
			//Covariance = (Matrix.Identity (P0.RowCount) - k * H) * P0;
			Covariance = (Matrix.IdentityMatrix (P0.rows) - k * H) * P0;
		}
    }
}