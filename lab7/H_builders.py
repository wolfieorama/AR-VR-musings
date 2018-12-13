#!/usr/local/bin/python3
import sys
import numpy as np
import math

#############################
# These routines are used to build H matrices for
# coordinate conversions and projections.  They produce
# matrices for use with homogenous coordinates
#############################

# TBA is the Tait-Bryan angles in the order phi, theta, psi.
# The input angles are in DEGREES not radians
# t is a translation vector

# Body to world conversion
# Returns a 4x4 homogenous matrix
def bw_build( TBA, t ) :
  Ry = Ry_build( TBA[0] * math.pi / 180 )
  Rx = Rx_build( TBA[1] * math.pi / 180 )
  Rz = Rz_build( TBA[2] * math.pi / 180 )
  Rc = Ry.dot( Rx.dot(Rz) )
  H = np.zeros( [4, 4], np.float64 )

  H[0:3, 0:3] = Rc[:,:]
  H[0:3, 3] = t
  H[3, 3] = 1
  return H

# World to body conversion
# Returns a 4x4 homogenous matrix
def wb_build( TBA, t ) :
  Ry = Ry_build( TBA[0] * math.pi / 180 )
  Rx = Rx_build( TBA[1] * math.pi / 180 )
  Rz = Rz_build( TBA[2] * math.pi / 180 )
  Rc = Ry.dot( Rx.dot(Rz) )
  RcT = Rc.T
  H = np.zeros( [4, 4], np.float64 )

  H[0:3, 0:3] = RcT[:,:]
  H[0:3, 3] = -RcT.dot(t)
  H[3, 3] = 1
  return H

# Camera projection matrix
# Returns a 3x4 homogenous matrix
def projection_build(eta, f, c1, c2) :
  H = np.zeros( [3, 4], np.float64 )
  H[0, 0] = eta * f
  H[1, 1] = eta * f
  H[2, 2] = 1
  H[0, 2] = c1
  H[1, 2] = c2
  return H

######
# These methods build the elemental rotation matrices
######
def Rx_build( theta ) :
  Rx = np.asarray( [ [1, 0, 0], \
                     [0, math.cos( theta ), -math.sin(theta) ], \
                     [0, math.sin( theta ),  math.cos(theta) ]], \
                     np.float64 )
  return Rx                   

def Ry_build( phi ) :
  Ry = np.asarray( [ [math.cos(phi), 0, math.sin(phi)], \
                     [0, 1, 0], \
                     [-math.sin( phi ), 0, math.cos(phi) ]], \
                     np.float64 )
  return Ry                   

def Rz_build( psi ) :
  Rz = np.asarray( [ [math.cos(psi), -math.sin(psi), 0], \
                     [math.sin(psi),  math.cos(psi), 0], \
                     [0, 0, 1]], \
                     np.float64 )
  return Rz                   
