
using UnityEngine;
using System.Collections;

public class SpriteTry : MonoBehaviour {

	// Use this for initialization
	void Start () {

		Texture2D tx = new Texture2D(100,100);
		tx.name = "TEXTURE";
		Rect R = new Rect(0,0,100,100);
		UnityEngine.Color[] c = new UnityEngine.Color[100*100];
		for (int i = 0; i < c.Length; i++)
		{
			switch(i % 5)
			{
			case 1:
				c[i] = new UnityEngine.Color(255,0,0,1);
				break;
			case 2:
				c[i] = new UnityEngine.Color(0,255,0,1);
				break;
			case 3:
				c[i] = new UnityEngine.Color(0,0,255,0.8f);
				break;

			case 4:
				c[i] = new UnityEngine.Color(120, 10, 37, 0.5f);
				break;
			default:
				c[i] = new UnityEngine.Color(100,231,120,0);
				break;
			}
		}
		Sprite sp = Sprite.Create(tx, R, new Vector2(0,0));
		tx.SetPixels(c);
		disp (tx.GetPixel(1,5), tx.GetPixel (90,1));
		var pl = GameObject.CreatePrimitive(PrimitiveType.Plane);
		pl.transform.position = new Vector3(0, 30, 0);
		pl.transform.rotation = Quaternion.Euler(180,0,0);
		disp(pl);
		Renderer r = GetComponent<Renderer>();
		disp (r.material);
		disp (r.material.name);
		disp (r.material.mainTexture.height, tx);
		r.material.mainTexture = tx;
		//Instantiate(pl, new Vector3(0,30,0), Quaternion.Euler(new Vector3(180,0,0)));
	}
	
	// Update is called once per frame
	void Update () {
	
	}

	static void disp(params object[] list)
	{
		foreach(object obj in list)
			Debug.Log(obj);
	}
}
