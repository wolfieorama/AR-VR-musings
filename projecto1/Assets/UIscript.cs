using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class UIscript : MonoBehaviour {

	public void Button_click() {
    Debug.Log("PERK Button was clicked!");
    GameObject go_as = GameObject.Find("MySound01");
    AudioSource aud_dat = 
                 go_as.GetComponent(typeof(AudioSource)) as AudioSource;
    aud_dat.Play(0);           
	}
}
