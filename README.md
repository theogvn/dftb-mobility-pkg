# dftb-mobility-pkg

Package for performing electron mobility calculation with [DFTB+](https://github.com/dftbplus/dftbplus "DFTB+ GitHub page"), using Density Of States and Transmission
In the coming updates this package will support the calculation of mobility with the band structure.

_See the LICENSE for terms of usage and distribution._

## /!\\ Warning /!\\
**You may take the results with caution**

**Slater Koster files are not include.**

**The automation only automate the process for computing resistivity. You still need to manually run `mobility`.**
## Installation
This package uses [Numpy](https://numpy.org/install/ "Numpy's install page"), [SciPy](https://www.scipy.org/install.html "SciPy install page"), [Matplotlib](https://matplotlib.org/stable/users/installing.html "Matplotlib install page") and [DFTB+](https://github.com/dftbplus/dftbplus "DFTB+ GitHub page") make sure they are installed and that their directory is in your executable path.

To install **dftb-mobility-pkg** simply paste the bin files in your `dftb+/bin` directory or **make sure they are in your `PATH`**.
You may also have to make the files executable. To do so run :
```bash
$ chmod +x mobility resistance resistivity transport_file_editor
```

You can also call the python files using the **`python`** command but then make sure the python files are in the same directory as your _`dftb_in.hsd`_

## Usage

### Basic usage
This package can compute electron mobility using DFTB+ outputs, it uses DOS and Transmission data.
You can also use it with DOS and transmission from other software but make sure the DOS to specifie the right names for _`dos.dat`_ and _`transmission.dat`_.

If you use the executables, we advise starting by running:
```bash
$ mobility -h
```
```bash
$ resistance -h
```
```bash
$ resistivity -h
```
or, if you use the `.py` files:
```bash
$ python mobility.py -h
```
```bash
$ python resistance.py -h
```
```bash
$ python resistivity.py -h
```
However we recomand using `Shell Scripts` to automate the process, especially if you use the **`resistance`** and **`resistivity`**

### Automation with Shell Scripts

**dftb-mobility-pkg** comes with `Shell Scripts` that automate the process of running mobility calculation. In this section we will explain briefly how it works and how to use it.
You can fin the `Shell Scripts` in `dftb-mobility-pkg/shell-scripts/` but we will use the one from `dftb-mobility-pkg/exemple/` for this demonstration. Note that they are the same.

#### Required files
In `dftb-mobility-pkg/exemple/` you may notice 5 files in addition to the `.sh` files. These files are essential and must be name as such, except for _`copper_init.gen`_ where copper can be anything it only needs to keep this structure _`*_init.gen`_

*   The file _`copper_init.gen`_ contains the position and nature of atoms of your system. It will be use by _`setgeom.sh`_ to build a PL using **`repeatgen`** from **DFTB+ tools**, hence it is important to build _`copper_init.gen`_ correctly for **`repeatgen`**. This PL will later be saved under the name of _`pl.gen`_.

*   The file _`contact_hamiltonian_settings.hsd`_ is used by _`run_contact.sh`_ to set `Hamiltonian = DFTB {...}` in _`dftb_in.hsd`_ file that will be use to process the **contact**.
    >Note that this file can host `Option = {...}`, `Parallel = {...}` and other modules appart from `Transport` and `Geometry`.

*   The file _`transport_settings.hsd`_ is used by _`run_transport.sh`_ to set  `Hamiltonian = DFTB {...}` in _`dftb_in.hsd`_ file that will be use to process the **transport**.
    >Note that this file can host `Option = {...}`, `Parallel = {...}` and other modules appart from `Transport` and `Geometry`. This is the file where you might add the `Poisson` solver etc...

*   Finally the two files _`source_settings.hsd`_ and _`source_settings.hsd`_ are used by _`run_transport.sh`_ to set the two `Contact = {...}` inside the `Transport` module for transport calculations.

#### Shell Scripts
**Make sure your all the `.sh` files actually have the permission to be executed.**
You can see the permission of the files by running:
```bash
$ ls -l *.sh
```
You should get:
```bash
-rwxr-xr-x  1 UserName  data_analysis.sh
-rwxr-xr-x  1 UserName  run_contact.sh
-rwxr-xr-x  1 UserName  run_transport.sh
-rwxr-xr-x  1 UserName  setgeom.sh
-rwxr-xr-x  1 UserName  tasks.sh
```
Other wise run:
```bash
$ chmod +x *.sh
```

**To use the scripts you only need to run** _`tasks.sh`_
```bash
$ ./tasks.sh
```
This script will successively run _`setgeom.sh`_, _`run_contact.sh`_, _`run_transport.sh`_, _`data_analysis.sh`_.

1.  _`setgeom.sh`_ will create multiple wire like system using the `buildwire` tool that comes with **DFTB+**. In the `for` loop you have to set the number of PL in the device fo each system. The two contact will automatically have 2 PL. (The arguments of the `for` should be the same in each `.sh` file).
Each system will be placed in a new directory inside the main directory (`exemple/`). The directories will be named `lengthN` where N is the number of PL inside the device region.
Hence the path to  _`dftb_in.hsd`_ will be `exemple/lengthN/dftb_in.hsd`, you must set the path for Slater Koster files accordingly

2.  _`run_contact.sh`_ will run contact calculation for the source and the drain

3.  _`run_transport.sh`_ will run transport calculation according to the settings given by _`transport_settings.hsd`_, _`source_settings.hsd`_ and _`drain_settings.hsd`_

4.  _`data_analysis.sh`_ will run **`resistance`** in each `lenthN/` and write results in a new directory `dataAnalysisResults/`. Make sure to pass all required arguments for **`resistance`** in `data_analysis.sh`.
    >Note that this directory is required by **`resistance`** and should be in the main directory (`exemple/`).

    Then **`resistivity`** is run in `dataAnalysisResults/`, this is where you will find all final results.

## Credits
When publishing results obtained with `dftb-mobility-pkg`, please cite the following
**T. Giverne**, Bordeaux University Institute of Technology, _France_  
**N. A. Nebogatikova**, Novosibirsk State University (NSU), _Russia_
