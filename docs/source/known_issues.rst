Known Issues
============

Below are a few know issues (which may be outside the author's control) as well
as possible fixes.

Plots aren't displaying
-----------------------

This could be an issue with the Matplotlib backend. Refer to this_ page to read
about the possible Matplotlib backends.

Linux: usually `TkAgg`
OS X: Use either `macosx` or `Agg`. 

OS X is prone to complaining about Python Framework versions, backends not 
being thread-safe etc. See other issues on how to deal with those. Mostly this
just involves using the `Agg` backend.

.. _this: http://matplotlib.org/faq/usage_faq.html#what-is-a-backend

Plots are not rendering correctly (missing/misplaced text, strange layouts,...)
-------------------------------------------------------------------------------

This behaviour has been observed before and was found to be related to the
parallelization. Try setting `nprocs` to 1 and see if that solves the problem.
If not, open an issue on GitHub, but it may again be related to backend 
weirdness.

Python is not installed as a framework
--------------------------------------

When running inside a Python vitualenv (as you probably should be ;)) on OS X
and you get the following error:

   from matplotlib.backends import _macosx
   RuntimeError: Python is not installed as a framework. The Mac OS X backend
   will not be able to function correctly if Python is not installed as a
   framework. See the Python documentation for more information on installing
   Python as a framework on Mac OS X. Please either reinstall Python as a
   framework, or try one of the other backends. If you are Working with
   Matplotlib in a virtual enviroment see 'Working with Matplotlib in Virtual
   environments' in the Matplotlib FAQ

Try the `Agg` backend which usually works.

The process has forked and you cannot use this CoreFoundation functionality...
------------------------------------------------------------------------------

If you get the following error on OS X:

   The process has forked and you cannot use this CoreFoundation functionality
   safely. You MUST exec().Break on __THE_PROCESS_HAS_FORKED_AND_YOU_CANNOT_USE_THIS_COREFOUNDATION_FUNCTIONALITY___YOU_MUST_EXEC__()
   to debug.

This means that the backend you are using is not thread-safe. See this_ page,
but again the solution is to use the `Agg` backend.

.. _this: http://stackoverflow.com/questions/8106002/using-the-python-multiprocessing-module-for-io-with-pygame-on-mac-os-10-7
