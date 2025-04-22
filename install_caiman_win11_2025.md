##  How to install caiman on Window 11 (2025 version)

This is my experience installing Caiman on a Windows 11 installation. I start with a fully updated installation, fairly plain vanilla (I don't use Windows much so I don't have much installed). 
It's quite a lengthy process but it did work for me.

Please follow all of these steps carefully and in the order in which they are listed in here

- Install Visual Studio Community Edition (2022 version is the one freely available here ). You find it [here](https://visualstudio.microsoft.com/downloads/). Install at least the C/C++ compiler (or "workload" as they call it). I think the rest is not necessary, I have myself also installed the .NET stuff but I don't think is needed. It takes some time, but should run unassisted. 

- Now install Miniconda as explained [here](https://www.anaconda.com/docs/getting-started/miniconda/install). If you haven't done this very recently (for example, at the beginning of this course) I would advice you to make a fresh install. I have used the PowerShell method. Search for PowerShell in the Windows and run it from there. If you don't have PowerShell already, you can install it from the Microsoft website. 

- Install mamba as explained in this [tutorial](https://christianjmills.com/posts/mamba-getting-started-tutorial-windows/index.html). Once again, this happens in the PowerShell. 

- In the Windows search bar, type "Miniforge prompt", and open it. This will open a "special" powershell window. You will need to access Caiman always from that window. 

- In the miniforge prompt, go to a suitable directory and git clone the caiman repository
```
git clone https://github.com/flatironinstitute/CaImAn.git
```

- cd into the newly created CaImAn directory

- now *CAREFULLY* follow the instructions on the Caiman GitHub site, using the method under "Step 1: Install Caiman (alternative for Windows users):, with one important difference: instead of doing 
```
mamba create -n caiman python=3.11 pip vs2019_win-64
```
you will do 
```
mamba create -n caiman python=3.11 pip vs2022_win-64
```

The reason for this is that we installed Visual Studio 2022 instead of Visual Studio 2019 (older versions of VS are only accessible for paying customers). 
- As mentioned in the instructions, do 
```
conda activate caiman
```

- Add other packages that you will need to the environment, for example `conda install jupyterlab` or `conda install notebook`. For the workshop, you will also need `conda install seaborn`.

- Install Caiman with:
```
pip install .
```
The last step assumes that you are in the CaImAn folder. This will take a while, if all goes well it should give no error. If you get trouble, chances are it will be at this step. Get out of the CaImAn folder as soon as this is done (commands may give error if run from there). 



- You can install and run the demos following Step 2 and 3 in the Caiman instructions if you wish.

- Remember, whenever you want to use caiman, you will have to open the miniforge prompt window and `conda activate caiman` from there and there only. 


