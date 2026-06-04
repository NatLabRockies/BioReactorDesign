#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.13.0 with dump python functionality
###

import sys

import salome

salome.salome_init()
import salome_notebook

notebook = salome_notebook.NoteBook()
sys.path.insert(0, r"/home/federico/OpenFOAM/federico-13/run")

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

import math

import GEOM
import SALOMEDS
from salome.geom import geomBuilder

geompy = geomBuilder.New()

geomObj_1 = geompy.MakeVertex(0, 0, 0)
geomObj_2 = geompy.MakeVectorDXDYDZ(1, 0, 0)
geomObj_3 = geompy.MakeVectorDXDYDZ(0, 1, 0)
geomObj_4 = geompy.MakeVectorDXDYDZ(0, 0, 1)
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Cylinder_1 = geompy.MakeCylinderRH(0.042, 0.137)
Vessel_vol = geompy.MakeFillet(
    Cylinder_1, 0.012, geompy.ShapeType["EDGE"], [9]
)
vessel_top = geompy.MakeVertex(0, 0, 0.137)
vessel_down_dir = geompy.MakeLineTwoPnt(vessel_top, O)
shaftLong = geompy.MakeCylinder(vessel_top, vessel_down_dir, 0.004, 0.1055)
Cylinder_2 = geompy.MakeCylinderRH(0.0135, 0.002)
Box_1 = geompy.MakeBoxDXDYDZ(0.0105, 0.0015, 0.008999999999999999)
Translation_1 = geompy.MakeTranslation(
    Box_1, 0.009350000000000001, -0.00075, -0.004
)
Multi_Rotation_1 = geompy.MultiRotate1DNbTimes(Translation_1, OZ, 6)
Cylinder_3 = geompy.MakeCylinderRH(0.008, 0.0075)
Translation_2 = geompy.MakeTranslation(Cylinder_3, 0, 0, 0.002)
impeller_base = geompy.MakeFuseList(
    [Cylinder_2, Multi_Rotation_1, Translation_2], True, True
)
impeller_1 = geompy.MakeTranslation(impeller_base, 0, 0, 0.03)
impeller_2 = geompy.MakeTranslation(impeller_1, 0, 0, 0.018)
Translation_3 = geompy.MakeTranslation(vessel_top, 0.035, 0, 0)
ports_centers = geompy.MultiRotate1DNbTimes(Translation_3, None, 10)
[
    Vertex_1,
    Vertex_2,
    Vertex_3,
    Vertex_4,
    Vertex_5,
    Vertex_6,
    Vertex_7,
    Vertex_8,
    Vertex_9,
    Vertex_10,
] = geompy.ExtractShapes(ports_centers, geompy.ShapeType["VERTEX"], True)
[
    Vertex_11,
    Vertex_12,
    Vertex_13,
    Vertex_14,
    Vertex_15,
    Vertex_16,
    Vertex_17,
    Vertex_18,
    Vertex_19,
    Vertex_20,
] = geompy.ExtractShapes(ports_centers, geompy.ShapeType["VERTEX"], True)
Cylinder_4 = geompy.MakeCylinder(Vertex_10, vessel_down_dir, 0.003, 0.126)
Disk_1 = geompy.MakeDiskPntVecR(O, OY, 0.003)
Translation_4 = geompy.MakeTranslation(Disk_1, 0.0215, 0, 0.008)
thermo = geompy.MakeCylinder(Vertex_9, vessel_down_dir, 0.003, 0.112)
sample = geompy.MakeCylinder(Vertex_2, vessel_down_dir, 0.003, 0.12)
port2 = geompy.MakeCylinder(Vertex_4, vessel_down_dir, 0.005, 0.115)
sample2 = geompy.MakeCylinder(Vertex_1, vessel_down_dir, 0.005, 0.115)
Fillet_2 = geompy.MakeFillet(port2, 0.005, geompy.ShapeType["EDGE"], [5])
Fillet_3 = geompy.MakeFillet(sample2, 0.005, geompy.ShapeType["EDGE"], [5])
Fillet_4 = geompy.MakeFillet(sample, 0.003, geompy.ShapeType["EDGE"], [5])
Fillet_5 = geompy.MakeFillet(thermo, 0.003, geompy.ShapeType["EDGE"], [5])
rotatingZone0 = geompy.MakeCylinderRH(0.023, 0.035)
rotatingZone = geompy.MakeTranslation(rotatingZone0, 0, 0, 0.025)
Disk_2 = geompy.MakeDiskPntVecR(Vertex_8, OZ, 0.005)
Disk_3 = geompy.MakeDiskPntVecR(Vertex_6, OZ, 0.005)
Disk_4 = geompy.MakeDiskPntVecR(Vertex_3, OZ, 0.005)
Disk_5 = geompy.MakeDiskPntVecR(Vertex_5, OZ, 0.005)
Disk_6 = geompy.MakeDiskPntVecR(Vertex_7, OZ, 0.005)
geomObj_5 = geompy.MakeRevolution(Translation_4, OZ, 360 * math.pi / 180.0)
geomObj_6 = geompy.MakeVertex(0.035, 0, 0.015)
geomObj_7 = geompy.MakeVertex(0.03, 0, 0.011)
geomObj_8 = geompy.MakeVertex(0.022, 0, 0.008)
geomObj_9 = geompy.GetSubShape(geomObj_5, [6])
geomObj_10 = geompy.MakeDiskPntVecR(Vertex_10, OZ, 0.003)
geomObj_11 = geompy.MakePrismVecH(geomObj_10, OZ, -0.129)
geomObj_12 = geompy.MakeVertex(0.035, 0, 0.008)
geomObj_13 = geompy.MakeVertex(0.0215, 0, 0.008)
geomObj_14 = geompy.MakeSpherePntR(geomObj_12, 0.003)
geomObj_15 = geompy.MakeLineTwoPnt(geomObj_13, geomObj_12)
geomObj_16 = geompy.MakeCylinder(geomObj_13, geomObj_15, 0.003, 0.013)
geomObj_17 = geompy.MakeFuseList(
    [geomObj_5, geomObj_11, geomObj_14, geomObj_16], True, True
)
[geomObj_18] = geompy.ExtractShapes(
    geomObj_17, geompy.ShapeType["SHELL"], True
)
geomObj_19 = geompy.MakeVertex(0, 0.0215, 0.011)
geomObj_20 = geompy.MakeDiskPntVecR(geomObj_19, OZ, 0.001)
Extrusion_3 = geompy.MakePrismVecH(Disk_5, OZ, 0.005)
vessel = geompy.MakeFuseList([Vessel_vol, Extrusion_3], True, True)
outlet = geompy.CreateGroup(vessel, geompy.ShapeType["FACE"])
geompy.UnionIDs(outlet, [27])
vessel_1 = geompy.CreateGroup(vessel, geompy.ShapeType["FACE"])
geompy.UnionIDs(vessel_1, [10, 3, 20, 15, 22])
[outlet, vessel_1] = geompy.GetExistingSubObjects(vessel, False)
Fuse_2 = geompy.MakeFuseList([shaftLong, impeller_1, impeller_2], True, True)
shaft = geompy.MakeCutList(Fuse_2, [rotatingZone], True)
stirrer = geompy.MakeCutList(Fuse_2, [shaft], True)
geomObj_21 = geompy.MakeCylinderRH(0.025, 0.005)
geomObj_22 = geompy.MakeTranslation(geomObj_21, 0, 0, 0.0105)
geomObj_23 = geompy.MakeCutList(geomObj_5, [geomObj_22], True)
Revolution_1 = geompy.MakeRevolution(Translation_4, OZ, 360 * math.pi / 180.0)
Cylinder_5 = geompy.MakeCylinder(Vertex_20, vessel_down_dir, 0.0025, 0.12)
Translation_5 = geompy.MakeTranslation(Vertex_20, 0, 0, -0.12)
Sphere_1 = geompy.MakeSpherePntR(Translation_5, 0.0025)
Vertex_21 = geompy.MakeVertex(0.025, 0, 0.007)
Line_1 = geompy.MakeLineTwoPnt(Vertex_21, Translation_5)
Line_1_vertex_2 = geompy.GetSubShape(Line_1, [2])
Sphere_2 = geompy.MakeSpherePntR(Line_1_vertex_2, 0.0025)
Sphere_1_vertex_8 = geompy.GetSubShape(Sphere_1, [8])
Disk_7 = geompy.MakeDiskPntVecR(Translation_5, Line_1, 0.0025)
Extrusion_1 = geompy.MakePrism(Disk_7, Translation_5, Vertex_21)
Cylinder_6 = geompy.MakeCylinderRH(0.0245, 0.003)
Translation_6 = geompy.MakeTranslation(Cylinder_6, 0, 0, 0.0108)
Cut_1 = geompy.MakeCutList(Revolution_1, [Translation_6], True)
sparger = geompy.MakeFuseList(
    [Cylinder_5, Sphere_1, Sphere_2, Extrusion_1, Cut_1], True, True
)
inlet = geompy.CreateGroup(sparger, geompy.ShapeType["FACE"])
geompy.UnionIDs(inlet, [46])
sparger_1 = geompy.CreateGroup(sparger, geompy.ShapeType["FACE"])
geompy.UnionIDs(sparger_1, [3, 18, 24, 26, 37, 39, 41, 46])
[inlet, sparger_1] = geompy.GetExistingSubObjects(sparger, False)
vessel_top_1 = geompy.CreateGroup(Vessel_vol, geompy.ShapeType["FACE"])
geompy.UnionIDs(vessel_top_1, [15])
Group_1 = geompy.CreateGroup(Vessel_vol, geompy.ShapeType["FACE"])
geompy.UnionIDs(Group_1, [3, 10, 17])
geompy.DifferenceIDs(sparger_1, [3, 18, 24, 26, 37, 39, 41, 46])
geompy.UnionIDs(sparger_1, [3, 18, 24, 26, 37, 39, 41])
Cut_2 = geompy.MakeCutList(
    vessel,
    [Fillet_2, Fillet_3, Fillet_4, Fillet_5, shaft, stirrer, sparger],
    True,
)
fluid_volume = geompy.MakePartition(
    [Cut_2], [rotatingZone], [], [], geompy.ShapeType["SOLID"], 0, [], 0
)
inlet_1 = geompy.CreateGroup(fluid_volume, geompy.ShapeType["FACE"])
geompy.UnionIDs(inlet_1, [144])
outlet_1 = geompy.CreateGroup(fluid_volume, geompy.ShapeType["FACE"])
geompy.UnionIDs(outlet_1, [112])
shaft_1 = geompy.CreateGroup(fluid_volume, geompy.ShapeType["FACE"])
geompy.UnionIDs(shaft_1, [51])
stirrer_1 = geompy.CreateGroup(fluid_volume, geompy.ShapeType["FACE"])
geompy.UnionIDs(
    stirrer_1,
    [
        374,
        486,
        835,
        790,
        271,
        437,
        820,
        266,
        215,
        289,
        348,
        276,
        848,
        230,
        490,
        599,
        684,
        815,
        149,
        826,
        468,
        818,
        464,
        779,
        484,
        459,
        625,
        302,
        813,
        809,
        862,
        325,
        756,
        431,
        338,
        453,
        589,
        648,
        475,
        831,
        807,
        235,
        457,
        851,
        842,
        733,
        508,
        857,
        523,
        840,
        630,
        361,
        513,
        612,
        697,
        859,
        410,
        796,
        720,
        837,
        594,
        671,
        307,
        379,
        518,
        415,
        481,
        448,
        574,
        738,
        853,
        702,
        769,
        495,
        743,
        829,
        846,
        253,
        397,
        666,
        824,
        240,
        154,
        451,
        462,
        804,
        473,
        164,
        470,
        492,
        794,
        479,
        420,
        661,
        159,
        312,
        503,
        506,
        435,
        501,
        635,
        384,
        707,
        343,
        774,
        497,
    ],
)
static = geompy.CreateGroup(fluid_volume, geompy.ShapeType["SOLID"])
geompy.UnionIDs(static, [2])
rotating = geompy.CreateGroup(fluid_volume, geompy.ShapeType["SOLID"])
geompy.UnionIDs(rotating, [147])
walls = geompy.CreateGroup(fluid_volume, geompy.ShapeType["FACE"])
geompy.UnionIDs(
    walls,
    [
        4,
        65,
        11,
        95,
        139,
        124,
        56,
        135,
        105,
        107,
        39,
        75,
        114,
        41,
        80,
        46,
        85,
        16,
        70,
    ],
)
[inlet_1, outlet_1, shaft_1, stirrer_1, static, rotating, walls] = (
    geompy.GetExistingSubObjects(fluid_volume, False)
)
faceRotating = geompy.CreateGroup(fluid_volume, geompy.ShapeType["FACE"])
geompy.UnionIDs(faceRotating, [119, 90, 137])
Vessel_vol.SetColor(SALOMEDS.Color(0.666667, 1, 1))
fluid_volume.SetColor(SALOMEDS.Color(1, 1, 1))
geompy.addToStudyInFather(ports_centers, Vertex_20, "Vertex_20")
geompy.addToStudy(vessel_top, "vessel_top")
geompy.addToStudy(O, "O")
geompy.addToStudy(vessel_down_dir, "vessel_down_dir")
geompy.addToStudy(Cylinder_5, "Cylinder_5")
geompy.addToStudy(Translation_5, "Translation_5")
geompy.addToStudy(Sphere_1, "Sphere_1")
geompy.addToStudy(Vertex_21, "Vertex_21")
geompy.addToStudy(Line_1, "Line_1")
geompy.addToStudyInFather(Line_1, Line_1_vertex_2, "Line_1:vertex_2")
geompy.addToStudy(Sphere_2, "Sphere_2")
geompy.addToStudy(Disk_7, "Disk_7")
geompy.addToStudy(Extrusion_1, "Extrusion_1")
geompy.addToStudy(OZ, "OZ")
geompy.addToStudy(OY, "OY")
geompy.addToStudy(Disk_1, "Disk_1")
geompy.addToStudy(Translation_4, "Translation_4")
geompy.addToStudy(Revolution_1, "Revolution_1")
geompy.addToStudy(Cylinder_6, "Cylinder_6")
geompy.addToStudy(Translation_6, "Translation_6")
geompy.addToStudy(Cut_1, "Cut_1")
geompy.addToStudy(sparger, "sparger")
geompy.addToStudyInFather(Sphere_1, Sphere_1_vertex_8, "Sphere_1:vertex_8")
geompy.addToStudyInFather(sparger, inlet, "inlet")
geompy.addToStudyInFather(sparger, sparger_1, "sparger")
geompy.addToStudy(Cylinder_1, "Cylinder_1")
geompy.addToStudy(Vessel_vol, "Vessel_vol")
geompy.addToStudyInFather(Vessel_vol, vessel_top_1, "vessel_top")
geompy.addToStudyInFather(Vessel_vol, Group_1, "Group_1")
geompy.addToStudyInFather(ports_centers, Vertex_11, "Vertex_11")
geompy.addToStudyInFather(ports_centers, Vertex_12, "Vertex_12")
geompy.addToStudyInFather(ports_centers, Vertex_13, "Vertex_13")
geompy.addToStudyInFather(ports_centers, Vertex_14, "Vertex_14")
geompy.addToStudyInFather(ports_centers, Vertex_15, "Vertex_15")
geompy.addToStudyInFather(ports_centers, Vertex_16, "Vertex_16")
geompy.addToStudyInFather(ports_centers, Vertex_17, "Vertex_17")
geompy.addToStudyInFather(ports_centers, Vertex_18, "Vertex_18")
geompy.addToStudyInFather(ports_centers, Vertex_19, "Vertex_19")
geompy.addToStudy(OX, "OX")
geompy.addToStudy(shaftLong, "shaftLong")
geompy.addToStudy(Cylinder_2, "Cylinder_2")
geompy.addToStudy(Box_1, "Box_1")
geompy.addToStudy(Translation_1, "Translation_1")
geompy.addToStudy(Multi_Rotation_1, "Multi-Rotation_1")
geompy.addToStudy(Cylinder_3, "Cylinder_3")
geompy.addToStudy(Translation_2, "Translation_2")
geompy.addToStudy(impeller_base, "impeller_base")
geompy.addToStudy(impeller_1, "impeller_1")
geompy.addToStudy(impeller_2, "impeller_2")
geompy.addToStudy(Translation_3, "Translation_3")
geompy.addToStudy(ports_centers, "ports_centers")
geompy.addToStudyInFather(ports_centers, Vertex_1, "Vertex_1")
geompy.addToStudyInFather(ports_centers, Vertex_2, "Vertex_2")
geompy.addToStudyInFather(ports_centers, Vertex_3, "Vertex_3")
geompy.addToStudyInFather(ports_centers, Vertex_4, "Vertex_4")
geompy.addToStudyInFather(ports_centers, Vertex_5, "Vertex_5")
geompy.addToStudyInFather(ports_centers, Vertex_6, "Vertex_6")
geompy.addToStudyInFather(ports_centers, Vertex_7, "Vertex_7")
geompy.addToStudyInFather(ports_centers, Vertex_8, "Vertex_8")
geompy.addToStudyInFather(ports_centers, Vertex_9, "Vertex_9")
geompy.addToStudyInFather(ports_centers, Vertex_10, "Vertex_10")
geompy.addToStudy(Cylinder_4, "Cylinder_4")
geompy.addToStudy(thermo, "thermo")
geompy.addToStudy(sample, "sample")
geompy.addToStudy(port2, "port2")
geompy.addToStudy(sample2, "sample2")
geompy.addToStudy(Fillet_2, "Fillet_2")
geompy.addToStudy(Fillet_3, "Fillet_3")
geompy.addToStudy(Fillet_4, "Fillet_4")
geompy.addToStudy(Fillet_5, "Fillet_5")
geompy.addToStudy(rotatingZone0, "rotatingZone0")
geompy.addToStudy(rotatingZone, "rotatingZone")
geompy.addToStudy(Disk_2, "Disk_2")
geompy.addToStudy(Disk_3, "Disk_3")
geompy.addToStudy(Disk_4, "Disk_4")
geompy.addToStudy(Disk_5, "Disk_5")
geompy.addToStudy(Disk_6, "Disk_6")
geompy.addToStudy(Extrusion_3, "Extrusion_3")
geompy.addToStudy(vessel, "vessel")
geompy.addToStudyInFather(vessel, outlet, "outlet")
geompy.addToStudyInFather(vessel, vessel_1, "vessel")
geompy.addToStudy(Fuse_2, "Fuse_2")
geompy.addToStudy(shaft, "shaft")
geompy.addToStudy(stirrer, "stirrer")
geompy.addToStudy(Cut_2, "Cut_2")
geompy.addToStudy(fluid_volume, "fluid_volume")
geompy.addToStudyInFather(fluid_volume, inlet_1, "inlet")
geompy.addToStudyInFather(fluid_volume, outlet_1, "outlet")
geompy.addToStudyInFather(fluid_volume, shaft_1, "shaft")
geompy.addToStudyInFather(fluid_volume, stirrer_1, "stirrer")
geompy.addToStudyInFather(fluid_volume, static, "static")
geompy.addToStudyInFather(fluid_volume, rotating, "rotating")
geompy.addToStudyInFather(fluid_volume, walls, "walls")
geompy.addToStudyInFather(fluid_volume, faceRotating, "faceRotating")
geompy.hideInStudy(Vertex_9)
geompy.hideInStudy(Vertex_10)
geompy.hideInStudy(Vertex_1)
geompy.hideInStudy(Vertex_2)
geompy.hideInStudy(Vertex_3)
geompy.hideInStudy(Vertex_4)
geompy.hideInStudy(Vertex_5)
geompy.hideInStudy(Vertex_6)
geompy.hideInStudy(Vertex_7)
geompy.hideInStudy(Vertex_8)

###
### SMESH component
###

import SALOMEDS
import SMESH
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
# smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
# multiples meshes built in parallel, complex and numerous mesh edition (performance)

NETGEN_2D_Parameters_1 = smesh.CreateHypothesis(
    "NETGEN_Parameters_2D", "NETGENEngine"
)
NETGEN_2D_Parameters_1.SetMinSize(0.00139449)
NETGEN_2D_Parameters_1.SetSecondOrder(0)
NETGEN_2D_Parameters_1.SetOptimize(1)
NETGEN_2D_Parameters_1.SetFineness(3)
NETGEN_2D_Parameters_1.SetChordalError(-1)
NETGEN_2D_Parameters_1.SetChordalErrorEnabled(0)
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature(1)
NETGEN_2D_Parameters_1.SetFuseEdges(1)
NETGEN_2D_Parameters_1.SetWorstElemMeasure(0)
NETGEN_2D_Parameters_1.SetUseDelauney(0)
NETGEN_2D_Parameters_1.SetQuadAllowed(0)
NETGEN_1D_2D = smesh.CreateHypothesis("NETGEN_2D", "NETGENEngine")
NETGEN_2D_Parameters_2 = smesh.CreateHypothesis(
    "NETGEN_Parameters_2D", "NETGENEngine"
)
NETGEN_2D_Parameters_2.SetMaxSize(0.001)
NETGEN_2D_Parameters_2.SetMinSize(2.32381e-05)
NETGEN_2D_Parameters_2.SetSecondOrder(0)
NETGEN_2D_Parameters_2.SetOptimize(1)
NETGEN_2D_Parameters_2.SetFineness(4)
NETGEN_2D_Parameters_2.SetChordalError(-1)
NETGEN_2D_Parameters_2.SetChordalErrorEnabled(0)
NETGEN_2D_Parameters_2.SetUseSurfaceCurvature(1)
NETGEN_2D_Parameters_2.SetFuseEdges(1)
NETGEN_2D_Parameters_2.SetWorstElemMeasure(0)
NETGEN_2D_Parameters_2.SetUseDelauney(0)
NETGEN_2D_Parameters_2.SetQuadAllowed(0)
NETGEN_2D_Parameters_1.SetMaxSize(0.002)
try:
    pass
except:
    print("ExportSTL() failed. Invalid file name?")
try:
    pass
except:
    print("ExportPartToSTL() failed. Invalid file name?")
try:
    pass
except:
    print("ExportPartToSTL() failed. Invalid file name?")
try:
    pass
except:
    print("ExportSTL() failed. Invalid file name?")
try:
    pass
except:
    print("ExportSTL() failed. Invalid file name?")
try:
    pass
except:
    print("ExportSTL() failed. Invalid file name?")
try:
    pass
except:
    print("ExportPartToSTL() failed. Invalid file name?")
try:
    pass
except:
    print("ExportPartToSTL() failed. Invalid file name?")
try:
    pass
except:
    print("ExportSTL() failed. Invalid file name?")
try:
    pass
except:
    print("ExportPartToSTL() failed. Invalid file name?")
try:
    pass
except:
    print("ExportPartToSTL() failed. Invalid file name?")
STR = smesh.Mesh(fluid_volume, "STR")
NETGEN_1D_2D_3D = STR.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_standard = NETGEN_1D_2D_3D.Parameters()
NETGEN_3D_standard.SetMaxSize(0.02)
NETGEN_3D_standard.SetMinSize(0.001)
NETGEN_3D_standard.SetSecondOrder(0)
NETGEN_3D_standard.SetOptimize(1)
NETGEN_3D_standard.SetFineness(2)
NETGEN_3D_standard.SetChordalError(-1)
NETGEN_3D_standard.SetChordalErrorEnabled(0)
NETGEN_3D_standard.SetUseSurfaceCurvature(1)
NETGEN_3D_standard.SetFuseEdges(1)
NETGEN_3D_standard.SetQuadAllowed(0)
NETGEN_3D_standard.SetCheckChartBoundary(4)
inlet_2 = STR.GroupOnGeom(inlet_1, "inlet", SMESH.FACE)
outlet_2 = STR.GroupOnGeom(outlet_1, "outlet", SMESH.FACE)
shaft_2 = STR.GroupOnGeom(shaft_1, "shaft", SMESH.FACE)
stirrer_2 = STR.GroupOnGeom(stirrer_1, "stirrer", SMESH.FACE)
static_1 = STR.GroupOnGeom(static, "static", SMESH.VOLUME)
rotating_1 = STR.GroupOnGeom(rotating, "rotating", SMESH.VOLUME)
walls_1 = STR.GroupOnGeom(walls, "walls", SMESH.FACE)
[inlet_2, outlet_2, shaft_2, stirrer_2, static_1, rotating_1, walls_1] = (
    STR.GetGroups()
)
status = STR.RemoveHypothesis(NETGEN_3D_standard)
NETGEN_3D_finer = NETGEN_1D_2D_3D.Parameters()
NETGEN_3D_finer.SetSecondOrder(0)
NETGEN_3D_finer.SetOptimize(1)
NETGEN_3D_finer.SetChordalError(-1)
NETGEN_3D_finer.SetChordalErrorEnabled(0)
NETGEN_3D_finer.SetUseSurfaceCurvature(1)
NETGEN_3D_finer.SetFuseEdges(1)
NETGEN_3D_finer.SetQuadAllowed(0)
NETGEN_3D_finer.SetFineness(3)
[inlet_2, outlet_2, shaft_2, stirrer_2, static_1, rotating_1, walls_1] = (
    STR.GetGroups()
)
NETGEN_3D_finer.SetMinSize(0.0008)
[inlet_2, outlet_2, shaft_2, stirrer_2, static_1, rotating_1, walls_1] = (
    STR.GetGroups()
)
NETGEN_3D_finer.SetMaxSize(0.002)
NETGEN_3D_finer.SetCheckChartBoundary(93)
[inlet_2, outlet_2, shaft_2, stirrer_2, static_1, rotating_1, walls_1] = (
    STR.GetGroups()
)
try:
    STR.ExportUNV(
        r"/home/federico/OpenFOAM/federico-13/run/STR_tetra/constant/geometry/salome/STR_finer.unv",
        0,
    )
    pass
except:
    print("ExportUNV() failed. Invalid file name?")  ### not created Object
[inlet_2, outlet_2, shaft_2, stirrer_2, static_1, rotating_1, walls_1] = (
    STR.GetGroups()
)
faceRotating_1 = STR.GroupOnGeom(faceRotating, "faceRotating", SMESH.FACE)
status = STR.RemoveHypothesis(NETGEN_3D_finer)
status = STR.AddHypothesis(NETGEN_3D_standard)
[
    inlet_2,
    outlet_2,
    shaft_2,
    stirrer_2,
    static_1,
    rotating_1,
    walls_1,
    faceRotating_1,
] = STR.GetGroups()
try:
    STR.ExportUNV(
        r"/home/federico/OpenFOAM/federico-13/run/STR_tetra_rotating/STR.unv",
        0,
    )
    pass
except:
    print("ExportUNV() failed. Invalid file name?")
NETGEN_2D_Parameters_3 = smesh.CreateHypothesis(
    "NETGEN_Parameters_2D", "NETGENEngine"
)
NETGEN_2D_Parameters_3.SetWorstElemMeasure(0)
NETGEN_2D_Parameters_3.SetUseDelauney(0)
status = STR.AddHypothesis(NETGEN_1D_2D, faceRotating)
status = STR.AddHypothesis(NETGEN_2D_Parameters_3, faceRotating)
[
    inlet_2,
    outlet_2,
    shaft_2,
    stirrer_2,
    static_1,
    rotating_1,
    walls_1,
    faceRotating_1,
] = STR.GetGroups()
try:
    STR.ExportUNV(
        r"/home/federico/OpenFOAM/federico-13/run/STR_tetra_rotating/STR.unv",
        0,
    )
    pass
except:
    print("ExportUNV() failed. Invalid file name?")
NETGEN_2D_Parameters_3.SetSecondOrder(0)
NETGEN_2D_Parameters_3.SetOptimize(1)
NETGEN_2D_Parameters_3.SetChordalError(0)
NETGEN_2D_Parameters_3.SetChordalErrorEnabled(0)
NETGEN_2D_Parameters_3.SetUseSurfaceCurvature(1)
NETGEN_2D_Parameters_3.SetFuseEdges(1)
NETGEN_2D_Parameters_3.SetFineness(3)
[
    inlet_2,
    outlet_2,
    shaft_2,
    stirrer_2,
    static_1,
    rotating_1,
    walls_1,
    faceRotating_1,
] = STR.GetGroups()
try:
    STR.ExportUNV(
        r"/home/federico/OpenFOAM/federico-13/run/STR_tetra_rotating/STR.unv",
        0,
    )
    pass
except:
    print("ExportUNV() failed. Invalid file name?")
[
    inlet_2,
    outlet_2,
    shaft_2,
    stirrer_2,
    static_1,
    rotating_1,
    walls_1,
    faceRotating_1,
] = STR.GetGroups()
Viscous_Layers_1 = NETGEN_1D_2D_3D.ViscousLayers(
    1, 2, 1.2, [90, 119, 137], 0, smeshBuilder.SURF_OFFSET_SMOOTH
)
NETGEN_2D_Parameters_3.SetMaxSize(0.002)
NETGEN_2D_Parameters_3.SetMinSize(0.002)
[
    inlet_2,
    outlet_2,
    shaft_2,
    stirrer_2,
    static_1,
    rotating_1,
    walls_1,
    faceRotating_1,
] = STR.GetGroups()
NETGEN_3D_standard.SetMaxSize(0.02)
NETGEN_3D_standard.SetMinSize(0.001)
NETGEN_3D_standard.SetSecondOrder(0)
NETGEN_3D_standard.SetOptimize(1)
NETGEN_3D_standard.SetFineness(2)
NETGEN_3D_standard.SetChordalError(0)
NETGEN_3D_standard.SetChordalErrorEnabled(0)
NETGEN_3D_standard.SetUseSurfaceCurvature(1)
NETGEN_3D_standard.SetFuseEdges(1)
NETGEN_3D_standard.SetQuadAllowed(0)
NETGEN_3D_standard.SetCheckChartBoundary(93)
[
    inlet_2,
    outlet_2,
    shaft_2,
    stirrer_2,
    static_1,
    rotating_1,
    walls_1,
    faceRotating_1,
] = STR.GetGroups()
Viscous_Layers_1.SetTotalThickness(0.0005)
Viscous_Layers_1.SetNumberLayers(1)
Viscous_Layers_1.SetStretchFactor(1.2)
Viscous_Layers_1.SetMethod(smeshBuilder.SURF_OFFSET_SMOOTH)
Viscous_Layers_1.SetFaces([90, 119, 137], 0)
[
    inlet_2,
    outlet_2,
    shaft_2,
    stirrer_2,
    static_1,
    rotating_1,
    walls_1,
    faceRotating_1,
] = STR.GetGroups()
status = STR.RemoveHypothesis(Viscous_Layers_1)
[
    inlet_2,
    outlet_2,
    shaft_2,
    stirrer_2,
    static_1,
    rotating_1,
    walls_1,
    faceRotating_1,
] = STR.GetGroups()
NETGEN_2D_Parameters_3.SetQuadAllowed(0)
NETGEN_2D_Parameters_3.SetCheckChartBoundary(95)
isDone = STR.Compute()
STR.CheckCompute()
[
    inlet_2,
    outlet_2,
    shaft_2,
    stirrer_2,
    static_1,
    rotating_1,
    walls_1,
    faceRotating_1,
] = STR.GetGroups()
try:
    STR.ExportUNV(
        r"/home/federico/OpenFOAM/federico-13/run/STR_tetra_rotating/STR.unv",
        0,
    )
    pass
except:
    print("ExportUNV() failed. Invalid file name?")
Sub_mesh_1 = STR.GetSubMesh(faceRotating, "Sub-mesh_1")


## Set names of Mesh objects
smesh.SetName(walls_1, "walls")
smesh.SetName(stirrer_2, "stirrer")
smesh.SetName(NETGEN_2D_Parameters_3, "NETGEN 2D Parameters_3")
smesh.SetName(inlet_2, "inlet")
smesh.SetName(shaft_2, "shaft")
smesh.SetName(NETGEN_2D_Parameters_1, "NETGEN 2D Parameters_1")
smesh.SetName(NETGEN_2D_Parameters_2, "NETGEN 2D Parameters_2")
smesh.SetName(STR.GetMesh(), "STR")
smesh.SetName(NETGEN_3D_finer, "NETGEN 3D finer")
smesh.SetName(outlet_2, "outlet")
smesh.SetName(static_1, "static")
smesh.SetName(Viscous_Layers_1, "Viscous Layers_1")
smesh.SetName(faceRotating_1, "faceRotating")
smesh.SetName(rotating_1, "rotating")
smesh.SetName(NETGEN_1D_2D, "NETGEN 1D-2D")
smesh.SetName(NETGEN_3D_standard, "NETGEN 3D standard")
smesh.SetName(Sub_mesh_1, "Sub-mesh_1")
smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), "NETGEN 1D-2D-3D")


if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser()
