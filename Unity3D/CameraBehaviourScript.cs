using UnityEngine;
using UnityEngine.UI;

public class NewBehaviourScript : MonoBehaviour {
	private readonly float amount = 20;
	private Text coord;

	// Use this for initialization
	void Start () {
		if (coord == null) {
			Text[] objs = GameObject.FindObjectsOfType<Text> ();

			foreach (Text obj in objs) {
				if (obj.name.Equals("Value")) {
					coord = obj;
				}
			}
		}
	}
	
	// Update is called once per frame
	void Update () {
		Vector3 trans = new Vector3 ();

		if (Input.GetKey (KeyCode.W)) {
			trans = Vector3.forward * amount * Time.deltaTime;
		}

		if (Input.GetKey (KeyCode.S)) {
			trans = Vector3.back * amount * Time.deltaTime;
		}

		if (Input.GetKey (KeyCode.A)) {
			trans = Vector3.left * amount * Time.deltaTime;
		}

		if (Input.GetKey(KeyCode.D)) {
			trans = Vector3.right * amount * Time.deltaTime;
		}

		if (Input.GetKey(KeyCode.C)) {
			trans = Vector3.down * amount * Time.deltaTime;
		}

		if (Input.GetKey(KeyCode.Space)) {
			trans = Vector3.up * amount * Time.deltaTime;
		}

		Vector3 pos = transform.position;
		transform.Translate(trans);

		if (transform.position.y > 10 || transform.position.y < 0.1) {
			transform.position = pos;
		}

		coord.text = transform.position.x + "\n" + transform.position.y + "\n" + transform.position.z;
	}
}
