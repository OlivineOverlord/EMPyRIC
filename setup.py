from setuptools import setup, find_packages

setup(
    name="empyric",  # Package name
    version="0.1.0",  # Initial version
    author="Joshua Shea",
    author_email="your-email@example.com",
    description="A geochemical data management package using HDF5.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/empyric",  # Update with your actual repo
    packages=find_packages(),  # Auto-detect `empyric/` package
    install_requires=[
        "numpy",
        "pandas",
        "h5py",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "empyric=empyric.cli:main",  # Enables CLI command
        ],
    },
    python_requires=">=3.7",
)