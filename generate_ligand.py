import os
import argparse
from Bio.PDB import PDBParser
import numpy as np
from pocket2mol_class import Pocket2MolCaller

"""
Parses a pocket PDB file and calculates:
- The geometric center (x, y, z) of the pocket atoms.
- The bounding box size (maximum length in any of the the x/y/z planes).
"""

def get_pocket_dimensions(pocket_path):
    """
    Args:
        pocket_path (str): Path to the PDB file of the binding pocket.

    Returns:
        tuple:
            center (list of float): The [x, y, z] center coordinates.
            bbox_size (float): The maximum length in any dimension.
    """
    parser = PDBParser(PERMISSIVE=1) 
    structure = parser.get_structure("pocket", pocket_path)

    coord = []

    # Extract all atom coordinates from the pocket structure
    for model in structure:
        for chain in model: 
            for residue in chain:
                for atom in residue:
                    coord.append(atom.coord)
    
    # Convert list of coordinates to NumPy array
    coord_numpy = np.array(coord)

    # Find max and min along each axis
    x_max, y_max, z_max = np.max(coord_numpy, axis=0) 
    x_min, y_min, z_min = np.min(coord_numpy, axis=0)

    # Compute the size of the bounding box (max extent)
    bbox_size = max(x_max - x_min, y_max - y_min, z_max - z_min)

    # Compute the geometric center of the pocket
    center = [
        (x_max + x_min) / 2,
        (y_max + y_min) / 2,
        (z_max + z_min) / 2
    ]

    return center, bbox_size

def main():
    """
    Command-line interface for running ligand generation using Pocket2Mol.
    
    Steps:
    - Parses command-line arguments.
    - Computes pocket center and bounding box size.
    - Calls the Pocket2Mol container via Pocket2MolCaller.
    """
    
    parser = argparse.ArgumentParser(description="Run Pocket2Mol ligand generation.")
    parser.add_argument('--pdb_path', required=True, help="Path to input protein PDB file.")
    parser.add_argument('--pocket_path', required=True, help="Path to pocket PDB file (used for center/bbox calculation).")
    parser.add_argument('--mount_dir', required=True, help="Directory to mount into the container.")
    parser.add_argument('--container_path', required=True, help="Path to the Pocket2Mol Singularity container (.sif).")
    parser.add_argument('--device', default="cpu", help="Device to use (e.g., cpu or cuda). Default: cpu.")
    parser.add_argument('--outdir', default=None, help="Directory to save output ligand files (optional).")

    args = parser.parse_args()

    # Calculate the center and bounding box from the pocket file
    center, bbox_size = get_pocket_dimensions(args.pocket_path)

    # Initialize the container runner
    caller = Pocket2MolCaller(
        mount_dir=args.mount_dir,
        container_path=args.container_path
    )

    # Run ligand generation inside the container
    caller.generate_ligand(
        pdb_path=args.pdb_path,
        center=center,
        bbox_size=bbox_size,
        device=args.device,
        outdir=args.outdir
    )

if __name__ == '__main__':
    main()
