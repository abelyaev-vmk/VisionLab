using UnityEngine;
using System.Collections;
using System.IO;

public class ObjectRotation : MonoBehaviour {
	/*public bool user_references = false;
	public float x = 10, y = 10, z = -10;
	public float OX_rot = 30, OY_rot = 50, OZ_rot = 20;
	public int lx = 0, ly = 1, lz = 2;
	public int dx = 0, dy = 1, dz = 2;*/
	public bool new_try = true;
	public bool user_quaternion = true;
	public float FocalLengthX = 2696.3588f, FocalLengthY = 2696.3588f;
	public float PrincipalPointX = 959.5f, PrincipalPointY = 539.5f;
	public float Skew = 0.00f;
	public float TranslationX = -0.05988364f;
	public float TranslationY = 3.833331299f;
	public float TranslationZ = 12.39112186f;
	public float RotationX = 0.697249179f;
	public float RotationY = -0.43029625f;
	public float RotationZ = 0.288768885f;
	public float RotationW = 0.495278967f;
	public float DistortionK1 = -0.601506f, DistortionK2 = 4.702037f;
	public float DistortionP1 = -0.000475f, DistortionP2 = -0.00782f;
	private Camera camera;
	// Use this for initialization
	void Start () {
		//GameObject camera = GameObject.Find("Main Camera");
		camera = GetComponent<Camera>();
		//camera.transform.localRotation = new Quaternion(0,0,0,0);
		//camera.transform.position = new Vector3(0,0,0);

		/*
		string[] corns = File.ReadAllText("corners1.txt").Split('\n');
		for (int i = 0; i < corns.Length; i++)
			Debug.Log (corns[i]);
		Vector3[] corners = new Vector3[corns.Length / 3];
		for (int i = 0; i < corns.Length; i++)
			corners[i / 3][i % 3] = (float)System.Convert.ToDouble(corns[i]);
		for (int i = 0; i < corners.Length; i++)
		{

			GameObject cube = GameObject.Find("Cube" + (i+1).ToString());
			//cube.gameObject.
			//GameObject cube = GameObject.Find("MainObject").AddComponent(PrimitiveType.Cube);
			cube.transform.localScale = new Vector3(3, 3, 3);
			cube.transform.localPosition = corners[i];
		}*/

		if (new_try)
		{
			Matrix4x4 Rx = new Matrix4x4();
			Rx[3,3] = Rx[1,0] = Rx[2,1] = Rx[0,2] = 1;
			float rx = 1.77454f, ry = 0.363704f, rz = 0.092806f;
			//camera.transform.localPosition = new Vector3(3206, 23119, -287);
			Matrix4x4 R = new Matrix4x4();
			string[] numbers = File.ReadAllText("View.txt").Split(' ');
			for (int i = 0; i < 4; i++)
				for (int j = 0; j < 4; j++)
					R[j, i] = (float)System.Convert.ToDouble(numbers[4 * i + j]);
			/*R[0,0] = 0.9306f;
			R[0,1] = 0.0866f;
			R[0,2] = 0.3557f;
			R[1,0] = -0.3281f;
			R[1,1] = -0.2338f;
			R[1,2] = 0.9153f;
			R[2,0] = 0.1624f;
			R[2,1] = -0.9684f;
			R[2,2] = -0.1891f;
			R[3,3] = 1;*/
			Debug.Log(R);
			Debug.Log(Rx);
			R = R * Rx;
			camera.worldToCameraMatrix *= R;
			return;


			numbers = File.ReadAllText("proj.txt").Split(' ');
			for (int i = 0; i < numbers.Length; i++)
				Debug.Log (numbers[i]);
			Matrix4x4 pm = new Matrix4x4();
			for (int i = 0; i < 4; i++)
				for (int j = 0; j < 3; j++)
					pm[j, i] = (float)System.Convert.ToDouble(numbers[3 * i + j]);


			Rx[0,0] = Rx[3,3] = 1;
			/*Rx[2,1] = 1;
			Rx[1,2] = -1;*/
			/*Rx[2,1] = -1;
			Rx[1,2] = 1;*/
			Rx[1,2] = Rx[2,1] = -1;


			/*Rx[3,3] = 1;
			Rx[0,1] = Rx[1,2] = Rx[2,0] = 1;*/
			//Rx[1,2] = -1;


			Debug.Log (pm);
			Debug.Log (Rx);
			////!!!!!!
			//pm = (pm.transpose * Rx).transpose;

			pm = pm * Rx;
			pm[3, 3] = 1;
			camera.worldToCameraMatrix = pm;
			Debug.Log (camera.worldToCameraMatrix);
			return;
		}



		/*if (user_references)
		{
			camera.transform.position = new Vector3(x, y, z);
			camera.transform.rotation = Quaternion.Euler(OX_rot, OY_rot, OZ_rot);

		}
		else */if (user_quaternion)
		{
			camera.fieldOfView = 2 * Mathf.Atan2(PrincipalPointY, FocalLengthY) * 180 / Mathf.PI;
			//camera.transform.localRotation = new Quaternion(RotationX, RotationY, RotationZ, RotationW);
			//Debug.Log (camera.transform.localRotation.eulerAngles);

			float fi = Mathf.Atan2(2 * (RotationW * RotationX + RotationY * RotationZ),
			                      (1 - 2 * (RotationX * RotationX + RotationY * RotationY))) * 180 / Mathf.PI;

			float theta = Mathf.Asin(2 * (RotationW * RotationY - RotationX * RotationZ)) * 180 / Mathf.PI;

			float psi = Mathf.Atan2(2 * (RotationW * RotationZ + RotationY * RotationX), 
			                       (1 - 2 * (RotationY * RotationY + RotationZ * RotationZ))) * 180 / Mathf.PI;

			camera.transform.localRotation = Quaternion.Inverse(Quaternion.Euler(fi, theta, psi));
			Debug.Log (fi);
			Debug.Log (theta);
			Debug.Log (psi);
			//Debug.Log (Mathf.Atan(2 * (RotationW * RotationX + RotationY * RotationZ) 
			//                      / (1 - 2 * (RotationX * RotationX + RotationY * RotationY))) * 180 / Mathf.PI); 
			//camera.transform.localRotation = camera.transform.rotation * Quaternion.Euler(-90, 0, 0);
			/*camera.transform.rotation = camera.transform.rotation * new Quaternion(RotationX, RotationY, RotationZ, RotationW);
			Debug.Log(camera.transform.forward);*/
			//camera.transform.forward = new Vector3(0.8289f, -0.3426f, -0.4422f);
//			camera.transform.rotation = camera.transform.rotation * Quaternion.Inverse(Quaternion.Euler(-90, 0, 0));
			//camera.transform.rotation = Quaternion.Inverse(new Quaternion(RotationX, RotationZ, -RotationY, RotationW));
			//camera.transform.rotation = Quaternion.Euler(new Vector3(RotationX, RotationZ, -RotationY));
			camera.transform.localPosition = new Vector3(TranslationX, TranslationY, TranslationZ);
		}
		else
		{



			string[] numbers = File.ReadAllText("camera.txt").Split(' ');
			float[] location = new float[3], direction = new float[3];
			for (int i = 0; i < 3; i++)
			{
				location[i] = (float)System.Convert.ToDouble(numbers[i]);
				direction[i] = (float)System.Convert.ToDouble(numbers[4 + i]);
			}
			//float koef = 2;
			
			numbers = File.ReadAllText("matrix.txt").Split(' ');
			for (int i = 0; i < numbers.Length; i++)
				Debug.Log (numbers[i]);
			Matrix4x4 pm = new Matrix4x4();
			for (int i = 0; i < 4; i++)
				for (int j = 0; j < 3; j++)
					pm[j, i] = (float)System.Convert.ToDouble(numbers[4 * j + i]);
			pm[3,0] = pm[3,1] = pm[3,2] = 0;
			pm[3,3] = 1;
			Matrix4x4 Rx = new Matrix4x4();
			Rx[0, 0] = Rx[2, 1] = Rx[3, 3] = 1;
			Rx[1, 2] = -1;
			pm = pm * Rx;
			Debug.Log(Rx);

			//pm = camera.worldToCameraMatrix;
			for (int i = 0; i < 4; i++)
			{
				float t = pm[i, 1];
				pm[i, 1] = -pm[i, 2];
				pm[i, 2] = t;
			}

			/*Debug.Log (pm);
			Debug.Log (GL.GetGPUProjectionMatrix(pm, false));*/
			Debug.Log ("Last Camera Info:");
			Debug.Log(camera.worldToCameraMatrix);
			/*Debug.Log(camera.transform.position);
			Debug.Log(camera.transform.rotation);*/

			camera.worldToCameraMatrix = pm;

			//camera.projectionMatrix = pm.inverse;
			//camera.worldToCameraMatrix = pm;
			//camera.cameraToWorldMatrix = pm;

			Debug.Log ("New Camera Info:");
			Debug.Log(camera.worldToCameraMatrix);
			/*Debug.Log(camera.transform.position);
			Debug.Log(camera.transform.rotation);*/

			//camera.transform.rotation = new Quaternion(0.7f, 0.29f, -0.43f, 0.5f);
			/*camera.transform.position = new Vector3(location[lx], location[ly], location[lz]) * koef;
			camera.transform.forward = new Vector3(direction[dx], direction[dy], direction[dz]); */
		}
		Debug.Log (GetComponent<Camera>().name);
		Debug.Log(GetComponent<Camera>().worldToCameraMatrix);
	}
}

