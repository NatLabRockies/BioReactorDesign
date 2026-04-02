#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.13.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/home/federico/OpenFOAM/federico-v2406/run/bioreactor_model')

####################################################
##       Begin of NoteBook variables section      ##
####################################################
notebook.set("vessel_height", 0.137)
notebook.set("vessel_trim_rad", 0.012)
notebook.set("vessel_diameter", 0.084)
notebook.set("shaft_height", 0.119)
notebook.set("shaft_diameter", 0.008)
notebook.set("vessel_height", 0.137)
notebook.set("vessel_trim_rad", 0.012)
notebook.set("vessel_diameter", 0.084)
notebook.set("shaft_height", 0.119)
notebook.set("shaft_diameter", 0.008)
####################################################
##        End of NoteBook variables section       ##
####################################################
###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Cylinder_1 = geompy.MakeCylinderRH(0.042, 0.137)
Vessel = geompy.MakeFillet(Cylinder_1, 0.012, geompy.ShapeType["EDGE"], [9])
vessel_top = geompy.MakeVertex(0, 0, 0.137)
vessel_down_dir = geompy.MakeLineTwoPnt(vessel_top, O)
shaft = geompy.MakeCylinder(vessel_top, vessel_down_dir, 0.004, 0.119)
Cylinder_2 = geompy.MakeCylinderRH(0.0135, 0.002)
Box_1 = geompy.MakeBoxDXDYDZ(0.01, 0.0015, 0.01)
Translation_1 = geompy.MakeTranslation(Box_1, 0.009350000000000001, -0.00075, -0.004)
Multi_Rotation_1 = geompy.MultiRotate1DNbTimes(Translation_1, OZ, 6)
Cylinder_3 = geompy.MakeCylinderRH(0.008, 0.0075)
Translation_2 = geompy.MakeTranslation(Cylinder_3, 0, 0, 0.002)
impeller_base = geompy.MakeFuseList([Cylinder_2, Multi_Rotation_1, Translation_2], True, True)
impeller_1 = geompy.MakeTranslation(impeller_base, 0, 0, 0.018)
impeller_2 = geompy.MakeTranslation(impeller_1, 0, 0, 0.03-0.0095)
Translation_3 = geompy.MakeTranslation(vessel_top, 0.035, 0, 0)
ports_centers = geompy.MultiRotate1DNbTimes(Translation_3, None, 10)
[Vertex_1,Vertex_2,Vertex_3,Vertex_4,Vertex_5,Vertex_6,Vertex_7,Vertex_8,Vertex_9,Vertex_10] = geompy.ExtractShapes(ports_centers, geompy.ShapeType["VERTEX"], True)
Cylinder_4 = geompy.MakeCylinder(Vertex_10, vessel_down_dir, 0.003, 0.126)
Disk_1 = geompy.MakeDiskPntVecR(O, OY, 0.003)
Translation_4 = geompy.MakeTranslation(Disk_1, 0.0215, 0, 0.008)
Revolution_1 = geompy.MakeRevolution2Ways(Translation_4, OZ, 150*math.pi/180.0)
[Face_1,Face_2,Face_3] = geompy.ExtractShapes(Revolution_1, geompy.ShapeType["FACE"], True)
Vertex_12 = geompy.MakeVertex(0, 0, 0.013)
Vertex_13 = geompy.MakeVertex(0, 0.001, 0.013)
Line_1 = geompy.MakeLineTwoPnt(Vertex_12, Vertex_13)
Translation_5 = geompy.MakeTranslation(Line_1, 0.028, 0, 0)
Cylinder_5 = geompy.MakeCylinder(Vertex_10, vessel_down_dir, 0.003, 0.118)
[geomObj_1] = geompy.SubShapes(Cylinder_5, [10])
Translation_6 = geompy.MakeTranslation(Translation_5, 0, 0, 0.006)
Revolution_2 = geompy.MakeRevolution(geomObj_1, Translation_6, 60*math.pi/180.0)
[Face_5] = geompy.SubShapes(Revolution_2, [12])
Vector_Normal_1 = geompy.GetNormal(Face_5, Vertex_13)
Extrusion_1 = geompy.MakePrismVecH(Face_5, Vector_Normal_1, 0.012)
Fillet_1 = geompy.MakeFillet(Extrusion_1, 0.001, geompy.ShapeType["EDGE"], [9])
sparger0 = geompy.MakeFuseList([Cylinder_5, Revolution_2, Fillet_1], True, True)
sparger1 = geompy.MakeFuseList([Revolution_1, sparger0], True, True)
thermo = geompy.MakeCylinder(Vertex_9, vessel_down_dir, 0.003, 0.112)
sample = geompy.MakeCylinder(Vertex_2, vessel_down_dir, 0.003, 0.12)
port2 = geompy.MakeCylinder(Vertex_4, vessel_down_dir, 0.005, 0.115)
sample2 = geompy.MakeCylinder(Vertex_1, vessel_down_dir, 0.005, 0.115)
Fillet_2 = geompy.MakeFillet(port2, 0.005, geompy.ShapeType["EDGE"], [5])
Fillet_3 = geompy.MakeFillet(sample2, 0.005, geompy.ShapeType["EDGE"], [5])
Fillet_4 = geompy.MakeFillet(sample, 0.003, geompy.ShapeType["EDGE"], [5])
Fillet_5 = geompy.MakeFillet(thermo, 0.003, geompy.ShapeType["EDGE"], [5])
Vessel.SetColor(SALOMEDS.Color(0.666667,1,1))
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( Vessel, 'Vessel' )
geompy.addToStudy( vessel_top, 'vessel_top' )
geompy.addToStudy( vessel_down_dir, 'vessel_down_dir' )
geompy.addToStudy( shaft, 'shaft' )
geompy.addToStudy( Cylinder_2, 'Cylinder_2' )
geompy.addToStudy( Box_1, 'Box_1' )
geompy.addToStudy( Translation_1, 'Translation_1' )
geompy.addToStudy( Multi_Rotation_1, 'Multi-Rotation_1' )
geompy.addToStudy( Cylinder_3, 'Cylinder_3' )
geompy.addToStudy( Translation_2, 'Translation_2' )
geompy.addToStudy( impeller_base, 'impeller_base' )
geompy.addToStudy( impeller_1, 'impeller_1' )
geompy.addToStudy( impeller_2, 'impeller_2' )
geompy.addToStudy( Translation_3, 'Translation_3' )
geompy.addToStudy( ports_centers, 'ports_centers' )
geompy.addToStudyInFather( ports_centers, Vertex_1, 'Vertex_1' )
geompy.addToStudyInFather( ports_centers, Vertex_2, 'Vertex_2' )
geompy.addToStudyInFather( ports_centers, Vertex_3, 'Vertex_3' )
geompy.addToStudyInFather( ports_centers, Vertex_4, 'Vertex_4' )
geompy.addToStudyInFather( ports_centers, Vertex_5, 'Vertex_5' )
geompy.addToStudyInFather( ports_centers, Vertex_6, 'Vertex_6' )
geompy.addToStudyInFather( ports_centers, Vertex_7, 'Vertex_7' )
geompy.addToStudyInFather( ports_centers, Vertex_8, 'Vertex_8' )
geompy.addToStudyInFather( ports_centers, Vertex_9, 'Vertex_9' )
geompy.addToStudyInFather( ports_centers, Vertex_10, 'Vertex_10' )
geompy.addToStudy( Cylinder_4, 'Cylinder_4' )
geompy.addToStudy( Disk_1, 'Disk_1' )
geompy.addToStudy( Translation_4, 'Translation_4' )
geompy.addToStudy( Revolution_1, 'Revolution_1' )
geompy.addToStudyInFather( Revolution_1, Face_1, 'Face_1' )
geompy.addToStudyInFather( Revolution_1, Face_2, 'Face_2' )
geompy.addToStudyInFather( Revolution_1, Face_3, 'Face_3' )
geompy.addToStudy( Vertex_12, 'Vertex_12' )
geompy.addToStudy( Vertex_13, 'Vertex_13' )
geompy.addToStudy( Line_1, 'Line_1' )
geompy.addToStudy( Translation_5, 'Translation_5' )
geompy.addToStudy( Cylinder_5, 'Cylinder_5' )
geompy.addToStudy( Translation_6, 'Translation_6' )
geompy.addToStudy( Revolution_2, 'Revolution_2' )
geompy.addToStudyInFather( Revolution_2, Face_5, 'Face_5' )
geompy.addToStudy( Vector_Normal_1, 'Vector_Normal_1' )
geompy.addToStudy( Extrusion_1, 'Extrusion_1' )
geompy.addToStudy( Fillet_1, 'Fillet_1' )
geompy.addToStudy( sparger0, 'sparger0' )
geompy.addToStudy( sparger1, 'sparger1' )
geompy.addToStudy( thermo, 'thermo' )
geompy.addToStudy( sample, 'sample' )
geompy.addToStudy( sample2, 'sample2' )
geompy.addToStudy( port2, 'port2' )
geompy.addToStudy( Fillet_2, 'Fillet_2' )
geompy.addToStudy( Fillet_3, 'Fillet_3' )
geompy.addToStudy( Fillet_4, 'Fillet_4' )
geompy.addToStudy( Fillet_5, 'Fillet_5' )


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
