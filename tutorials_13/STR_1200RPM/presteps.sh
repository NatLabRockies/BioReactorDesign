#module purge
#module load conda
rm ./blockMeshDict_reactor
rm -r dynamicCode
rm -r 0
cp -r 0.org 0
# conda activate bird
python3 system/write_bmesh_file.py
blockMesh -dict ./blockMeshDict_reactor
stitchMesh -overwrite "((inside_to_hub inside_to_hub_copy) (hub_to_rotor hub_to_rotor_copy))"
transformPoints "rotate=((0 0 1)(0 1 0))"
# topoSet
setFields
