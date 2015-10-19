using UnityEngine;
using System.Collections;

public class TryCameraOptional : MonoBehaviour {
	public bool UseConstQuaternion = true;
	public Quaternion constQuaternion = new Quaternion(-0.22264708f, -0.43816416f, -0.70999293f, 0.50433173f);
	public Vector3 constPosition = new Vector3(-0.059884f, 3.8333f, 12.3911f);
	void Start () 
	{
		if (UseConstQuaternion)
		{
			GameObject.Find ("Camera").transform.position = constPosition;
			GameObject.Find ("Camera").transform.rotation = constQuaternion;
		}
	}
}
