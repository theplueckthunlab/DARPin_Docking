for (( c=1; c<=30; c++ ))
do  
   mpiexec -np 32 ~/rosetta_src_2017.45.59812_bundle/main/source/bin/rosetta_scripts.mpi.linuxgccrelease -database ~/rosetta_src_2017.45.59812_bundle/main/database @flags_pert_flex
done