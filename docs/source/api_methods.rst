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

The options dictionary controls plot options not included in plot_options (e.g. 
axis labels, plot limits, etc.) as well as how the program behaves. A complete 
list of parameters implemented so far in `pyfilm` is produced below.

Example:

.. code-block:: python
   
   import numpy as np
   import pyfilm as pf

   pf.make_film_1d(np.random.rand(10,10), options={'fps':20, 'xlim':[0,1.5]})

================ =============== ==============================================
Option           Default [#f1]_  Value Type                          
================ =============== ==============================================
aspect           'auto'          ['auto' | 'equal' | float] Set plot aspect 
                                 ratio.
bbox_inches      None            [None | 'tight' | float] Bbox in inches. Only 
                                 the given portion of the figure is saved. If 
                                 ‘tight’, try to figure out the tight bbox of 
                                 the figure.
cbar_label       'z'             [str] Label of the contour plot color bar
cbar_ticks       None            [None | int | np.ndarray] Set the color bar ticks
cbar_tick_format '%.2f'          [str] Print format of the color bar ticks
contours         7               [int] Number of contour levels
crop             True            [True | False] Crops images before encoding
dpi              None            [None | int] DPI of saved images. Defaults to
                                 savefig.dpi value in matplotlibrc file.
encoder          None            [None | 'ffmpeg' | 'avconv'] Specifies the 
                                 encoder to be used by pyfilm
file_name        'f'             [str] Name of film frames and film
film_dir         'films'         [str] Location where films are written
film_frames      'films/         [str] Location where film frames are written
                 film_frames'
fps              10              [int] Frames per second of the film                      
grid             True            [True | False] Controls plotting of gridlines
title            ''              [str | list] Specify title as string or array
                                 of strings of length of time domain which is
                                 iterated through
nprocs           None            [None | int] Set max number of cpu cores to 
                                 use. Defaults to max number of cores on 
                                 machine
xlabel           'x'             [str] Specify xlabel. May include LaTeX 
xlim             None            [None | array] Set x-axis limits
ylabel           'y'             [str] Specify ylabel. May include LaTeX 
ylim             None            [None | array] Set y-axis limits
================ =============== ============================================== 

.. rubric:: Footnotes

.. [#f1] None implies that the value is automatically determined.

Multiprocessing and performance considerations
----------------------------------------------

As of version 0.2.0, *pyfilm* includes support for multiprocessing mainly for 
parallel saving of film frames. The number of cores dedicated to both saving of
film frames and encoding using ffmpeg/avconv is controlled via the `nprocs`
option.

Even with multiprocessing support, adding too many plot options may affect the 
run time and limit the usefulness of the API. If things are running too slowly 
consider moving some options to your Matplotlib rcParams to set plot defaults.

