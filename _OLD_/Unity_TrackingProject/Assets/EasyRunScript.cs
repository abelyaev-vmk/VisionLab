using UnityEngine;
using System.Collections;

public class EasyRunScript : MonoBehaviour {
	public float eye_degree = 60.0f;
	private float camera_degree;
	public float normal_distance = 7; // depth = 0.5
	public float half_distance = 3;
	private float max_distance, min_distance;
	static public int clons_count = 1;
	private GameObject cmr;

	// Use this for initialization
	void Start () {
		camera_degree = eye_degree * Mathf.PI / 180.0f;
		cmr = GameObject.Find("Main Camera");
		max_distance = normal_distance + half_distance;
		min_distance = normal_distance - half_distance;
		if (clons_count > 0)
			Debug.Log("Clons Creating " + clons_count.ToString());
		if (clons_count-- <= 0)
			return;

		/*
		/// 1 RUNNER ////
		GameObject runner = Instantiate(GameObject.Find("Runs"));
		runner.SetActive(true);
		float now_dist = normal_distance;
		float left_max_dist = normal_distance * Mathf.Tan(camera_degree);
		runner.transform.localScale = new Vector3(1, 1, 1);
		runner.transform.position = new Vector3(-left_max_dist, 0, cmr.transform.position.z + now_dist);
		runner.transform.Rotate(new Vector3(0, 90, 0));
		runner.name = "FirstRunner";
		*/

		///2 RUNNERS ////
		GameObject runner = Instantiate(GameObject.Find("Runs"));
		runner.SetActive(true);
		float now_dist = normal_distance;
		float left_max_dist = normal_distance * Mathf.Tan(camera_degree);
		runner.transform.localScale = new Vector3(1, 1, 1);
		runner.transform.position = new Vector3(-left_max_dist, 0, cmr.transform.position.z + now_dist);
		runner.transform.Rotate(new Vector3(0, 90, 0));
		runner.name = "FirstRunner";

		GameObject runner2 = Instantiate(GameObject.Find("Runs"));
		runner2.SetActive(true);
		runner2.transform.localScale = new Vector3(1, 1, 1);
		now_dist = normal_distance - half_distance;
		runner2.transform.position = new Vector3(-left_max_dist - 2, 0, cmr.transform.position.z + now_dist);
		runner2.transform.Rotate(new Vector3(0, 90, 0));
		runner2.name = "SecondRunner";

	}
	
	// Update is called once per frame
	void Update () {
		return;
	}
}
