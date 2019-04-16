#!/bin/bash
# python 3.6 required
# tested on openfoam 1806


#def vars
cpus=4
py1=direction_of_vortex.py
py2= rot_zirkulation.py

# calculate vorticity
#mpirun -np $cpus postProcess -func vorticity -parallel -latestTime |tee log.calculation_vorticity


# sample vortex plane
#mpirun -np $cpus postProcess -func sampleDict_plane_vorticity -parallel -latestTime |tee log.vortex_plane

#find max and define lines
python3 $py1 |tee log.linegeneration

#read out defined lines
mpirun -np $count_proc postProcess -parallel -func sampleDict_python_plotlines |tee log.sampling

#calculate circulation based on umlaufintegral
python3 $py2 |tee log.calculation_gamma

