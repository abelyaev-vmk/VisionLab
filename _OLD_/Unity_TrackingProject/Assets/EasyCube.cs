using UnityEngine;
using System.Collections;

public class EasyCube : MonoBehaviour {
	private Vector3 rot = new Vector3(60, 20, 10);
	public static int steps = 1400;
	// Use this for initialization
	void Start () {
		GameObject cube = GameObject.Find("Runs");
		rot = cube.transform.localEulerAngles;
	}
	
	// Update is called once per frame
	void Update () {
		if (steps-- > 0)
			ObjectTranslate(GameObject.Find("Runs"), new Vector3(-0.009f, 0, -0.005f));
		/*GameObject cube = GameObject.Find("Cube");
		cube.transform.localEulerAngles = new Vector3(0, 0, 0);
		cube.transform.Translate(new Vector3(-0.1f, 0, 0));
		cube.transform.localEulerAngles = rot;*/
	}

	static void ObjectTranslate(GameObject obj, Vector3 translation)
	{
		Vector3 rot = obj.transform.localEulerAngles;
		obj.transform.localEulerAngles = new Vector3(0, 0, 0);
		obj.transform.Translate(translation);
		obj.transform.localEulerAngles = rot;
	}
}
