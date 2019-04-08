# python 3.6 required
# tested on openfoam 1806


# calculate vorticity
mpirun -np 4 postProcess -func vorticity -parallel -latestTime
# sample vortex plane
mpirun -np 4 postProcess -func sampleDict_plane_vorticity -parallel -latestTime

# run script to determine vector of vortex

#run script tp calculate circulation of vortex

