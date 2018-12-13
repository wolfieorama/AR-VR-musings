# -*- coding: utf-8 -*-
'''
@author John Munyi
        David Chuckuma
        Adolphe Ndagijimana
    
    VRCube
    
'''
import numpy as np
from H_builders import bw_build
import VRpicture as pic

'''
Cube class
Arguments:
    Tait-Bryan angles
    translation in focal length units
    center of the cube in world coordinates 
    image_names
    Edge length 
'''
class VRCube():
    def __init__(self, TBA, t, image_names, edge_length_col) :
        #attributes
        self.t_world = t
        self.TBA_world = TBA
        self.image_names = image_names
        self.edge_length_col = edge_length_col
        
        #transform that convert from body to world coordinates
        self.body_to_world = bw_build(self.TBA_world,self.t_world)
        
        # body rotation and translation of sides of the cube
        self.left_body = np.asarray([[90,0,0],[0.5,0,0]])
        self.right_body = np.asarray([[-90,0,0],[-0.5,0,0]])
        self.top_body = np.asarray([[0,-90,0],[0,-1/2,0]])
        self.down_body = np.asarray([[0,90,0],[0,1/2,0]])
        self.behind_body = np.asarray([[180,0,0],[0,0,-1/2]])
        self.front_body = np.asarray([[0,0,0],[0,0,1/2]]) 
        
        # building image of each side
        self.left_image_body = self.build_image(self.left_body[0],self.left_body[1],0)
        self.right_image_body = self.build_image(self.right_body[0],self.right_body[1],1)
        self.top_image_body = self.build_image(self.top_body[0],self.top_body[1],2)
        self.down_image_body = self.build_image(self.down_body[0],self.down_body[1],3)
        self.behind_image_body = self.build_image(self.behind_body[0],self.behind_body[1],4)
        self.front_image_body = self.build_image(self.front_body[0],self.front_body[1],5)
        
        # concatinating all the 6 side images
        self.cube = np.concatenate((self.left_image_body.get_wc_list(),
            self.right_image_body.get_wc_list(),
            self.top_image_body.get_wc_list(),
            self.down_image_body.get_wc_list(),
            self.behind_image_body.get_wc_list(),
            self.front_image_body.get_wc_list()), axis=0)
        
        
        # converting from body coordinates to world coordinates
        self.cube[:,:4] = np.dot(self.body_to_world,self.cube[:,:4].T).T
        
        
    # helper method 
    def build_image(self, TBA, translation,i):
        return pic(TBA, translation, self.image_names[i], self.edge_length_col)
    
    # return homogenous body to world transform
    def get_H(self):
        return self.body_to_world
    
    # returns the cube
    def get_cube(self):
        return self.cube