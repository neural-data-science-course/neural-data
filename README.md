# Module 1: Neural Data

This is module one of the [Neural data science course](https://neural-data-science-course.github.io/). In this module we'll introduce some of the most important type of data that neuroscientists encounter in their research activity.
You will learn how to handle, pre-process and visualize these data, to make them ready for downstream analysis.

## Lessons
01. LFP - 60 minutes
02. Spikes - 60 minutes (coming soon)
03. Calcium Imaging - 60 minutes

## Prerequisites
To use material of this module profitably, you will need:  
* Familiarity with python and jupyter
* Basic knowledge of calculus and linear algebra

## Setup

### Install Pyhton and anaconda on your machine 
If you don't have them already installed, install Pyhton and Anaconda on your machine.
Follow these instructions on [how to install anaconda](https://docs.anaconda.com/anaconda/install/)

### Intall Mamba on your machine
CaImAn, a library used in this module, is more easily installed with (mamba)[https://mamba.readthedocs.io/en/latest/index.html
].
To install mamba on your machine, download the [mambaforge installer](https://github.com/conda-forge/miniforge#mambaforge) and run it.  
You can also download mamba from conda following this instructions: https://mamba.readthedocs.io/en/latest/installation.html (not recommended, often fails to build the environment)

### Create a virtual environment**
Create a conda virtual environment with the name you prefer, then activate it to work within it.
For this module, you will need the CaImAn tool, that is easier to install when creating the environment. 
Open a terminal, or open 'Anaconda Prompt' from Anaconda Navigator, in there run:

```
mamba create -n neural_data -c conda-forge caiman
mamba activate env_name
```


### Download the module folder
Clic on Code/Download Zip at the top of the page.  
Move the zipped folder in the directory of your choice and decompress it.  
Open the terminal and navigate to the module directory.

### Install the module requirements

Run in the terminal

```
pip install -r requirements.txt
```

### Open Jupyter lab
You can now open the lesson's notebooks in jupyter lab
```
jupyter lab
```

### All set!
You're all set to go through the lessons.


## Contributors  
* Davide Spalla  
* Melisa Maidana Capitan  

## License


Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

## Citation
If you want to cite this module, please use:
