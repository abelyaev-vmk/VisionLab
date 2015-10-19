using UnityEngine;
using System.Collections;
using System.IO;
using System;

public class MovieMake : MonoBehaviour {
	public string path = "C:\\Users\\Andrew\\Desktop\\VisionLab\\Unity_TrackingProject\\CapturedVideo\\";
	private string capture_path;
	private bool folder_done = true;
	public int max_screenshots = 1000;
	private int screenshot_number = 0;
	public int quality = 1;
	// Use this for initialization

	void MakeTimeFolder()
	{
		string new_folder = DateTime.Now.Day.ToString() + "-" +
			DateTime.Now.Month.ToString() + "__" + 
				DateTime.Now.Hour.ToString() + "-" + 
				DateTime.Now.Minute.ToString() + "-" +
				DateTime.Now.Second.ToString();
		capture_path = new_folder + "\\";
		Debug.Log (capture_path);
		Debug.Log (Directory.CreateDirectory(path + capture_path));
	}

	string filename(int number, int quality)
	{
		string name = "IMG";
		int max = max_screenshots * 10;
		while (max > number)
		{
			max /= 10;
			name += "0";
		}
		name += number.ToString();
		return name + "_Q" + quality.ToString() + ".png";
	}

	public void Start () {
		//Screen.SetResolution(720, 480, false);
		MakeTimeFolder();

		/*Camera cmr = gameObject.GetComponent<Camera>();
		Debug.Log (cmr.name);
		Debug.Log (cmr.depthTextureMode);
		cmr.depthTextureMode = DepthTextureMode.DepthNormals;
		Debug.Log (cmr.depthTextureMode);*/


	}
	
	// Update is called once per frame
	public void Update () {
		if (!folder_done || screenshot_number == max_screenshots)
			return;
		Application.CaptureScreenshot(path + capture_path + filename(screenshot_number++, quality), quality);
	}

}
