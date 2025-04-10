import os
import argparse
from Bio.PDB import PDBParser
import numpy as np
from pocket2mol_class import Pocket2MolCaller

def get_pocket_dimensions(pocket_path):
    parser = PDBParser(PERMISSIVE=1) 
    structure = parser.get_structure("pocket", pocket_path)

    coord = []
    for model in structure:
        for chain in model: 
            for residue in chain:
                    for atom in residue:
                        coord.append(atom.coord)
    
    coord_numpy = np.array(coord)

    x_max,y_max,z_max = np.max(coord_numpy, axis=0) 
    x_min,y_min,z_min = np.min(coord_numpy, axis=0)

    bbox_size = max(x_max - x_min, y_max - y_min, z_max - z_min)

    center = [(x_max + x_min) / 2, (y_max + y_min) / 2, (z_max + z_min) / 2]

    return center, bbox_size

def main():
    parser = argparse.ArgumentParser(description="Run Pocket2Mol ligand generation.")
    parser.add_argument('--pdb_path', required=True, help="Path to input PDB file.")
    parser.add_argument('--pocket_path', required=True, help="Path to pocket PDB file.")
    parser.add_argument('--mount_dir', required=True, help="Mount directory for container.")
    parser.add_argument('--container_path', required=True, help="Path to Singularity container (.sif).")
    parser.add_argument('--device', default="cpu", help="Device to use (e.g., cpu or cuda).")
    parser.add_argument('--outdir', default=None, help="Directory to save output (optional).")

    args = parser.parse_args()

    center, bbox_size = get_pocket_dimensions(args.pocket_path)

    caller = Pocket2MolCaller(args.mount_dir, args.container_path)
    caller.generate_ligand(
        pdb_path=args.pdb_path,
        center=center,
        bbox_size=bbox_size,
        device=args.device,
        outdir=args.outdir
    )
if __name__ == '__main__':
    main()
