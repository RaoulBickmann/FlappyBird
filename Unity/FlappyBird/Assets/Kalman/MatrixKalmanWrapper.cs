using UnityEngine;

namespace Kalman {
	
	/// <summary>
	/// Matrix kalman wrapper.
	/// </summary>
	public class MatrixKalmanWrapper : IKalmanWrapper
	{
		private KalmanFilter kY;
		
		public MatrixKalmanWrapper (double set_q)
		{
            var Ts = 0.02;
		    var Q = set_q;
		    var G = Matrix.CreateVector(Mathf.Pow((float)Ts, 3)/6, Mathf.Pow((float)Ts, 3)/2, Ts);
		    var a = new Matrix(new[,] { { 0, 1.0, 0 }, { 0, 0, 1.0 }, { 0, 0, 0 } }); //a

            /*
			X0 : predicted state
			P0 : predicted covariance
			
			F : factor of real value to previous real value
			B : the control-input model which is applied to the control vector uk;
			U : the control-input model which is applied to the control vector uk;
			Q : measurement noise
			H : factor of measured value to real value
			R : environment noise
			*/
            var f = Matrix.IdentityMatrix(3) + (Ts * a) + 0.5 * Matrix.Power(Ts * a, 2);    //ad
			var b = Matrix.CreateVector(0);
            var u = Matrix.CreateVector(0);
            var r_good = Matrix.CreateVector (0.68);
            var r_bad = Matrix.CreateVector (1000000000000);
		    var q = (Q * G) * G.Transpose();                                                //g * q * g.T
			var h = new Matrix (new[,] {{1.0 , 0, 0}});                                     //c
			
			kY = makeKalmanFilter (f, b, u, q, h, r_good, r_bad);
		}
		
		public Vector3 Update (Vector3 current)
		{
			kY.Correct (new Matrix (new double[,] {{current.y}}));
			
			// rashod
			// kX.State [1,0];
			// kY.State [1,0];
			// kZ.State [1,0];
			
			Vector3 filtered = new Vector3 (
                current.x,
				(float)kY.State [0, 0],
                current.z
            );
			return filtered;
		}
	
		public void Dispose ()
		{
		
		}
		
		#region Privates
		KalmanFilter makeKalmanFilter (Matrix f, Matrix b, Matrix u, Matrix q, Matrix h, Matrix r_good, Matrix r_bad)
		{
			var filter = new KalmanFilter (
				f.Duplicate (),
				b.Duplicate (),
				u.Duplicate (),
				q.Duplicate (),
				h.Duplicate (),
				r_good.Duplicate (),
				r_bad.Duplicate ()
			);
			// set initial value
			filter.SetState (
				Matrix.CreateVector (0, 0, 0), 
				new Matrix (new [,] {{100, 0, 0}, {0, 9.0, 0}, {0, 0, 1.0}})
			);
			return filter;
		}
		#endregion
		
		
		
	}

}
