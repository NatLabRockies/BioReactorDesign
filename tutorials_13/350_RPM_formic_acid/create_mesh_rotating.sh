#!/bin/sh
cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

ideasUnvToFoam full_mesh.unv

createPatch -overwrite

createBaffles #-flipMap

renumberMesh -noFields -overwrite

createNonConformalCouples nonCouple1 nonCouple2

checkMesh

rm -r 0
cp -r 0.org 0

setFields

decomposePar -fileHandler collated -force

