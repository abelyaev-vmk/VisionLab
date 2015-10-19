using UnityEngine;
using System.Collections;

public class RUNRUN : MonoBehaviour {
	protected Animator animator;
	public float DirectionDampTime = .25f;
	public float h = 1, v = 1;
	// Use this for initialization
	void Start () {
		animator = GetComponent<Animator>();
		if(animator.layerCount >= 2)
			animator.SetLayerWeight(1, 1);
	}
	
	// Update is called once per frame
	void Update () {
		animator.SetFloat("Speed", h*h+v*v);
		animator.SetFloat("Direction", h, DirectionDampTime, Time.deltaTime);
	}
}
