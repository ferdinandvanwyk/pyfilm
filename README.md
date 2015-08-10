pyfilm
======

[![Documentation Status](https://readthedocs.org/projects/pyfilm/badge/?version=latest)](https://readthedocs.org/projects/pyfilm/?badge=latest)
[![Build Status](https://travis-ci.org/ferdinandvwyk/pyfilm.svg?branch=master)](https://travis-ci.org/ferdinandvwyk/pyfilm)
[![Coverage Status](https://coveralls.io/repos/ferdinandvwyk/pyfilm/badge.svg?branch=master&service=github)](https://coveralls.io/github/ferdinandvwyk/pyfilm?branch=master)

Creates films of 1D and 2D python arrays in time.

Getting Started
===============

System dependencies
-------------------

`pyfilm` generates a .png file for each timestep and stitches them together using
ffmpeg/avconv. The following non-system specific packages are therefore 
required:

* [libpng](www.libpng.org/pub/png/libpng.html)
* [libav](https://libav.org/) or [ffmpeg](https://www.ffmpeg.org/)

For example on Ubuntu 14.04 these are installed via:

    sudo apt-get install libpng12-dev libav-tools

For OSX using the Brew package manager, these can be installed via:

    brew install libpng ffmpeg

`pyfilm` will automatically check which of these is installed on your system.

Refer to [this](http://matplotlib.org/faq/usage_faq.html#what-is-a-backend) 
page to deal with Matplotlib backends in case plots don't display. TkAgg is a
good backend for most machines. Be sure to have the system packages installed 
before installing matplotlib.

Python dependencies
-------------------

The dependencies are listed in the requirements.txt file and are installed by
running:

    $ pip install -r requirements.txt

Since this project is structured as a PIP package, it also needs to be installed
using the following command (in the package root directory):

    $ pip install -e .

Importing
---------

Simply import into your project via:

    import pyfilm as pf

Examples
--------

1D Example:

    import numpy as np

    x = np.random.rand(10)
    y = np.random.rand(10, 10)
    pf.make_film_1d(x, y)

2D Example:

    import numpy as np

    x = np.random.rand(10)
    y = np.random.rand(10)
    z = np.random.rand(10, 10, 10)
    pf.make_film_2d(x, y, z)

1D Example wiht styling and options:

    import numpy as np

    x = np.random.rand(10)
    y = np.random.rand(10, 10)
    pf.make_film_1d(x, y, plot_options={'lw':3, 'ls':'--'}, 
                    options={'ylabel':'Amplitude', 'fname':'amp'})














