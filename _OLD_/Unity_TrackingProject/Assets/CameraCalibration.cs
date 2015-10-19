using UnityEngine;
using System.Collections;
using System.Xml;
public class CameraCalibration : MonoBehaviour{

	public bool fromXML = true;
	public string pathXML = "View_005.xml";
	private string pathFOLDER = "C:\\Users\\Andrew\\Desktop\\VisionLab\\_OLD_\\Unity_TrackingProject\\calibrations\\";
	private Camera cam;
	public float width, height;
	private float ncx, nfx, dx, dy, dpx, dpy;
	private float focal, kappal, cx, cy, sx;
	private float tx, ty, tz, rx, ry, rz;
	private Matrix4x4 K, F, P;

	/// <summary>
	/// Initialize scene
	/// </summary>
	public void Start () {
		Screen.SetResolution(System.Convert.ToInt32(width), System.Convert.ToInt32(height), false);
		Screen.SetResolution(720,576,false);
		cam = gameObject.GetComponent<Camera>();
		cam.farClipPlane = 1000000;
		GetDataFromXML();
		//ChangeData();
		GetMatrixesOfCameras();
		TEST_RotationAndTranslate();
		Test_Scene();
	}
	
	/// <summary>
	/// Update scene
	/// </summary>
	public void Update () {
	
	}
	
	/// <summary>
	/// JUST TESTING FUNCTION for rotation and translate camera
	/// </summary>
	public void TEST_RotationAndTranslate()
	{

		Matrix4x4 rot = GetRotationMatrix();
		disp (rot);
		Quaternion Q = MatrixToQuaternion(rot);
		cam.transform.localRotation = Q;
		cam.transform.localPosition = GetTranslationVector();
		disp (cam.transform.forward);
		disp (cam.transform.localPosition);
		cam.fieldOfView = GetViewAngle();
		/*Vector3 forward = cam.transform.forward;
		Quaternion roundForward = Quaternion.AngleAxis(180, forward);
		Q = MatrixToQuaternion(QuaternionToMatrix(roundForward) * rot);
		cam.transform.localRotation = Q;*/
	}


	/// <summary>
	/// JUST TESTING FUNCTION for creating scene
	/// </summary>
	public void Test_Scene()
	{
		/*Vector3 imgVec = Img2World(500, 500);
		disp(imgVec);
		GameObject cube = GameObject.Find("Cube");
		cube.transform.localPosition = imgVec;*/
		GameObject.Find("Cube1").transform.localPosition = Img2World(1, 1);
		GameObject.Find("Cube2").transform.localPosition = Img2World(1, height);
		GameObject.Find("Cube3").transform.localPosition = Img2World(width, 1);
		GameObject.Find("Cube4").transform.localPosition = Img2World(width, height);
		GameObject.Find("Cube5").transform.localPosition = Img2World(width/2, height/2);
		//GameObject.Find ("Cube1").transform.localPosition = Img2World(width/2, height/2);
	}
	
	/// <summary>
	/// Use camera like child of a main object. Can be incorrect
	/// </summary>
	public void Try2()
	{
		Vector3 position = new Vector3(tx, ty, tz) / 100;
		GameObject.Find("MainObject").transform.position = position;
		Vector3 rotation = new Vector3(rx, ry, rz);
		cam.transform.localRotation = Quaternion.Euler(rotation * 180 / Mathf.PI);
	}
	
	/// <summary>
	/// Using quaternion rotation. Can be incorrect
	/// </summary>
	public void Try1()
	{
		disp (tx, ty, tz);
		cam.transform.Translate(new Vector3(tx, ty, tz));
		Quaternion Q = Quaternion.Euler(new Vector3(rx, ry, rz) * 180 / Mathf.PI);
		disp (Q, cam.transform.rotation);
		cam.transform.rotation = cam.transform.rotation * Q;
		disp (Q, cam.transform.rotation);
	}

	/// <summary>
	/// UsingProjectionMatrix
	/// </summary>
	public void Try3()
	{
		cam.worldToCameraMatrix = F;
	}

	/// <summary>
	/// Small changes for better look
	/// </summary>
	public void ChangeData()
	{
		while (Mathf.Abs(tx) > 100 && Mathf.Abs(ty) > 100 && Mathf.Abs(tz) > 100)
		{
			if (Mathf.Abs(tx) < 10 || Mathf.Abs(ty) < 10 || Mathf.Abs(tz) < 10)
			{
				break;
			}
			else
			{
				tx /= 10;
				ty /= 10;
				tz /= 10;
			}
		}

	}

	/// <summary>
	/// Converts point from image to world coordinates
	/// </summary>
	/// <returns>Point in world coordinates.</returns>
	/// <param name="Xi">Xi.</param>
	/// <param name="Yi">Yi.</param>
	public Vector3 Img2World(float x, float y)
	{
		float p11, p12, p13, p14, p21, p22, p23, p24, p31, p32, p33, p34;
		p11 = P[0,0];
		p12 = P[0,1];
		p13 = P[0,2];
		p14 = P[0,3];
		p21 = P[1,0];
		p22 = P[1,1];
		p23 = P[1,2];
		p24 = P[1,3];
		p31 = P[2,0];
		p32 = P[2,1];
		p33 = P[2,2];
		p34 = P[2,3];
		Vector3 worldVec = new Vector3();
		float norm = (p11*p22 - p12*p21)/
			(p11*p22*p34 - p11*p24*p32 - p12*p21*p34 + p12*p24*p31 + p14*p21*p32 - p14*p22*p31) + 
				(x*(p21*p32 - p22*p31))/
				(p11*p22*p34 - p11*p24*p32 - p12*p21*p34 + p12*p24*p31 + p14*p21*p32 - p14*p22*p31) - 
				(y*(p11*p32 - p12*p31))/
				(p11*p22*p34 - p11*p24*p32 - p12*p21*p34 + p12*p24*p31 + p14*p21*p32 - p14*p22*p31);
		worldVec.x = (p12*p24 - p14*p22)/
			(p11*p22*p34 - p11*p24*p32 - p12*p21*p34 + p12*p24*p31 + p14*p21*p32 - p14*p22*p31) + 
				(x*(p22*p34 - p24*p32))/
				(p11*p22*p34 - p11*p24*p32 - p12*p21*p34 + p12*p24*p31 + p14*p21*p32 - p14*p22*p31) - 
				(y*(p12*p34 - p14*p32))/
				(p11*p22*p34 - p11*p24*p32 - p12*p21*p34 + p12*p24*p31 + p14*p21*p32 - p14*p22*p31);
		worldVec.y = (y*(p11*p34 - p14*p31))/
			(p11*p22*p34 - p11*p24*p32 - p12*p21*p34 + p12*p24*p31 + p14*p21*p32 - p14*p22*p31) - 
				(x*(p21*p34 - p24*p31))/
				(p11*p22*p34 - p11*p24*p32 - p12*p21*p34 + p12*p24*p31 + p14*p21*p32 - p14*p22*p31) - 
				(p11*p24 - p14*p21)/
				(p11*p22*p34 - p11*p24*p32 - p12*p21*p34 + p12*p24*p31 + p14*p21*p32 - p14*p22*p31);
		worldVec.z = 0;
		return worldVec / norm;
	}

	/// <summary>
	/// Gets the matrixes of cameras. 1st is a matrix of inside calibration, 
	/// 2nd is a matrix of outside calibration (projection matrix),
	/// 3rd is a camera's calibration matrix. 
	/// </summary>
	/// <returns>The matrixes of cameras.</returns>
	public Matrix4x4[] GetMatrixesOfCameras()
	{
		Matrix4x4 tmpFocal = NewMatrix();
		tmpFocal[0,0] = tmpFocal[1,1] = focal;
		tmpFocal[2,2] = 1;

		// compute matrix of in-calibration
		Matrix4x4[] matrixes = new Matrix4x4[3];
		K = NewMatrix();
		K[0,0] = sx / dpx;
		K[0,2] = cx;
		K[1,1] = 1 / dpy;
		K[1,2] = cy;
		K[2,2] = 1;
		K = K * tmpFocal;
		matrixes[0] = K;

		// compute matrix of out-calibration
		F = NewMatrix();
		float sa, ca, sb, cb, sg, cg;
		sa = Mathf.Sin(rx);
		ca = Mathf.Cos(rx);
		sb = Mathf.Sin(ry);
		cb = Mathf.Cos(ry);
		sg = Mathf.Sin(rz);
		cg = Mathf.Cos(rz);
		F[0,0] = cb * cg;
		F[0,1] = cg * sa * sb - ca * sg;
		F[0,2] = sa * sg + ca * cg * sb;
		F[1,0] = cb * sg;
		F[1,1] = sa * sb * sg + ca * cg;
		F[1,2] = ca * sb * sg - cg * sa;
		F[2,0] = -sb;
		F[2,1] = cb * sa;
		F[2,2] = ca * cb;
		/*F[0,3] = -(tx * F[0,0] + ty * F[1,0] + tz * F[2,0]);
		F[1,3] = -(tx * F[0,1] + ty * F[1,1] + tz * F[2,1]);
		F[2,3] = -(tx * F[0,2] + ty * F[1,2] + tz * F[2,2]);*/
		F[0,3] = tx;
		F[1,3] = ty;
		F[2,3] = tz;
		matrixes[1] = F;

		// compute camera's calibration matrix
		P = K * F;
		matrixes[2] = P;
		return matrixes;
	}

	/// <summary>
	/// Computes rotation matrix from matrix of camera's in-calibration
	/// </summary>
	/// <returns>The rotation matrix.</returns>
	public Matrix4x4 GetRotationMatrix()
	{
		Matrix4x4 rot = NewMatrix();
		for (int i = 0; i < 3; i++)
			for (int j = 0; j < 3; j++)
				rot[i, j] = F[i, j];
		return rot;
	}

	/// <summary>
	/// Computes translation vector from calibration matrix
	/// </summary>
	/// <returns>The translation vector.</returns>
	public Vector3 GetTranslationVector()
	{
		Vector3 trans = new Vector3();
		Matrix4x4 tmp = NewMatrix ();
		for(int i = 0; i < 3; i++)
			tmp[i,0] = F[i,3];
		tmp = GetRotationMatrix().transpose * tmp;
		for (int i = 0; i < 3; i++)
			trans[i] = -tmp[i, 0];
		return trans;
	}

	public Vector2 FindHorizont()
	{
		Matrix4x4 temp = new Matrix4x4();
		for (int i = 0; i < 4; i++)
			for (int j = 0; j < 3; j++)
				temp[i,j] = P[i, j];
		Matrix4x4 dir = new Matrix4x4();
		dir[0,0] = dir[1, 1] = 1;
		Matrix4x4 points = temp * dir;
		points[2,2] = points[3,3] = 1;
		temp = new Matrix4x4();
		temp[0,2] = 1;
		Matrix4x4 line = temp * points.inverse;
		return new Vector2(line[0,0], line[0,1]);
	}

	public float GetViewAngle()
	{
		return 2 * Mathf.Atan(0.5f * height / (focal / dpx)) * 180 / Mathf.PI;
		/*float ratio = height / width;
		return 2 * Mathf.Atan(ratio * 0.5f * ncx * dx / focal) * 180 / Mathf.PI;*/ 
	}

	/// <summary>
	/// Computes rotation matrix from quaternion
	/// </summary>
	/// <returns>The to matrix.</returns>
	/// <param name="Q">Q.</param>
	public static Matrix4x4 QuaternionToMatrix(Quaternion Q)
	{
		Matrix4x4 matr = new Matrix4x4();
		float wx, wy, wz, xx, xy, xz, yy, yz, zz, x2, y2, z2;
		float s = 2.0f/Norm (Q);
		x2 = Q.x * s; y2 = Q.y *s ; z2 = Q.z *s ;
		xx = Q.x * x2; xy = Q.x * y2; xz = Q.x * z2;
		yy = Q.y * y2; yz = Q.y * z2; zz = Q.z * z2;
		wx = Q.w * x2; wy = Q.w * y2; wz = Q.w * z2;
		matr[0,0] = 1.0f - (yy + zz);
		matr[0,1] = xy + wz;
		matr[0,2] = xz - wy;
		matr[1,0] = xy - wz;
		matr[1,1] = 1.0f - (xx + zz);
		matr[1,2] = yz + wx;
		matr[2,0] = xz + wy;
		matr[2,1] = yz - wx;
		matr[2,2] = 1.0f - (xx + yy);
		matr[3,3] = 1;
		return matr;
	}

	/// <summary>
	/// Computes quaternion from rotation matrix
	/// </summary>
	/// <returns>The to quaternion.</returns>
	/// <param name="m">M.</param>
	public static Quaternion MatrixToQuaternion(Matrix4x4 m)
	{
		/*Quaternion Q = new Quaternion();
		float tr = m[0,0] + m[1,1] + m[2,2];
		if (tr > 0.0f)
		{
			Q.w = tr + 1.0f;
			Q.x = 0.5f * (m[1,2] - m[2,1]) / (float)Mathf.Sqrt (Q.w);
			Q.y = 0.5f * (m[2,0] - m[0,2]) / (float)Mathf.Sqrt (Q.w);
			Q.z = 0.5f * (m[0,1] - m[1,0]) / (float)Mathf.Sqrt (Q.w);
			Q.w = 0.5f * Q.w / (float)Mathf.Sqrt (Q.w);
		}
		else if (m[0,0] > m[1,1] && m[0,0] > m[2,2])
		{
			Q = new Quaternion(1.0f + m[0,0] - m[1,1] - m[2,2], m[1,0] + m[0,1], m[2,0] + m[0,2], m[1,2] - m[2,1]);
			Q.x *= 0.5f / (float)Mathf.Sqrt (Q.x);
			Q.y *= 0.5f / (float)Mathf.Sqrt (Q.x);
			Q.z *= 0.5f / (float)Mathf.Sqrt (Q.x);
			Q.w *= 0.5f / (float)Mathf.Sqrt (Q.x);
		}
		else if (m[1,1] > m[2,2])
		{
			Q = new Quaternion(m[1,0] + m[0,1], 1.0f + m[1,1] - m[0,0] - m[2,2], m[2,1] + m[1,2], m[2,0] - m[0,2]);
			Q.x *= 0.5f / (float)Mathf.Sqrt (Q.y);
			Q.y *= 0.5f / (float)Mathf.Sqrt (Q.y);
			Q.z *= 0.5f / (float)Mathf.Sqrt (Q.y);
			Q.w *= 0.5f / (float)Mathf.Sqrt (Q.y);
		}
		else
		{
			Q = new Quaternion(m[2,0] + m[0,2], m[2,1] + m[1,2], 1.0f + m[2,2] - m[0,0] - m[1,1], m[0,1] - m[1,0]);
			Q.x *= 0.5f / (float)Mathf.Sqrt (Q.z);
			Q.y *= 0.5f / (float)Mathf.Sqrt (Q.z);
			Q.z *= 0.5f / (float)Mathf.Sqrt (Q.z);
			Q.w *= 0.5f / (float)Mathf.Sqrt (Q.z);
		}
		return Q;*/
		float m00, m01, m02, m10, m11, m12, m20, m21, m22;
		/*m00 = m[0,0];
		m01 = m[0,1];
		m02 = m[0,2];
		m10 = m[1,0];
		m11 = m[1,1];
		m12 = m[1,2];
		m20 = m[2,0];
		m21 = m[2,1];
		m22 = m[2,2];*/
		m00 = m[0,0];
		m10 = m[0,1];
		m20 = m[0,2];
		m01 = m[1,0];
		m11 = m[1,1];
		m21 = m[1,2];
		m02 = m[2,0];
		m12 = m[2,1];
		m22 = m[2,2];
		float qx, qy, qz, qw;
		float tr = m00 + m11 + m22;	
		if (tr > 0) { 
			float S = Mathf.Sqrt(tr+1.0f) * 2; // S=4*qw 
			qw = 0.25f * S;
			qx = (m21 - m12) / S;
			qy = (m02 - m20) / S; 
			qz = (m10 - m01) / S; 
		} else if ((m00 > m11)&(m00 > m22)) { 
			float S = Mathf.Sqrt(1.0f + m00 - m11 - m22) * 2; // S=4*qx 
			qw = (m21 - m12) / S;
			qx = 0.25f * S;
			qy = (m01 + m10) / S; 
			qz = (m02 + m20) / S; 
		} else if (m11 > m22) { 
			float S = Mathf.Sqrt(1.0f + m11 - m00 - m22) * 2; // S=4*qy
			qw = (m02 - m20) / S;
			qx = (m01 + m10) / S; 
			qy = 0.25f * S;
			qz = (m12 + m21) / S; 
		} else { 
			float S = Mathf.Sqrt(1.0f + m22 - m00 - m11) * 2; // S=4*qz
			qw = (m10 - m01) / S;
			qx = (m02 + m20) / S;
			qy = (m12 + m21) / S;
			qz = 0.25f * S;
		}
		return new Quaternion(qx, qy, qz, qw);
	}
		
	/// <summary>
	/// Returns norm of quaternion
	/// </summary>
	/// <param name="Q">Q.</param>
	public static float Norm(Quaternion Q)
	{
		return (float)Mathf.Sqrt(Q.x*Q.x + Q.y*Q.y + Q.z*Q.z + Q.w*Q.w);
	}

	//World - ground_plane = (z=0)
	//Unity - ground_plane = (y=0)

	/// <summary>
	/// Computes quaternion for rotation from 
	/// Unity left-oriented coordinates to World left-oriented
	/// </summary>
	/// <returns>Quaternion</returns>
	public static Quaternion qULtoWL()
	{
		return Quaternion.Euler(270, 270, 0);
	}

	/// <summary>
	/// Computes rotation matrix4x4 from 
	/// Unity left-oriented coordinates to World left-oriented
	/// </summary>
	/// <returns>Rotation Matrix</returns>
	public static Matrix4x4 mULtoWL()
	{
		//Unity left-oriented to World left-oriented
		Matrix4x4 matr = new Matrix4x4();
		matr[0,2] = matr[1,0] = matr[2,1] = matr[3,3] = 1;
		return matr;
	}

	public static Matrix4x4 m2DLto2DR()
	{
		Matrix4x4 matr = NewMatrix();
		matr[0,0] = matr[2,2] = 1;
		matr[1,1] = -1;
		return matr;
	}

	/// <summary>
	/// Gets normal data about camera's calibration from XML
	/// </summary>
	public void GetDataFromXML()
	{
		XmlDocument xml = new XmlDocument();
		xml.Load (pathFOLDER + pathXML);
		ArrayList listOfAttributes = new ArrayList();
		foreach(XmlNode xnode in xml.DocumentElement)
		{
			float[] mas = new float[xnode.Attributes.Count];
			int m = 0;
			foreach(XmlAttribute xatr in xnode.Attributes)
				mas[m++] = (float)System.Convert.ToDouble(xatr.Value);
			listOfAttributes.Add(mas);
		}
		
		width = ((float[])listOfAttributes[0])[0];
		height = ((float[])listOfAttributes[0])[1];
		ncx = ((float[])listOfAttributes[0])[2];
		nfx = ((float[])listOfAttributes[0])[3];
		dx = ((float[])listOfAttributes[0])[4];
		dy = ((float[])listOfAttributes[0])[5];
		dpx = ((float[])listOfAttributes[0])[6];
		dpy = ((float[])listOfAttributes[0])[7];
		
		focal = ((float[])listOfAttributes[1])[0];
		kappal = ((float[])listOfAttributes[1])[1];
		cx = ((float[])listOfAttributes[1])[2];
		cy = ((float[])listOfAttributes[1])[3];
		sx = ((float[])listOfAttributes[1])[4];
		
		tx = ((float[])listOfAttributes[2])[0];
		ty = ((float[])listOfAttributes[2])[1];
		tz = ((float[])listOfAttributes[2])[2];
		rx = ((float[])listOfAttributes[2])[3];
		ry = ((float[])listOfAttributes[2])[4];
		rz = ((float[])listOfAttributes[2])[5];
	}

	/// <summary>
	/// Display the specified list.
	/// </summary>
	/// <param name="list">List.</param>
	public static void disp(params object[] list)
	{
		foreach(object obj in list)
			Debug.Log(obj);
	}

	/// <summary>
	/// Returns zero matrix with left-down (m[3,3]) = 1;
	/// </summary>
	/// <returns>The matrix.</returns>
	public static Matrix4x4 NewMatrix()
	{
		Matrix4x4 matr = new Matrix4x4();
		matr[3,3] = 1;
		return matr;
	}
}
