# NAG Library for Python Training material

This repository contains tutorials and exercises that are used to support NAG's training courses for the [NAG Library for Python](https://www.nag.com/nag-library-python).

## NAG library for Python installation

The NAG library for Python comes in two versions. One is linked to the Intel MKL for improved linear algebra performance on x86 architectures and the other is linked to NAG's self contained linear algebra libraries.

When using Intel or AMD CPUs we recommend the use of the Intel MKL version of the NAG Library for Python.

Install using the following command

```
python -m pip install --extra-index-url https://www.nag.com/downloads/py/naginterfaces_mkl naginterfaces
```

**Obtaining a license**

Before you can use the NAG Library for Python, you'll need a license.  Free trial licenses are available!

Run the following command to begin the licensing process and email [support@nag.co.uk](mailto:support@nag.co.uk) if you have any problems.

```
# This will launch a license request GUI on windows
# On Mac and Linux, it gives the information you need to send to support@nag.co.uk to request a trial license
python -m naginterfaces.kusari
```

* More detailed installation instructions are [available in the official documentation](https://www.nag.com/numeric/py/nagdoc_latest/readme.html#installation).
* More detailed license management instructions are available at [https://www.nag.com/numeric/py/nagdoc_latest/naginterfaces.kusari.html#kusari](https://www.nag.com/numeric/py/nagdoc_latest/naginterfaces.kusari.html#kusari)

## Exercises

We have collected together a set of exerices in the folder [hands-on-exercises](https://github.com/numericalalgorithmsgroup/NAGPythonLibraryTraining/blob/master/hands-on-exercises/). Solutions are in [hands-on-solutions](https://github.com/numericalalgorithmsgroup/NAGPythonLibraryTraining/tree/master/hands-on-solutions)

## Tutorials

Self-paced tutorials for various aspects of the library are in the [tutorials](https://github.com/numericalalgorithmsgroup/NAGPythonLibraryTraining/tree/master/tutorials) folder.

* [The 3 levels of interface](https://github.com/numericalalgorithmsgroup/NAGPythonLibraryTraining/blob/master/tutorials/python_3_interface_levels.ipynb) - A tutorial that explains the 3 different interface levels in the NAG Library for Python: **library**, **base** and **_primitive**

## Further examples

The [NAGPythonExamples](https://github.com/numericalalgorithmsgroup/NAGPythonExamples) repo contains a set of more detailed NAG Library for Python examples covering various areas of mathematics.

The NAG Library for Python also ships with a set of usage examples.  To see them all, run the following command once you have installed the product.

```
python -m naginterfaces.library.examples --locate
```
