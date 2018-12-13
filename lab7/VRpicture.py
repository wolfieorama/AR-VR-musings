#!/usr/local/bin/python3

import sys
import numpy as np
import math
import H_builders as Hx
import bmp_io_c

# TBA is in degrees
# t is in focal length units
class VRpicture(object) :
  def __init__(self, TBA, t, image_name, edge_length_col) :
    self.__t = np.copy( t )
    self.__TBA = np.copy( TBA )
    self.__in = image_name
    # cel means "column edge length"
    self.__cel = float( edge_length_col )
    self.__R, self.__C, self.__imgdat = bmp_io_c.input_bmp_c(self.__in)
    R = self.__R
    C = self.__C
    # rel means "row edge length"
    self.__rel = self.__cel * float(R) / C
    self.__wcl = np.zeros( [R*C, 7], np.float32 )
    self.__wcl[:, 4:7] = self.__imgdat.reshape(3, R*C, order='C').T
    self.__H = Hx.bw_build(TBA, t)

    # compute the range over which x and y vary
    x = np.arange(-self.__cel/2., self.__cel/2.,
                   self.__cel / C )
    y = np.arange(-self.__rel/2., self.__rel/2.,
                   self.__rel / R )

    # build picture-sized vector of x values
    tmp = np.ones(R, np.float32)
    x = np.outer(tmp, x).flatten()

    # build picture-sized vector of y values (note the Transpose)
    tmp = np.ones(C, np.float32)
    y = np.outer(tmp, y).T.flatten()

    # build picture-sized vector with z values and also a vector
    # filled with 1's
    z = np.zeros(R*C, np.float32)
    onez = np.ones(R*C, np.float32)

    # row stack the four vectors and multiply by H
    datvecs = self.__H.dot( np.asarray( [x, y, z, onez] ) )
    self.__wcl[:, 0:4] = datvecs.T

  def get_R(self) :
    return self.__R

  def get_C(self) :
    return self.__C

  def get_wc_list(self) :
    return np.copy( self.__wcl )

  def get_H(self) :
    return np.copy( self.__H )

a = VRpicture([0,0,90], 3, "pano1.bmp", 1024)
a.get_wc_list(self)
