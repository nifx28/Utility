using UnityEngine;
using System.Collections;

public class NewBehaviourScript1 : MonoBehaviour {
	private readonly float amount = 20;
	private static GameObject cube;
	private static bool isStart = false;

	// Use this for initialization
	void Start () {
		if (cube == null) {
			MeshFilter[] meshes = FindObjectsOfType<MeshFilter> ();

			foreach (MeshFilter mesh in meshes) {
				if (mesh.sharedMesh.name.Equals ("Cube") && mesh.gameObject.name.Equals ("Water Cube")) {
					cube = mesh.gameObject;
				}
			}
		}
	}
	
	// Update is called once per frame
	void Update () {
		if (isStart) {
			cube.transform.Rotate(Vector3.up * amount * Time.deltaTime);
		}
	}

	void OnMouseDown() {
		if (name.Equals ("Start")) {
			isStart = true;
		} else if (name.Equals ("Stop")) {
			isStart = false;
		} else if (name.Equals ("Reset")) {
			cube.transform.rotation = new Quaternion();
		}
	}
}
