#!/bin/bash
# python 3.6 required
# tested on openfoam 1806


#def vars

py1=direction_of_vortex.py
py2=rot_zirkulation.py


cd .. #needs to be run from case
rm -r postProcessing
mkdir postProcessing # muss erstellt werden, Manueller Modus geht nur wenn weder Druck, noch Vorticity vorhanden ist.
# calculate vorticity
#postProcess -func vorticity -latestTime |tee log.calculation_vorticity
#postProcess -func Lambda2 -latestTime |tee log.calculation_lambda2
# !!!!! Druck oder Vorticity!!!!!!

# sample vortex plane
postProcess -func sampleDict_plane_vorticity -latestTime |tee log.vortex_plane
################### oder #####################
#postProcess -func sampleDict_plane_pressure -latestTime |tee log.pressure_plane
################### oder #####################
#postProcess -func sampleDict_plane_lambda -latestTime |tee log.lambda_plane

#cd pP_script #  tools  need to be run from this folder

cp pP_script/$py1 postProcessing/
cd postProcessing
#find max and define lines
python3 $py1 |tee log.linegeneration
rm $py1

cd ..
#read out defined lines
postProcess -func sampleDict_python_plotlines -latestTime |tee log.sampling


cp pP_script/$py2 postProcessing/
cd postProcessing
#calculate circulation based on umlaufintegral
python3 $py2 |tee log.calculation_gamma

#clean up
rm $py2
rm p_min
rm v_max
rm -r sampleDict_plane_pressure
rm -r sampleDict_plane_vorticity
rm -r sampleDict_plane_lambda
rm ../system/sampleDicht_python_plotlines
