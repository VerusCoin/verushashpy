VerusHash Module in C++
=======================

A native VerusHash module that supports VerusHash from V1 to V2.1

Installation (requires Python 3.5+)
-----------------------------------

NOTE: Installation currently requires cloning the pybind11 repo as well and running: "python setup.py install" in the 
pybind11 directory before installing this module in order to access the pybind11 header files.

**On Unix (Linux, OS X)**

 - clone this repository
 - `pip install ./verushashpy`

**On Windows (Requires Visual Studio 2015)**

     - clone this repository
     - `pip install .\verushashpy`

   Note that this requires the user building `verushash` to have registry editing
   rights on the machine, to be able to run the `vcvarsall.bat` script.


Windows runtime requirements
----------------------------

On Windows, the Visual C++ 2015 redistributable packages are a runtime
requirement for this project. It can be found [here](https://www.microsoft.com/en-us/download/details.aspx?id=48145).

If you use the Anaconda python distribution, you may require the Visual Studio
runtime as a platform-dependent runtime requirement for you package:

```yaml
requirements:
  build:
    - python
    - setuptools
    - pybind11

  run:
   - python
   - vs2015_runtime  # [win]
```


Building the documentation
--------------------------

Documentation for the example project is generated using Sphinx. Sphinx has the
ability to automatically inspect the signatures and documentation strings in
the extension module to generate beautiful documentation in a variety formats.
The following command generates HTML-based reference documentation; for other
formats please refer to the Sphinx manual:

 - `cd verushashpy/docs`
 - `make html`

License
-------

pybind11 is provided under a BSD-style license that can be found in the LICENSE
file. By using, distributing, or contributing to this project, you agree to the
terms and conditions of this license.

Usage
-----

```python
import verushash as vh

vh.initialize()
byte_ary = vh.verushash()
byte_ary = vh.verushash_v2()
byte_ary = vh.verushash_v2b()
byte_ary = vh.verushash_v2b1()
byte_ary = vh.verushash_v2b2()

```
