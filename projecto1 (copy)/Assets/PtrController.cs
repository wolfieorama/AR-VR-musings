/************************************************************************************

Copyright   :   Copyright 2017 Oculus VR, LLC. All Rights reserved.

Licensed under the Oculus VR Rift SDK License Version 3.4.1 (the "License");
you may not use the Oculus VR Rift SDK except in compliance with the License,
which is provided at the time of installation or download, or which
otherwise accompanies this software in either electronic or hard copy form.

You may obtain a copy of the License at

https://developer.oculus.com/licenses/sdk-3.4.1


Unless required by applicable law or agreed to in writing, the Oculus VR SDK
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

************************************************************************************/

using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;
using System.Collections;
using System.Collections.Generic;

public class PtrController : MonoBehaviour{

  [System.Serializable]
  public class perkCB_rayhit : UnityEvent<Ray, RaycastHit> {}
  public perkCB_rayhit rayhit;

  Vector3 world_origin;
  Vector3 cont_pos;
  Quaternion cont_rot;
  int update_ctr = 0;
  float next_click_time = 0.0f;

  LayerMask excludeLayers;
  LineRenderer lr = null;
  Transform RHA = null;  // Stands for Right Hand Anchor

  void Start(){
    Debug.Log("PERK start was called");
    Debug.Log("PERK Adding the rayhit listener");
    rayhit.AddListener( do_rayhit );

    world_origin = new Vector3(0, 0, 0);
    lr = gameObject.AddComponent<LineRenderer>();
    lr.useWorldSpace = true;
    lr.SetPosition(0, world_origin);
    lr.SetPosition(1, world_origin);
    lr.startWidth = 0.03f;
    lr.endWidth = 0.01f;
    lr.enabled = false;
  }

	// Update is called once per frame
  void Update(){
    OVRInput.Update();
    cont_pos = OVRInput.GetLocalControllerPosition(
                       OVRInput.GetActiveController( ) );
    cont_rot = OVRInput.GetLocalControllerRotation(
                       OVRInput.GetActiveController( ) );

    GameObject right = GameObject.Find("RightHandAnchor");
    RHA = right.transform;
    Ray laserpointer = new Ray(RHA.position, RHA.forward);
    lr.SetPosition(0, laserpointer.origin);
    lr.SetPosition(1, laserpointer.origin + laserpointer.direction * 50.0f);

		// Turn on the ray if the thumbpad button is pressed    
		if( OVRInput.Get(OVRInput.Button.One) ){
      lr.enabled = true;
    }
    else lr.enabled = false;

		// If the ray is on and we hit an object, and the trigger is
		// pulled, process the hit    
		if( lr.enabled ){
      RaycastHit hit;
      if(Physics.Raycast(laserpointer, out hit, 500.0f, ~excludeLayers)){
        if(lr != null){
          lr.SetPosition (1, hit.point);
        }
        if(rayhit != null) { // Should never be null but check in case
          // Check if trigger button is pulled
					if( OVRInput.Get(OVRInput.Button.PrimaryIndexTrigger) ){
            rayhit.Invoke(laserpointer, hit);
          }  
        }
      }
    } 
    
		// Print a status message to the log
		if( update_ctr % 250 == 0 ){
      Debug.Log("PERK update_ctr = " + update_ctr);
      /*
      Debug.Log("    PERK controller type = " + 
                                   OVRInput.GetActiveController() );
      Debug.Log("    PERK controller position = " + cont_pos);
      Debug.Log("    PERK controller rot = " + cont_rot.eulerAngles);
      */
    }
    update_ctr += 1;
  }

  void do_rayhit(Ray myray, RaycastHit myhit ){
    GameObject gm_hit = myhit.collider.gameObject;

    if(gm_hit.name == "bouncy_ball"){
      // gm_hit.GetComponent<BallCollide>().collide();
      Material like_it = gm_hit.GetComponent<Renderer>().material;
        Color newcolor;

        if(like_it.color.r == 255){
            newcolor.r = 0f;
            newcolor.g = 255f;
            newcolor.b = 0f;
            newcolor.a = 0f;
        } 
        else if(like_it.color.g == 255){
            newcolor.r = 0f;
            newcolor.g = 0f;
            newcolor.b = 255f;
            newcolor.a = 0f;
        } 
        else {
            newcolor.r = 255f;
            newcolor.g = 0f;
            newcolor.b = 0f;
            newcolor.a = 0f;
        }

        like_it.color = newcolor;
    }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    else if(gm_hit.name != "Button" ){
      Debug.Log("   PERK ray hit an object other than the Button");
    }
    else{ // The ray hit the Button
      GameObject go_bb = GameObject.Find("bouncy_ball");
      Rigidbody rb = go_bb.GetComponent<Rigidbody>();
      rb.velocity = new Vector3(0f, 0f, 0f);
      go_bb.transform.position = new Vector3(0f, 10f, 10f);
			// We need the time check below to control the click activation rate
      if( Time.time > next_click_time  ){
        Debug.Log("PERK Time.time = " + Time.time);
        next_click_time = Time.time + 1.0f;
        Button likeit = gm_hit.GetComponent(typeof(Button)) as Button;
        likeit.onClick.Invoke();
      }
    }
  }
}
