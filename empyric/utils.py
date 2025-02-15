"""
utils.py - Utility functions for handling and inspecting HDF5 files in EMPyRIC.

This module provides helper functions for:
- Printing HDF5 file structure efficiently.
- Filtering datasets based on metadata.
- Searching datasets by name.
- Interactive tree-based structure browsing.
- Previewing dataset contents.
"""

import h5py
from rich.tree import Tree
from rich.console import Console


def print_h5_structure(file_path):
    """
    Prints the structure of an HDF5 file in a hierarchical format.

    :param file_path: Path to the HDF5 file.
    """
    def traverse_h5(obj, indent=""):
        """Recursively traverses an HDF5 group and prints its structure."""
        for key in obj:
            item = obj[key]
            if isinstance(item, h5py.Group):
                print(f"{indent}📂 {key}/")  # Group
                traverse_h5(item, indent + "    ")
            else:
                print(f"{indent}📄 {key} (Shape: {item.shape}, Type: {item.dtype})")  # Dataset")
    
    with h5py.File(file_path, "r") as f:
        print(f"📁 File: {file_path}")
        traverse_h5(f)


def filter_datasets_by_metadata(file_path, metadata_key, metadata_value):
    """
    Searches an HDF5 file for datasets that contain a specific metadata attribute.

    :param file_path: Path to the HDF5 file.
    :param metadata_key: Metadata key to search for.
    :param metadata_value: Expected value of the metadata key.
    :return: List of matching dataset paths.
    """
    matches = []

    def search_metadata(obj, path=""):
        for key, item in obj.items():
            full_path = f"{path}/{key}" if path else key
            if isinstance(item, h5py.Group):
                search_metadata(item, full_path)
            elif isinstance(item, h5py.Dataset):
                if metadata_key in item.attrs and item.attrs[metadata_key] == metadata_value:
                    matches.append(full_path)

    with h5py.File(file_path, "r") as f:
        search_metadata(f)

    return matches


def search_dataset_by_name(file_path, dataset_name):
    """
    Searches for a dataset by name in an HDF5 file.

    :param file_path: Path to the HDF5 file.
    :param dataset_name: Name of the dataset to search for.
    :return: List of matching dataset paths.
    """
    matches = []

    def search(obj, path=""):
        for key, item in obj.items():
            full_path = f"{path}/{key}" if path else key
            if isinstance(item, h5py.Group):
                search(item, full_path)
            elif key == dataset_name:
                matches.append(full_path)

    with h5py.File(file_path, "r") as f:
        search(f)

    return matches


def print_h5_tree(file_path):
    """
    Uses Rich to print an interactive tree of the HDF5 structure.

    :param file_path: Path to the HDF5 file.
    """
    console = Console()

    def build_tree(obj, tree):
        """Recursively builds the Rich tree structure for an HDF5 file."""
        for key, item in obj.items():
            if isinstance(item, h5py.Group):
                subgroup = tree.add(f"📂 {key}/")
                build_tree(item, subgroup)
            else:
                tree.add(f"📄 {key} (Shape: {item.shape}, Type: {item.dtype})")

    with h5py.File(file_path, "r") as f:
        root_tree = Tree(f"📁 [bold]{file_path}[/bold]")
        build_tree(f, root_tree)
        console.print(root_tree)


def preview_dataset(file_path, dataset_path, num_rows=5):
    """
    Prints a preview of the first few values of a dataset.

    :param file_path: Path to the HDF5 file.
    :param dataset_path: Path to the dataset within the HDF5 file.
    :param num_rows: Number of rows to display (default is 5).
    """
    with h5py.File(file_path, "r") as f:
        if dataset_path not in f:
            print(f"Dataset {dataset_path} not found.")
            return
        
        dataset = f[dataset_path]
        if dataset.ndim == 1:  # 1D dataset
            print(f"{dataset_path} (First {num_rows} values): {dataset[:num_rows]}")
        elif dataset.ndim == 2:  # 2D dataset
            print(f"{dataset_path} (First {num_rows} rows):\n", dataset[:num_rows, :])
        else:
            print(f"{dataset_path} (First {num_rows} slices):\n", dataset[:num_rows])


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python utils.py <HDF5_FILE_PATH> [optional: --tree | --preview <dataset> | --search <name> | --filter <key> <value>]")
    else:
        file_path = sys.argv[1]
        if "--tree" in sys.argv:
            print_h5_tree(file_path)
        elif "--preview" in sys.argv and len(sys.argv) > 3:
            preview_dataset(file_path, sys.argv[3])
        elif "--search" in sys.argv and len(sys.argv) > 3:
            results = search_dataset_by_name(file_path, sys.argv[3])
            print("Matching datasets:", results)
        elif "--filter" in sys.argv and len(sys.argv) > 4:
            results = filter_datasets_by_metadata(file_path, sys.argv[3], sys.argv[4])
            print("Matching datasets:", results)
        else:
            print_h5_structure(file_path)