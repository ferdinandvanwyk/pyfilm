#!/usr/bin/env python
import os
from setuptools import setup

setup(
    name = "pyfilm",
    version = "0.1.1",
    author = "Ferdinand van Wyk",
    author_email = 'ferdinandvwyk@gmail.com',
    description = "PyFilm: easily create films of 1D and 2D NumPy arrays.",
    long_description = "PyFilm is a package which enables the quick creation of animations of NumPy arrays. It does this by writing each time step as a separate image and using either ffmpeg or avconv to stitch the images together into an animation. The package is designed to be very easy to use, and allow animations to be created with a single line.",
    license = "GNU",
    keywords = ['film', 'animation', 'numpy', 'ffmpeg', 'avconv'],
    packages=['pyfilm'],
    url = 'https://github.com/ferdinandvwyk/pyfilm.git',
    setup_requires =['numpy'],
    install_requires =[
        'matplotlib>1.4',
        'py-cpuinfo>0.1',
        'Pillow>2.8',
    ],
    classifiers=[
    "Development Status :: 3 - Alpha"
    ],
)
