pyfilm
======

.. image:: https://travis-ci.org/ferdinandvwyk/pyfilm.svg?branch=master
   :target: https://travis-ci.org/ferdinandvwyk/pyfilm
.. image:: https://readthedocs.org/projects/pyfilm/badge/?version=latest
   :target: https://readthedocs.org/projects/pyfilm
   :alt: Documentation Status
.. image:: https://coveralls.io/repos/ferdinandvwyk/pyfilm/badge.svg?branch=master&service=github 
   :target: https://coveralls.io/github/ferdinandvwyk/pyfilm?branch=master

Easily create films of 1D and 2D python arrays.

Getting Started
===============

Python version support
----------------------

Currently, *pyfilm* only support Python versions 3.x, however it is only tested
with 3.4.

System dependencies
-------------------

*pyfilm* generates a .png file for each timestep and stitches them together using
ffmpeg/avconv. The following non-system specific packages are therefore 
required:

* libpng_
* libav_ or ffmpeg_

For example on Ubuntu 14.04 these are installed via:

.. code:: bash

    sudo apt-get install libpng12-dev libav-tools

For OSX using the Brew package manager, these can be installed via:

.. code:: bash

    brew install libpng ffmpeg

*pyfilm* will automatically check which of these is installed on your system 
and default to ``avconv`` if both are found.

Refer to this_  
page to deal with Matplotlib backends in case plots don't display. TkAgg is a
good backend for most machines. Be sure to have the system packages installed 
before installing matplotlib.

.. _libpng: http://www.libpng.org/pub/png/libpng.html
.. _libav: https://libav.org/ 
.. _ffmpeg: https://www.ffmpeg.org/
.. _this: http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

Python dependencies
-------------------

The dependencies are listed in the requirements.txt file and are installed by
running:

.. code:: bash

    $ pip install -r requirements.txt

Since this project is structured as a PIP package, it also needs to be installed
using the following command (in the package root directory):

.. code:: bash

    $ python setup.py install

Importing
---------

Simply import into your project via:

.. code:: bash

    import pyfilm as pf

Examples
--------

1D Example:

.. code:: bash

    import numpy as np

    x = np.random.rand(10)
    y = np.random.rand(10, 10)
    pf.make_film_1d(x, y)

2D Example:

.. code:: bash

    import numpy as np

    x = np.random.rand(10)
    y = np.random.rand(10)
    z = np.random.rand(10, 10, 10)
    pf.make_film_2d(x, y, z)

1D Example wiht styling and options:

.. code:: bash

    import numpy as np

    x = np.random.rand(10)
    y = np.random.rand(10, 10)
    pf.make_film_1d(x, y, plot_options={'lw':3, 'ls':'--'}, 
                    options={'ylabel':'Amplitude', 'fname':'amp'})

Running Tests
-------------

*pyfilm* uses the pytest framework for unit and functional tests. To 
run the tests, run the following in the package root directory:

.. code:: bash

    $ py.test

To see information on the test coverage for individual files:

.. code:: bash

    $ py.test --cov pyfilm tests

Documentation
-------------

The documentation is completely built on Sphinx with numpydoc_ docstring 
convention and is hosted on `Read the Docs`_. Using 
RTD/GitHub webhooks, the documentation is rebuilt upon every commit that makes
changes to the documentation files The current build status is shown by the 
``docs`` badge at the top of the main page. To make the docs, run:

.. _numpydoc: https://github.com/numpy/numpydoc
.. _`Read the Docs`: https://readthedocs.org/projects/pyfilm/

.. code:: bash

    $ cd docs
    $ make html

where ``html`` can be replaced with other acceptable formats, such as latex,
latexpdf, text, etc. In order to view the Latex document, it first has to be 
built:

.. code:: bash

   $ cd build/latex
   $ make
