#!/bin/bash
#ablauf des skripts: Distanzen, in denen die Zirkulations berechnet werden soll sind in in "line_gen_gamma.py" in der Variable 'x_list' definiert, y und z koennen analog angepasst werden. 

#zunaechst werden in line_gen_gamma.py die zu sampelnden Linien definiert, es wird mit 2000 Werten/ Linie gesampelt.

#mit postProcess -func wird das sampleDict_python_plotlines ausgeführt

#Die gesampelten Lines werden in "integration_gamma.py" eingelesen, mit Trapez integriert und mit matplot lib geplottet. Die Ausgabe erfolgt einmal über Terminal (->plt.show()) und als .pdf in  /postProcessing/sampleDict_python_plotlines/<latest Timestep>/plots/c_gamma*.pdf


echo "needs to be run from inside pP_script!
Readme:
	needs Python 3.6 (at least 3, i think)
	Error: no module matplotlib found? install matplotlib using 'python3 -m 	install matplotlib'
	Error: no moudle tkinter found? install tkinter using 'sudo apt-get install 	python3-tk'
	worked for me"
#first python tool
py1=linge_gen_wing_gamma.py
py2=wingintegration_gamma.py
#rm log*
rm -r /system/sampleDict_python_plotlines
#mkdir Auswertungsdaten
cd ..

cp pP_script/$py1 postProcessing/
cd postProcessing
python3 $py1

cd ..
rm -r postProcessing/sampleDict_python_plotlines
postProcess -func sampleDict_python_plotlines


cp pP_script/$py2 postProcessing/
cd postProcessing
python3 $py2

rm $py2
rm $py1

echo 'should be done, .pdf can be found in /postProcessing/sampleDict_python_plotlines/<latest Timestep>/plots/c_gamma*.pdf '











## Copy mesh:
# cp -r /home.temp/fds159/feder/OpenFOAM/feder-1706/chow/meshing/snappy5_f/8/polyMesh/ constant/

## Execute with of v1706
# mapFields -consistent -sourceTime 4000 ../../snappy4_LEnoCyl_0.75/SST_simple
# rm -r processor*
# rm log.simpleFoam

#decomposePar -constant

## Don't do potiFoam, because the initial fields were mapped!!
# mpirun -np 4 potentialFoam -parallel -writep | tee log.potFoam
#mpirun -np 4 simpleFoam -parallel | tee log.simpleFoam

## Postprocessing with of1706?

#selber rausgemacht
#mpirun -np 10 vorticity -parallel -latestTime
#mpirun -np 10 Lambda2 -parallel -latestTime
#mpirun -np 10 yPlusRAS -parallel -latestTime | tee log.yPlus -a

#reconstructPar -latestTime

# cp system/sampleDict_plane_U system/sampleDict
# sample -time 300
