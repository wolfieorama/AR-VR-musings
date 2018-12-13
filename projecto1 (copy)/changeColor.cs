public void Button_click() {
    Debug.Log("PERK Button was clicked!");
    GameObject go_as = GameObject.Find("MySound01");
    AudioSource aud_dat = 
                 go_as.GetComponent(typeof(AudioSource)) as AudioSource;
    aud_dat.Play(0);           
	}

GameObject go_bb = GameObject.Find("bouncy_ball");
Rigidbody rg = go_bb.GetComponent<Rigidbody>();
rb.velocity = new Vector3(0f, 0f, 0f);
go_bb.transform.position = new Vector3(0f, 10f, 10f);

if(gm_hit.name.Equals("Button")){

}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class ball_collide : MonoBehaviour {

    public void collide(){
        Material like_it = gm_hit.GetComponent<MeshRenderer().material;
        Color newcolor;

        if( like_it.color.r == 255 ){
            newcolor.r = 0f;
            newcolor.g = 255f;
            newcolor.b = 0f;
            newcolor.a = 0f;
        }

        bouncy_ball.color = newcolor;
    }
}