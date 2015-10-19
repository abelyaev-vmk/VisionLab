using UnityEngine;
using System.Collections;

public class TranslatePlane : MonoBehaviour {
	public string Scene = "007";
	void Start () {
		CameraCalibration cc = new CameraCalibration();
		cc.pathXML = "View_" + Scene + ".xml";
		cc.GetDataFromXML();
		cc.GetMatrixesOfCameras();
		disp (transform.position);
		disp (GameObject.Find("CubeR").transform.localPosition);
		disp (cc.Img2World(cc.width, cc.height));
		//Vector3 pos = cc.Img2World(cc.width, cc.height);
		//Vector3 pos = cc.Img2World(cc.width, 0);
		//Vector3 pos = cc.Img2World(0, cc.height);
		Vector3 pos = cc.Img2World(0, 0);
		transform.position = new Vector3(pos.x, 0, pos.y);
	}

	void Update () {
	
	}

	public static void disp(params object[] list)
	{
		foreach(object obj in list)
			Debug.Log(obj);
	}

}
