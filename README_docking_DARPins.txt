#### DOCKING DARPINS ####

AUTHORS
Filip Radom, Emanuele Paci, Andreas Plueckthun

GENERAL DESCRIPTION
The protocol for computational modeling and docking of DARPins.

PREREQUISITES
1) Linux-based system.
2) Python2 with numpy package.
3) Message Passing Interface (e.g. OpenMPI; https://www.open-mpi.org/).
4) PyMOL (https://pymol.org/2/).
5) Rosetta 3 (https://www.rosettacommons.org).

GETTING STARTED
1) Copy /Rosetta_DARPin_docking_templates to your working directory.

PROCEDURE
Homology modelling of a DARPin:
1) Navigate to /DARPin_model/DARPin_fixbb or, if insertions/deletions need to be modelled, to /DARPin_model/DARPin_remodel
2) Choose best template (details in the manuscript), modify .resfile, or .remodel (blueprint file for remodelling) in a text editor to introduce mutations and update flags.
3a) Run fixbb:
	$ ~/<rosetta_directory>/main/source/bin/fixbb.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags
3b) Run remodel:
	$ ~/<rosetta_directory>/main/source/bin/remodel.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags
	$ cd /rosetta_output
	$ ~/<rosetta_directory>/main/source/bin/cluster.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags_cluster
	
	Example:
		protocols.cluster: Cluster:  0  N: 30GN: 31   c.0.*.pdb 
		protocols.cluster:     2xee_A.clean_0001_0001  -539.949
		protocols.cluster:     2xee_A.clean_0001_0006  -540.342
	Here, second model: c.0.1 scores best.

4) Copy the single .pdb model from /rosetta_output to /rosetta_output/relax, navigate there and run relax:
	$ mpiexec -np <no_cores> ~/<rosetta_directory>/main/source/bin/relax.mpi.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags
5) Navigate to /relax/rosetta_output and cluster the models:
	$ ~/<rosetta_directory>/main/source/bin/cluster.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags_cluster
6) Pick the lowest-scoring model from the largest cluster (as in 3b).

#Receptor modelling:
1) Download receptor coordinates from PDB and place in /Receptor_model/relax_with_constraints
2) Prepare the structure for Rosetta:
	a) grep "^ATOM" <receptor>.pdb > <receptor>.clean.pdb
	b) Load the cleaned receptor into Pymol and in Pymol execute:
		% alter (all),resi=str(int(resi)-<identifier_of_first_res> + 1) #renumber for Rosetta
		% alter (all), chain ='A' #rename chain to A
3) Update flags and run relax:
	$ ~/<rosetta_directory>/main/source/bin/relax.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags
4) Copy the relaxed receptor to /Receptor_model/search_flexible/Backrub_on_full
5) Update flags and run backrub:
	$ mpiexec -np <no_cores> ~/<rosetta_directory>/main/source/bin/backrub.mpi.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags
6) Rename the output models: update receptor name in rename.txt and run:
	$ python rename.py
7) Load the generated models (250) together with the relaxed receptor from 4) into Pymol session and execute provided script:
	% run pymol_rmsf.py
	Then, execute two functions described within the script:
	% fit_unbound arg1, arg2, arg3
	% dev_fragment arg1, arg2, arg3, arg4, arg5, arg6
	Calculation may take up to a few hours. The console outputs RMSF of protein segments.
8) List all residues from all segments with RMSF values >0.2 and update -pivot_residues in /Backrub_on_loop/flags.
9) Copy relaxed receptor from 4) to /Backrub_on_loop and run backrub on loops:
	$ mpiexec -np <no_cores> ~/<rosetta_directory>/main/source/bin/backrub.mpi.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags
10) Take all generated models with ‘_last’ suffix as input for ClusPro.

#Rigid-body docking in ClusPro
1) Go to https://cluspro.bu.edu/
2) Start new job for each of 20 receptor loop models:
	a) Upload a receptor and a DARPin model.
	b) In menu Attraction and Repulsion add repulsive constraints to the DARPin chain.
3) Download 10 best models from each run and place them in folders /ClusPro/en1-20
4) Run the script to rename and to move the files to /docking_prepack:
	$ python ClusPro_rename.py	
5) Navigate to /docking_prepack, list the files and run docking_prepack_protocol:
$ ls -d $PWD/en* > files.txt
$ ~/<rosetta_directory>/main/source/bin/docking_prepack_protocol.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags
6) Move prepacked models from /rosetta_output to /ClusPro/sequential_clustering, list them and cluster within 5 A radius:
$ ls -d $PWD/en* > files.txt
$ ~/<rosetta_directory>/main/source/bin/cluster.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags_cluster
7) Move models from c.0, c.1 and c.2 clusters to corresponding subfolders and rename them:
$ python rename.py
8) In each subfolder list the files and cluster within 2 A radius:
$ ls -d $PWD/m* > files.txt
$ ~/<rosetta_directory>/main/source/bin/cluster.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags_cluster
9) For each cluster rename center of the largest subcluster (rename the subcluster center c.0.0 of cluster c.1 to c.1.0.0, etc.). Use the three models for flexible docking.

#Flexible docking with Rosetta
1) Copy three best models: c.0.0.0, c.1.0.0., c.2.0.0 to Rosetta_flexible_docking
2) Modify constraint.cst if necessary (if DARPin models contain insertions/deletions)
3) Check centers of mass of binding partners (necessary for next step): copy c.0.0.0 to /rigid_dock_to_check_centers and run docking_protocol:
$ ~/<rosetta_directory>/main/source/bin/docking_protocol.linuxgccrelease -database ~/<path_to_rosetta>/main/database @flags_pert
3) Design fold tree and modify fold_tree_DARPin.txt. DARPin_loops_pdb_to_rosetta.xlsx can be used for calculation of DARPin numbering.
4) Define flexible fragments in .xml Rosetta script: modify MoveMap in MinMover in DARPin_flex.xml
5) List the models and run rosetta_scripts:
$ ls -d $PWD/c.* > files.txt
$ mpiexec -np <no_cores> ~/<rosetta_directory>/main/source/bin/rosetta_scripts.mpi.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags_pert_flex
6) Navigate to /rosetta_output. Run InterfaceAnalyzer for models derived from each input model separately:
	a) $ ls -d $PWD/c.<0/1/2>* > files_c.<0/1/2>.txt
	b) Update flags_int
	c) mpiexec -np <no_cores> ~/<rosetta_directory>/main/source/bin/InterfaceAnalyzer.mpi.linuxgccrelease -database ~/<rosetta_directory>/main/database @flags_int
7) Compute p2gs scores and pick the best cluster:
$ python p2gs_calculator.py
8) Sort the best cluster by dG_separated and identify the best model, e.g.,:
$ cat Interface_c.<0/1/2>.txt | sort -nk 6 | awk '{print $NF}' | head -1  #check if dG_separated values are in column 6 (may change in future releases of Rosetta)

DEMO
Example files are provided in /Demo, where DARPin K27 is docked to KRAS.




