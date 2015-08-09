API Methods
===========

Below are the two main API functions provided by `pyfilm`.

.. automodule:: pyfilm.pyfilm
   :members: make_film_1d, make_film_2d

Plot options
------------

The available plot options are specified using the plot_options dictionary, 
passed as a keyword argument into the plotting functions. This means that the 
options are specified exactly as for `Matplotlib`_.

Example:

.. code-block:: python
   
   import numpy as np
   import pyfilm as pf

   pf.make_film_1d(np.random.rand(10,10), plot_options={'lw':3, 'ls':'--'})

Please consult the `Matplotlib`_ documentation for a comprehensive list of plot 
options.

.. _Matplotlib: http://matplotlib.org/api/pyplot_api.html

Options
-------

The options dictionary controls plot options not included in plot_dict (e.g. 
axis labels, plot limits, etc.) as well as how the program behaves. An 
exhaustive list is produced below.

======================= =========== ===========================================
Option                  Default     Value Type                          
======================= =========== ===========================================
xlabel                  'x'         String specifying xlabel. May include LaTeX. 
ylabel                  'y'         String specifying ylabel. May include LaTeX. 
xlim                    None        Array of x-axis limits
ylim                    None        Array of y-axis limits
grid                    True        Boolean controlling plot gridlines
encoder                 None        Specifies the encoder to be used by pyfilm
fps                     10          Frames per second of the film                      
fname                   'y'         Name of film frames and film
crop                    True        Set whether images are cropped or not
threads                 auto        Set max number of threads to use
======================= =========== =========================================== 

Performance considerations
--------------------------

Adding too many plot options may affect the run time and limit the usefulness 
of the API. If things are running too slowly consider moving some options to
your Matplotlib rcParams to set plot defaults.

