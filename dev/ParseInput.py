#!/usr/bin/env python

# JACoPO.py: calculation of electronic couplings with various approaches.
# Copyright (C) 2016  Daniele Padula, Marco Campetella
# dpadula85@yahoo.it, marco.campetella82@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import numpy as np

# Constants

au2ang = 0.5291771
au2wn = 2.194746e5

# class CUBE:
#     def __init__(self, fname):
# 
#         f = open(fname, 'r')
#         for i in range(2): f.readline() # echo comment
#         tkns = f.readline().split() # number of atoms included in the file followed by the position of the origin of the volumetric data
#         self.natoms = int(tkns[0])
#         self.origin = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])
# 
#         # The next three lines give the number of voxels along each axis (x, y, z) followed by the axis vector.
#         tkns = f.readline().split() #
#         self.NX = int(tkns[0])
#         self.X = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])
#         tkns = f.readline().split() #
#         self.NY = int(tkns[0])
#         self.Y = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])
#         tkns = f.readline().split() #
#         self.NZ = int(tkns[0])
#         self.Z = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])
# 
#         # The last section in the header is one line for each atom consisting of 5 numbers, the first is the atom number, second (?), the last three are the x,y,z coordinates of the atom center.
#         self.atoms = []
#         for i in range(self.natoms):
#             tkns = map(float, f.readline().split())
#             self.atoms.append([tkns[0], tkns[2], tkns[3], tkns[4]])
# 
#         # Volumetric data
#         self.data = np.zeros((self.NX,self.NY,self.NZ))
#         i=0
#         for s in f:
#             for v in s.split():
#                 self.data[i/(self.NY*self.NZ), (i/self.NZ)%self.NY, i%self.NZ] = float(v)
#                 i+=1
#         if i != self.NX*self.NY*self.NZ: raise NameError, "FSCK!"
# 
# 
#     def dump(self, f):
# 
#         # output Gaussian cube into file descriptor "f".
#         # Usage pattern: f=open('filename.cube'); cube.dump(f); f.close()
#         print >>f, "CUBE file\nGenerated by JACoPO.py"
#         print >>f, "%5d %12.6f %12.6f %12.6f" % (self.natoms, self.origin[0], self.origin[1], self.origin[2])
#         print >>f, "%5d %12.6f %12.6f %12.6f"% (self.NX, self.X[0], self.X[1], self.X[2])
#         print >>f, "%5d %12.6f %12.6f %12.6f"% (self.NY, self.Y[0], self.Y[1], self.Y[2])
#         print >>f, "%5d %12.6f %12.6f %12.6f"% (self.NZ, self.Z[0], self.Z[1], self.Z[2])
#         for atom in self.atoms:
#             print >>f, "%5d %12.6f %12.6f %12.6f %12.6f" % (atom[0], atom[0], atom[1], atom[2], atom[3])
#         for ix in xrange(self.NX):
#             for iy in xrange(self.NY):
#                 for iz in xrange(self.NZ):
#                     print >>f, "%.5e " % self.data[ix,iy,iz],
#                     if (iz % 6 == 5): print >>f, ''
#                 #print >>f,  ""
# 
# 
#     def mask_sphere(self, R, Cx,Cy,Cz):
# 
#         # produce spheric volume mask with radius R and center @ [Cx,Cy,Cz]
#         # can be used for integration over spherical part of the volume
#         m=0*self.data
#         for ix in xrange( int(ceil((Cx-R)/self.X[0])), int(floor((Cx+R)/self.X[0])) ):
#             ryz=np.sqrt(R**2-(ix*self.X[0]-Cx)**2)
#             for iy in xrange( int(ceil((Cy-ryz)/self.Y[1])), int(floor((Cy+ryz)/self.Y[1])) ):
#                 rz=np.sqrt(ryz**2 - (iy*self.Y[1]-Cy)**2)
#                 for iz in xrange( int(ceil((Cz-rz)/self.Z[2])), int(floor((Cz+rz)/self.Z[2])) ):
#                     m[ix,iy,iz]=1
#         return m


class Cube:
    def __init__(self, fname):

        f = open(fname, 'r')
        for i in range(2): f.readline() # echo comment
        tkns = f.readline().split() # number of atoms included in the file followed by the position of the origin of the volumetric data
        self.natoms = int(tkns[0])
        self.origin = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])

        # The next three lines give the number of voxels along each axis (x, y, z) followed by the axis vector.
        tkns = f.readline().split() #
        self.NX = int(tkns[0])
        self.X = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])
        tkns = f.readline().split() #
        self.NY = int(tkns[0])
        self.Y = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])
        tkns = f.readline().split() #
        self.NZ = int(tkns[0])
        self.Z = np.array([float(tkns[1]),float(tkns[2]),float(tkns[3])])

        # The last section in the header is one line for each atom consisting of 5 numbers, the first is the atom number, second (?), the last three are the x,y,z coordinates of the atom center.
        self.atoms = []
        for i in range(self.natoms):
            tkns = map(float, f.readline().split())
            self.atoms.append([tkns[0], tkns[2], tkns[3], tkns[4]])

        # Other data
        self.atoms = np.array(self.atoms)
        self.grid = self.gen_grid()
        self.dV = self.X[0] * self.Y[1] * self.Z[2]
        self.coords = np.array([ [x[1], x[2], x[3]] for x in self.atoms ]) * au2ang

        # Volumetric data
        self.data = np.zeros((self.NX,self.NY,self.NZ))
        i=0
        for s in f:
            for v in s.split():
                self.data[i/(self.NY*self.NZ), (i/self.NZ)%self.NY, i%self.NZ] = float(v)
                i+=1

        self.data = self.data.reshape(self.NX * self.NY * self.NZ)
        if i != self.NX*self.NY*self.NZ: raise NameError, "FSCK!"


    def gen_grid(self):

        grid = np.zeros((self.NX, self.NY, self.NZ, 3))
        for i in range(self.NX):
            for j in range(self.NY):
                for k in range(self.NZ):
                    grid[i,j,k,0] = self.origin[0] + i * self.X[0]
                    grid[i,j,k,1] = self.origin[1] + j * self.Y[1]
                    grid[i,j,k,2] = self.origin[2] + k * self.Z[2]

        N = self.NX * self.NY * self.NZ
        return grid.reshape(N, 3)


    def dump(self, f):

        # output Gaussian cube into file descriptor "f".
        # Usage pattern: f=open('filename.cube'); cube.dump(f); f.close()
        self.data = self.data.reshape(self.NX, self.NY, self.NZ)
        print >>f, "CUBE file\nGenerated by JACoPO.py"
        print >>f, "%5d %12.6f %12.6f %12.6f" % (self.natoms, self.origin[0], self.origin[1], self.origin[2])
        print >>f, "%5d %12.6f %12.6f %12.6f"% (self.NX, self.X[0], self.X[1], self.X[2])
        print >>f, "%5d %12.6f %12.6f %12.6f"% (self.NY, self.Y[0], self.Y[1], self.Y[2])
        print >>f, "%5d %12.6f %12.6f %12.6f"% (self.NZ, self.Z[0], self.Z[1], self.Z[2])
        for atom in self.atoms:
            print >>f, "%5d %12.6f %12.6f %12.6f %12.6f" % (atom[0], atom[0], atom[1], atom[2], atom[3])
        for ix in xrange(self.NX):
            for iy in xrange(self.NY):
                for iz in xrange(self.NZ):
                    print >>f, "%.5e " % self.data[ix,iy,iz],
                    if (iz % 6 == 5): print >>f, ''
                #print >>f,  ""

# def read_cub(cubfile):
# 
#     checkfile(cubfile)
#     TrDen1 = CUBE(cubfile)
#     
#     TrD1 = np.asfortranarray(TrDen1.data)
#     
#     # structure
#     struct1 = np.array(TrDen1.atoms)
#     
#     # calculate the volume element
#     dVx1 = TrDen1.X[0]
#     dVy1 = TrDen1.Y[1]
#     dVz1 = TrDen1.Z[2]
#     
#     # Grid points
#     NX1 = TrDen1.NX
#     NY1 = TrDen1.NY
#     NZ1 = TrDen1.NZ
#     
#     # Origin of the cube
#     O1 = TrDen1.origin
# 
#     return TrD1, dVx1, dVy1, dVz1, NX1, NY1, NZ1, O1, struct1


def read_geo(geofile):

    checkfile(geofile)
    atgeo = np.loadtxt(geofile, usecols=[0], dtype="|S5")
    structgeo = np.loadtxt(geofile, usecols=[1,2,3]) / au2ang

    return atgeo, structgeo


def read_chg(chgfile):

    checkfile(chgfile)
    chgs = np.loadtxt(chgfile)

    return chgs


def read_sel(string):

    string =  ','.join(string).replace(',,',',')

    try:
        f = open(string, 'r')
        string = f.readlines()
        f.close()
        string =  ','.join(string).replace(',,',',')
        string = string.replace(',', ' ')
        string = map(lambda x: x - 1, extend_compact_list(string))

    except IOError:
        string = string.replace(',', ' ')
        string = map(lambda x: x - 1, extend_compact_list(string))

    return string


def extend_compact_list(idxs):

    extended = []

    # Uncomment this line if idxs is a string and not a list
    idxs = idxs.split()

    for idx in idxs:

        to_extend = idx.split('-')

        if len(to_extend) > 1:

            sel =  map(int, to_extend)
            extended += range(sel[0],sel[1]+1,1)

        else:
        
            extended.append(int(idx))
    
    return extended


def checkfile(filename):

    if not os.path.isfile(filename):
        print(banner(text='ERROR', ch='#', length=80))
        print("File %s not found!" % filename)
        sys.exit()


def banner(text=None, ch='=', length=78):
    """Return a banner line centering the given text.
    
        "text" is the text to show in the banner. None can be given to have
            no text.
        "ch" (optional, default '=') is the banner line character (can
            also be a short string to repeat).
        "length" (optional, default 78) is the length of banner to make.

    Examples:
        >>> banner("Peggy Sue")
        '================================= Peggy Sue =================================='
        >>> banner("Peggy Sue", ch='-', length=50)
        '------------------- Peggy Sue --------------------'
        >>> banner("Pretty pretty pretty pretty Peggy Sue", length=40)
        'Pretty pretty pretty pretty Peggy Sue'
    """
    if text is None:
        return ch * length

    elif len(text) + 2 + len(ch)*2 > length:
        # Not enough space for even one line char (plus space) around text.
        return text

    else:
        remain = length - (len(text) + 2)
        prefix_len = remain / 2
        suffix_len = remain - prefix_len
    
        if len(ch) == 1:
            prefix = ch * prefix_len
            suffix = ch * suffix_len

        else:
            prefix = ch * (prefix_len/len(ch)) + ch[:prefix_len%len(ch)]
            suffix = ch * (suffix_len/len(ch)) + ch[:suffix_len%len(ch)]

        return prefix + ' ' + text + ' ' + suffix


if __name__ == '__main__':
    pass
