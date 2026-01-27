#!/bin/bash

# Clean case
./Allclean

set -e  # Exit on any error
# Define what to do on error
trap 'echo "ERROR: Something failed! Running cleanup..."; ./Allclean' ERR


echo PRESTEP 1
# Generate blockmeshDict
python ../../applications/write_block_cyl_mesh.py -i system/mesh.json -t system/topology.json -o system

# Generate species thermo properties
python ../../applications/write_species_thermo_prop.py -cf .


echo PRESTEP 2
# Mesh gen
blockMesh -dict system/blockMeshDict
transformPoints "rotate=((0 0 1) (0 1 0))"
transformPoints "scale=(0.001 0.001 0.001)"

# setup IC
cp -r 0.orig 0
setFields

# Scale
transformPoints "scale=(0.28329616612443 0.28329616612443 0.28329616612443)"

# Setup mass flow rate
# Get inlet area
postProcess -func 'patchIntegrate(patch="inlet_sparger_top", field="alpha.gas")'
postProcess -func 'patchIntegrate(patch="inlet_sparger_bottom", field="alpha.gas")'
postProcess -func writeCellVolumes
writeMeshObj

echo PRESTEP 3
python writeGlobalVars.py
cp constant/phaseProperties_pbe constant/phaseProperties


echo RUN
birdmultiphaseEulerFoam
