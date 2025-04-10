import subprocess
import os 

"""
A class to use a Pocket2Mol container to generate ligands from a protein binding pocket.
"""
class Pocket2MolCaller:
    def __init__(self, mount_dir, container_path):
        """
        Initializes the Pocket2MolCaller with the mount directory and the path to the container.

        Args:
            mount_dir (str): Directory on the host system to mount inside the container.
            container_path (str): Absolute path to the Singularity container.
        """
        self.mount_dir = os.path.abspath(mount_dir)
        self.container_path = os.path.abspath(container_path)

    def generate_ligand(self, pdb_path, center, bbox_size=None, device=None, outdir=None):
        """
        Generates a ligand from a given protein pocket using the Pocket2Mol container.

        Args:
            pdb_path (str): Path to the input PDB file.
            center (list or tuple of float): Center coordinates of the binding pocket (x, y, z).
            bbox_size (float, optional): Size of the bounding box for ligand generation.
            device (str, optional): Device to use, e.g., 'cpu' or 'cuda'.
            outdir (str, optional): Directory to store the generated ligand output.

        """
        # Format center coordinates as a comma-separated string
        self.center = " " + ",".join(map(str, center))

        # Compute relative path of pdb file with respect to mount directory
        rel_pdb_path = os.path.relpath(os.path.abspath(pdb_path), self.mount_dir)

        # Define paths as seen from inside the container
        pdb_path_in_con = f"/work/{rel_pdb_path}"
        script_path_in_con = f"/work/sample_for_pdb.py"

        # Build the base singularity command
        command = [
            "singularity", "run",
            "--pwd", "/",         # Start execution from root directory
            "--cleanenv",         # Use a clean environment
            "--bind", f"{self.mount_dir}/:/work",  # Bind mount_dir to /work in the container
            self.container_path,  # Path to container
            "python",             # Run the Python script inside the container
            script_path_in_con,
            "--pdb_path", pdb_path_in_con,
            "--center", self.center
        ]

        # Optionally adds bbox_size, device, and output directory to the command
        if bbox_size is not None:
            command.extend(["--bbox_size", str(bbox_size)])
        if device is not None:
            command.extend(["--device", device])
        if outdir is not None:
            rel_outdir = os.path.relpath(os.path.abspath(outdir), self.mount_dir)
            command.extend(["--outdir", f"/work/{rel_outdir}"])

        # Run the command
        subprocess.run(command, check=True)

        