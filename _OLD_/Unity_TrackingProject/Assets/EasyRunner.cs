using UnityEngine;
using System.Collections;
using System.IO;
using System;

public class EasyRunner : MonoBehaviour
{
    public Vector3 camera_pos = new Vector3(-5.0f, 3.0f, 6.0f);
    public int steps = 1000;
    public string object_name = "Runs";
    private float x_begin = 7.5f, x_end = -6.0f;
    private float z_begin = 5.0f, z_end = -5.0f;
    //private float x_begin = 13, x_end = -11;
    //private float z_begin = 8.5f, z_end = -9.0f;
    private float y = 0.25f;
    private float x_step, z_step;
    private float min_dist, max_dist, diff_dist;
    private Vector3 start_scale = new Vector3(1.6f, 1.6f, 1.6f);
    private Vector3 diff_scale = new Vector3(0.7f, 0.7f, 0.7f);
    private GameObject obj;
    private Vector3 rot;

    protected Animator animator;
    public float DirectionDampTime = 0.25f;
    public float h = 1, v = 1;


    public string path = "C:\\Users\\Andrew\\Desktop\\VisionLab\\Unity_TrackingProject\\CapturedVideo\\";
    private string capture_path;
    private bool folder_done = true;
    public int max_screenshots = 1000;
    private int screenshot_number = 0;
    public int quality = 1;


    // Use this for initialization
    void Start()
    {
        x_step = (x_end - x_begin) / steps;
        z_step = (z_end - z_begin) / steps;
        obj = GameObject.Find(object_name);
        rot = obj.transform.localEulerAngles;
        obj.transform.position = new Vector3(x_begin, y, z_begin);
        //obj.transform.position = new Vector3(13, y, 8.5f);
        min_dist = Distance(camera_pos, obj.transform.position);
        max_dist = Distance(camera_pos, new Vector3(x_end, y, z_end));
        diff_dist = max_dist - min_dist;

        MakeTimeFolder();

        animator = obj.GetComponent<Animator>();
        Debug.Log(animator);
        if (animator.layerCount >= 2)
            animator.SetLayerWeight(1, 1);
    }

    // Update is called once per frame
    void Update()
    {

        if (steps-- < 0)
            return;
        ObjectTranslate(obj, new Vector3(x_step, 0, z_step));
        float dist = Distance(obj.transform.position, camera_pos);
        obj.transform.localScale = start_scale - diff_scale * (1 - (max_dist - dist) / diff_dist);

        SaveScrinshot();

        animator.SetFloat("Speed", h * h + v * v);
        animator.SetFloat("Direction", h, DirectionDampTime, Time.deltaTime);


    }

    void ObjectTranslate(GameObject obj, Vector3 translation)
    {
        obj.transform.localEulerAngles = new Vector3(0, 0, 0);
        obj.transform.Translate(translation);
        obj.transform.localEulerAngles = rot;
    }

    static float Distance(Vector3 v1, Vector3 v2)
    {
        Vector3 s = v1 - v2;
        return Mathf.Sqrt(s.x * s.x + s.y * s.y + s.z * s.z);
    }

    void MakeTimeFolder()
    {
        string new_folder = DateTime.Now.Day.ToString() + "-" +
            DateTime.Now.Month.ToString() + "__" +
                DateTime.Now.Hour.ToString() + "-" +
                DateTime.Now.Minute.ToString() + "-" +
                DateTime.Now.Second.ToString();
        capture_path = new_folder + "\\";
        Debug.Log(capture_path);
        Debug.Log(Directory.CreateDirectory(path + capture_path));
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
        return name + "_Q" + quality.ToString() + ".jpg";
    }

    void SaveScrinshot()
    {
        if (!folder_done || screenshot_number == max_screenshots)
            return;
        Application.CaptureScreenshot(path + capture_path + filename(screenshot_number++, quality), quality);
    }
}
