To do list
==========

Regular and irregular grids
---------------------------

At the moment `pyfilm` only uses contourf_ to generate the contour plots. The
limitation of this function is that it requires a regular grid of points in
order to generate the contours. There is a separate function in matplotlib
which can take an irregular grid, called tricontourf_ which can operate on
irregular grids. There is possibly scope for allowing an option in `pyfilm` to
be able to take in both regular and irregular grids. The subtelty is that
tricontourf only takes in three 1D arrays so the data format currently
demanded would have to flattened first.

.. _contourf: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.contourf
.. _tricontourf: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.tricontourf
