using UnityEngine;
using System.Collections;
using System.IO;

public class CreatePlane : MonoBehaviour {
	public string Scene = "007";
	private int height, width;
	// Use this for initialization
	void Start () {
		Renderer renderer = GetComponent<Renderer>();
		StreamReader sr = new StreamReader(Scene + ".txt");
		string[] s = sr.ReadLine().Split(' ');
		height = System.Convert.ToInt32(s[0]);
		width = System.Convert.ToInt32(s[1]);
		CameraCalibration cc = new CameraCalibration();
		cc.pathXML = "View_" + Scene + ".xml";
		cc.GetDataFromXML();
		cc.GetMatrixesOfCameras();

		//Texture2D texture = new Texture2D(Mathf.CeilToInt(max_x - min_x), Mathf.CeilToInt(max_y - min_y));
		Vector2 hor = cc.FindHorizont();
		float k = -hor[0] / hor[1];
		float b = -1 / hor[1];

		float im_min_x = width, im_min_y = height, im_max_x = 0, im_max_y = 0;
		for (int x = 0; x < width; x++)
			for (int y = 0; y < height; y++)
				if (OnGround(x, y, k, b))
				{
					if (im_min_x > x)
						im_min_x = x;
					if (im_min_y > y)
						im_min_y = y;
					if (im_max_x < x)
						im_max_x = x;
					if (im_max_y < y)
						im_max_y = y;
				}
		disp (im_min_x, im_min_y, im_max_x, im_max_y);
		/////!!!!!!
		im_min_y = 150.0f;
		/// 
		Vector3 leftUp, leftDown, rightUp, rightDown, center;
		leftUp = cc.Img2World(im_min_x, im_max_y);
		leftDown = cc.Img2World(im_min_x, im_min_y);
		rightDown = cc.Img2World(im_max_x, im_min_y);
		rightUp = cc.Img2World(im_max_x, im_max_y);
		center = cc.Img2World(width / 2, height / 2);
		float min_x = min (leftUp.x, leftDown.x, rightUp.x, rightDown.x);
		float min_y = min (leftUp.y, leftDown.y, rightUp.y, rightDown.y);
		float max_x = max (leftUp.x, leftDown.x, rightUp.x, rightDown.x);
		float max_y = max (leftUp.y, leftDown.y, rightUp.y, rightDown.y);
		transform.position = center;
		disp (Mathf.CeilToInt(max_x - min_x), Mathf.CeilToInt(max_y - min_y));
		transform.localScale = new Vector3((max_x - min_x) / 2,1.0f, (max_y - min_y) / 2);
		//Texture2D texture = new Texture2D(Mathf.CeilToInt(max_x - min_x), Mathf.CeilToInt(max_y - min_y));
		Texture2D texture = new Texture2D(10000, 10000);
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	public bool OnGround(float x, float y, float k, float b)
	{
		return y > k * x + b;
	}

	public void SetPixel(ref Texture2D tx, Color c, float x, float y, float r)
	{
		float x_min = max (0, x - r), x_max = min (x + r, width);
		float y_min = max (0, y - r), y_max = min (y + r, height);
		for (int i = Mathf.CeilToInt(x_min); i < x_max; i++)
			for (int j = Mathf.CeilToInt(y_min); j < y_max; j++)
				tx.SetPixel(i, j, c);
	}

	public static void disp(params object[] list)
	{
		foreach(object obj in list)
			Debug.Log(obj);
	}

	public static float min(params float[] vars)
	{
		float m = vars[0];
		foreach(float v in vars)
			if (v < m)
				m = v;
		return m;
	}

	public static float max(params float[] vars)
	{
		float m = vars[0];
		foreach(float v in vars)
			if (m < v)
				m = v;
		return m;
	}
}
