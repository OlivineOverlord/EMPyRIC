from setuptools import setup, find_packages

setup(
    name="empyric",
    version="0.1.0",
    author="Joshua Shea",
    author_email="joshuajshea@gmail.com",
    description="A geochemical data management package using HDF5.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OlivineOverlord/empyric",
    packages=find_packages(),
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
            "empyric=empyric.cli:main",
        ],
    },
    python_requires=">=3.7",
)