// using System.Collections;
// using System.Collections.Generic;
// using UnityEngine;
// using UnityEngine.UI;
// using UnityEngine.SceneManagement;

// public class BallCollide : MonoBehaviour {
//     public void collide(){
//         Debug.Log("objects collided");
//         // GameObject bouncy_ball = GameObject.Find("bouncy_ball");

//         Material like_it = gm_hit.GetComponent<MeshRenderer>().material;
//         Color newcolor;

//         if(like_it.color.r == 255){
//             newcolor.r = 0f;
//             newcolor.g = 255f;
//             newcolor.b = 0f;
//             newcolor.a = 0f;
//         } 
//         else if(like_it.color.g == 255){
//             newcolor.r = 0f;
//             newcolor.g = 0f;
//             newcolor.b = 255f;
//             newcolor.a = 0f;
//         } 
//         else {
//             newcolor.r = 0f;
//             newcolor.g = 0f;
//             newcolor.b = 0f;
//             newcolor.a = 255f;
//         }

//         like_it.color = newcolor;
//     }
// }
