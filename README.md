# Pocket2Mol Wrapper

This repository provides a reproducible, command-line interface for running the [Pocket2Mol](https://github.com/zhaohongqi/Pocket2Mol) ligand generation pipeline using Singularity containers.
It includes tools for automatically computing the 3D center and bounding box of a protein pocket, and initiates the containerized ligand generation process.

Requirements:  
python 3.7+  
Singularity (https://sylabs.io/singularity/)  
Pocket2Mol '.sif' container  

Python Packages:  
biopython  
numpy  

## How it works

1. generate_ligand.py uses Biopython to parse the pocket PDB file.
2. It calculates the center coordinates and bounding box size.
3. It runs the Pocket2Mol container using singularity run, passing the center and box size.
4. Ligands are generated and saved to the specified output directory.

## Usage
```
python generate_ligand.py \ 
--pdb_path /path/to/protein.pdb \ 
--pocket_path /path/to/pocket.pdb \
--mount_dir /absolute/path/to/shared_dir \
--container_path /absolute/path/to/pocket2mol.sif \
--device cpu \
--outdir /path/to/output
```
**Arguments:**  
pdb_path:	Path to the full protein structure in PDB format  
pocket_path:	Path to the pocket (binding site) PDB file  
mount_dir:	Host directory to mount into container as /work  
container_path:	Absolute path to the Pocket2Mol .sif container image  
device:	(Optional) cpu or cuda (default: cpu)  
outdir:	(Optional) Directory to save output ligand files  

  
