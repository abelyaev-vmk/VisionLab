using UnityEngine;
using System.Collections;

public class TryCameraOptional : MonoBehaviour {
	public bool UseConstQuaternion = true;
	private Quaternion constQuaternion = new Quaternion(0.28876954f, 0.43029931f, 0.69724888f, -0.49527634f);
	private Vector3 constPosition = new Vector3(-0.059884f, 3.8333f, 12.3911f);
	void Start () 
	{
		if (UseConstQuaternion)
		{
			GameObject.Find ("Camera").transform.position = constPosition;
			GameObject.Find ("Camera").transform.rotation = constQuaternion;
		}
		Debug.Log(GameObject.Find ("Camera").transform.rotation);
	}
}
