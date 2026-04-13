module load python
rm ./blockMeshDict_reactor
rm -r 0
python3 system/write_bmesh_file.py --n_fins 6 6    --imp_scale 1 1 --imp_centers 18 35 --aspect_ratio 1.671 --tank_volume 10000 --round_bottom 
blockMesh -dict ./blockMeshDict_reactor
stitchMesh  "( (inside_to_hub inside_to_hub_copy) (hub_to_rotor hub_to_rotor_copy) )"
transformPoints "scale=(0.001 0.001 0.001)"
cp -r 0.org 0
setFields
