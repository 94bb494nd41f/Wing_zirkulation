#!/bin/bash
# python 3.6 required
# tested on openfoam 1806


#def vars

py1=direction_of_vortex.py
py2=rot_zirkulation.py


cd .. #needs to be run from case
# calculate vorticity
postProcess -func vorticity -latestTime |tee log.calculation_vorticity


# sample vortex plane
postProcess -func sampleDict_plane_vorticity -latestTime |tee log.vortex_plane

#cd pP_script #  tools  need to be run from this folder

cp pP_script/$py1 postProcessing/
cd postProcessing
#find max and define lines
python3 $py1 |tee log.linegeneration

cd ..
#read out defined lines
postProcess -func sampleDict_python_plotlines |tee log.sampling


cp pP_script/$py2 postProcessing/
cd postProcessing
#calculate circulation based on umlaufintegral
python3 $py2 |tee log.calculation_gamma