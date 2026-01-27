echo PRESTEP 1
# Generate blockmeshDict
python ../../applications/write_block_cyl_mesh.py -i system/mesh.json -t system/topology.json -o system

# Generate species thermo properties
python ../../applications/write_species_thermo_prop.py -cf .

