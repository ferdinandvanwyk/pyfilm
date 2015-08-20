"""
.. module:: pyfilm
   :platform: Unix, OSX
   :synopsis: Main pyfilm functions.

.. moduleauthor:: Ferdinand van Wyk <ferdinandvwyk@gmail.com>
"""

import os
import warnings
import multiprocessing as mp

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cpuinfo import cpuinfo


def make_film_1d(*args, **kwargs):
    """
    The main function which generates 1D films.

    Parameters
    ----------

    x : array_like, optional
        Array specifying the x axis.
    y : array_like
        Two dimensional array assumed to be of the form y(t, x). This specifies
        the values to be plotted as a function of time.
    plot_options : dict, optional
        Dictionary of plot customizations which are evaluated for each plot,
        e.g. when plot is called it will be called as
        plt.plot(x, y, **plot_options)
    options : dict, optional
        Dictionary of options which control various program functions.
    """

    options = {}
    options = set_default_options(options)
    try:
        options = set_user_options(options, kwargs['options'])
    except KeyError:
        pass

    try:
        plot_options = kwargs['plot_options']
    except KeyError:
        plot_options = {}

    set_up_dirs(options)

    if options['encoder'] == None:
        options = find_encoder(options)

    if len(args) == 1:
        y = np.array(args[0])
        nt = y.shape[0]
        nx = y.shape[1]
        x = np.arange(nx)
    elif len(args) == 2:
        x = np.array(args[0])
        y = np.array(args[1])
        nt = y.shape[0]
        check_data_1d(x, y)
    else:
        raise ValueError('This function only takes in max. 2 arguments.')

    if options['ylim'] == None:
        options = set_ylim(y, options)

    options = make_plot_titles(nt, options)

    pool = mp.Pool(processes=options['nprocs'])
    params = zip(range(nt), [x]*nt, y, [plot_options]*nt, [options]*nt)
    pool.map(plot_1d, params)
    pool.close()
    pool.join()

    if options['crop']:
        crop_images(nt, options)

    encode_images(options)


def make_film_2d(*args, **kwargs):
    """
    The main function which generates 2D films.

    Parameters
    ----------
    x : array_like, optional
        Array specifying the x axis.
    y : array_like, optional
        Array specifying the y axis.
    z : array_like
        Three dimensional array assumed to be of the form z(t, x, y). This
        specifies the values to be plotted as a function of time.
    plot_options : dict, optional
        Dictionary of plot customizations which are evaluated for each plot,
        e.g. when plot is called it will be called as
        plt.plot(x, y, **plot_options)
    options : dict, optional
        Dictionary of options which control various program functions.
    """
    options = {}
    options = set_default_options(options)
    try:
        options = set_user_options(options, kwargs['options'])
    except KeyError:
        pass

    try:
        plot_options = kwargs['plot_options']
    except KeyError:
        plot_options = {}

    set_up_dirs(options)

    if options['encoder'] == None:
        options = find_encoder(options)

    if len(args) == 1:
        z = np.array(args[0])

        nt = z.shape[0]
        nx = z.shape[1]
        ny = z.shape[2]

        x = np.arange(nx)
        y = np.arange(ny)
    elif len(args) == 2:
        raise ValueError('Specify either (x,y,z) or just z.')
    elif len(args) == 3:
        x = np.array(args[0])
        y = np.array(args[1])
        z = np.array(args[2])

        check_data_2d(x, y, z)

        nt = z.shape[0]
    else:
        raise ValueError('This function only takes in max. 3 arguments.')

    if type(options['cbar_ticks']) == np.ndarray:
        pass
    elif type(options['cbar_ticks']) == int or options['cbar_ticks'] == None:
        options = calculate_cbar_ticks(z, options)

    options = make_plot_titles(nt, options)

    pool = mp.Pool(processes=options['nprocs'])
    params = zip(range(nt), [x]*nt, [y]*nt, z, [plot_options]*nt, [options]*nt)
    pool.map(plot_2d, params)
    pool.close()
    pool.join()

    if options['crop']:
        crop_images(nt, options)

    encode_images(options)


def set_default_options(options):
    """
    Sets the default options.

    Parameters
    ----------
    options : dict
        Dictionary of options which control various program functions.
    """

    options['title'] = ''
    options['xlabel'] = 'x'
    options['ylabel'] = 'y'
    options['xlim'] = None
    options['ylim'] = None
    options['grid'] = False
    options['aspect'] = 'auto'

    options['encoder'] = None
    options['fps'] = 10
    options['file_name'] = 'f'
    options['film_dir'] = 'films'
    options['frame_dir'] = 'films/film_frames'
    options['crop'] = True
    options['cbar_label'] = 'f(x,y)'
    options['cbar_ticks'] = None
    options['contours'] = 7
    options['cbar_tick_format'] = '%.2f'
    options['nprocs'] = cpuinfo.get_cpu_info()['count']
    options['dpi'] = None
    options['bbox_inches'] = None

    return(options)


def set_user_options(options, user_options):
    """
    Replace default options with user specified ones.

    An exhastive list of the available options is given in a table in the
    documentation.

    Parameters
    ----------

    options : dict
        Dictionary of options which control various program functions.
    user_options : dict
        Dictionary of options passed in by the user as a keyword argument.
    """
    for key, value in user_options.items():
        options[key] = value

    return(options)


def set_up_dirs(options):
    """
    Checks for film directories and creates them if they don't exist.

    Parameters
    ----------
    options : dict
        Dictionary of options which control various program functions.
    """
    if options['film_dir'] not in os.listdir('.'):
        os.system("mkdir -p " + options['film_dir'])
    if options['frame_dir'] not in os.listdir('.'):
        os.system("mkdir -p " + options['frame_dir'])
    os.system("rm -f " + options['frame_dir'] + "/" + options['file_name'] +
              "_*.png")


def check_data_1d(x, y):
    """
    Performs consistency checks on the data passed into make_film_1d.

    These checks are only done when both x and y arguments are passed into the
    function.

    Parameters
    ----------

    x : array_like,
        Array specifying the x axis.
    y : array_like
        Two dimensional array assumed to be of the form y(t, x). This specifies
        the values to be plotted as a function of time.
    """
    x_s = x.shape
    y_s = y.shape
    if x_s[0] != y_s[1]:
        raise ValueError('x and y must have the same length: '
                         '{0}, {1}'.format(x_s[0], y_s[1]))


def check_data_2d(x, y, z):
    """
    Performs consistency checks on the data passed into make_film_2d.

    These checks are only done when both x, y, and z arguments are passed into
    the function.

    Parameters
    ----------
    x : array_like
        Array specifying the x axis.
    y : array_like
        Array specifying the y axis.
    z : array_like
        Three dimensional array assumed to be of the form z(t, x, y). This
        specifies the values to be plotted as a function of time.
    """
    x_s = x.shape
    y_s = y.shape
    z_s = z.shape
    if x_s[0] != z_s[1]:
        raise ValueError('x and z must have the same length: '
                         '{0}, {1}'.format(x_s[0], z_s[1]))
    elif y_s[0] != z_s[2]:
        raise ValueError('y and z must have the same length: '
                         '{0}, {1}'.format(y_s[0], z_s[2]))


def find_encoder(options):
    """
    Determines which encoder the user has on their system.

    Parameters
    ----------
    options : dict
        Dictionary of options which control various program functions.
    """

    f = os.system('which ffmpeg')
    a = os.system('which avconv')

    if a > 0 and f > 0:
        raise EnvironmentError('This system does not have FFMPEG or AVCONV '
                               'installed.')
    elif a == 0 and f == 0:
        warnings.warn('This system has both FFMPEG and AVCONV installed. '
                      'Defaulting to AVCONV.')
        options['encoder'] = 'avconv'
    elif a == 0 and f > 0:
        options['encoder'] = 'avconv'
    elif f == 0 and a > 0:
        options['encoder'] = 'ffmpeg'

    return(options)


def set_ylim(y, options):
    """
    Sets the y limit for 1D films if not specified in options.

    Parameters
    ----------
    y : array_like
        Two dimensional array assumed to be of the form y(t, x). This specifies
        the values to be plotted as a function of time.
    options : dict
        Dictionary of options which control various program functions.
    """

    y_min = np.min(y)
    y_max = np.max(y)
    if y_min*y_max < 0:
        if np.abs(y_min) > np.abs(y_max):
            options['ylim'] = [y_min, -y_min]
        else:
            options['ylim'] = [-y_max, y_max]
    else:
        options['ylim'] = [y_min, y_max]

    return(options)


def calculate_cbar_ticks(z, options):
    """
    Calculate the color bar ticks based on the array extremes.

    There are three options for options['cbar_ticks']:

    * None: Automatically determine the extrama and set 5 ticks.
    * int: Automatically determine the extrama and set specified number of
      ticks.
    * array: Set cbar_ticks to user specified values.

    Parameters
    ----------

    z : array_like
        The 3D array being plotted: z(x, y).
    options : dict
        Dictionary of options which control various program functions.
    """

    z_min = np.min(z)
    z_max = np.max(z)
    if z_min*z_max < 0:
        if options['cbar_ticks'] == None:
            if np.abs(z_max) > np.abs(z_min):
                options['cbar_ticks'] = np.around(
                                           np.linspace(-z_max, z_max, 5), 7)
            else:
                options['cbar_ticks'] = np.around(
                                           np.linspace(z_min, -z_min, 5), 7)
        else:
            if np.abs(z_max) > np.abs(z_min):
                options['cbar_ticks'] = np.around(np.linspace(-z_max, z_max,
                                                  options['cbar_ticks']), 7)
            else:
                options['cbar_ticks'] = np.around(np.linspace(z_min, -z_min,
                                                  options['cbar_ticks']), 7)
    elif z_min*z_max >= 0:
        if options['cbar_ticks'] == None:
            options['cbar_ticks'] = np.around(np.linspace(z_min, z_max, 5), 7)
        else:
            options['cbar_ticks'] = np.around(np.linspace(z_min, z_max,
                                              options['cbar_ticks']), 7)

    return(options)


def plot_1d(args):
    """
    Plot the 1D graph for a given time step.

    Parameters
    ----------

    it : int
        Time index being plotted.
    x : array_like
        Array specifying the x axis.
    y : array_like
        Two dimensional array assumed to be of the form y(t, x). This specifies
        the values to be plotted as a function of time.
    plot_options : dict
        Dictionary of plot customizations which are evaluated for each plot,
        e.g. when plot is called it will be called as
        plt.plot(x, y, **plot_options)
    options : dict
        Dictionary of options which control various program functions.
    """

    it, x, y, plot_options, options = args

    fig = plt.figure()
    plt.plot(x, y, **plot_options)

    plt.title(options['title'][it])
    plt.xlabel(options['xlabel'])
    plt.ylabel(options['ylabel'])

    plt.xlim(options['xlim'])
    plt.ylim(options['ylim'])

    plt.grid(options['grid'])

    plt.axes().set_aspect(options['aspect'])

    plt.savefig(options['frame_dir'] + '/{0}_{1:05d}.png'.format(
                options['file_name'], it),
                dpi=options['dpi'],
                bbox_inches=options['bbox_inches'])
    plt.close(fig)


def plot_2d(args):
    """
    Plot the 2D contour plot for a given time step.

    Parameters
    ----------

    it : int
        Time index being plotted.
    x : array_like
        Array specifying the x axis.
    y : array_like
        Array specifying the y axis.
    z : array_like
        Three dimensional array assumed to be of the form z(t, x, y). This
        specifies the values to be plotted as a function of time.
    plot_options : dict
        Dictionary of plot customizations which are evaluated for each plot,
        e.g. when plot is called it will be called as
        plt.plot(x, y, **plot_options)
    options : dict
        Dictionary of options which control various program functions.
    """

    it, x, y, z, plot_options, options = args

    plt.clf()
    ax = plt.subplot(111)
    im = ax.contourf(x, y, np.transpose(z), options['contours'],
                     **plot_options)

    plt.title(options['title'][it])
    plt.xlabel(options['xlabel'])
    plt.ylabel(options['ylabel'])

    plt.xlim(options['xlim'])
    plt.ylim(options['ylim'])

    plt.grid(options['grid'])

    ax.set_aspect(options['aspect'])

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    plt.colorbar(im, cax=cax, label=options['cbar_label'],
                 ticks=options['cbar_ticks'],
                 format=options['cbar_tick_format'])

    plt.savefig(options['frame_dir'] + '/{0}_{1:05d}.png'.format(
                options['file_name'], it),
                dpi=options['dpi'],
                bbox_inches=options['bbox_inches'])


def crop_images(nt, options):
    """
    Ensures that PNG files have height and width that are even.

    This owes to a quirk of avconv and libx264 that requires this. At the
    moment there is no easy way to specifically set the pixel count using
    Matplotlib and this is not desirable anyway since plots can be almost
    any size and aspect ratio depending on the data. The other solution
    found online is to use the `-vf` flag for avconv to control the output
    size but this does not seem to work. The most reliable solution
    therefore is to use Pillow to load and crop images.

    Parameters
    ----------

    nt : int
        Length of the time dimension.
    options : dict
        Dictionary of options which control various program functions.
    """

    w = np.empty([nt], dtype=int)
    h = np.empty([nt], dtype=int)
    for it in range(nt):
        im = Image.open(options['frame_dir'] + '/{0}_{1:05d}.png'.format(
                                                    options['file_name'], it))
        w[it] = im.size[0]
        h[it] = im.size[1]

    w_min = np.min(w)
    h_min = np.min(h)
    new_w = int(w_min/2)*2
    new_h = int(h_min/2)*2
    for it in range(nt):
        im = Image.open(options['frame_dir'] + '/{0}_{1:05d}.png'.format(
                                                    options['file_name'], it))
        im_crop = im.crop((0, 0, new_w, new_h))
        im_crop.save(options['frame_dir'] + '/{0}_{1:05d}.png'.format(
                                                     options['file_name'], it))


def make_plot_titles(nt, options):
    """
    Creates the array of plot titles passed to the plotting function.

    This function allows dynamic plot titles such as the frame number or time.
    When the user has just passed in a fixed string, this is repeated to be the
    same length as the time dimension.

    Parameters
    ----------

    nt : int
        Length of the time dimension.
    options : dict
        Dictionary of options which control various program functions.
    """

    if type(options['title']) == str:
        options['title'] = [options['title']]*nt
    elif type(options['title']) == list:
        if len(options['title']) > nt:
            warnings.warn('Dimension of time and length of plot titles '
                          'different: {0}, {1}'.format(nt,
                                                       len(options['title'])))
        elif len(options['title']) < nt:
            raise ValueError('Dimension of time greater than length of plot '
                             'titles: {0}, {1}'.format(nt,
                                                       len(options['title'])))

    return(options)


def encode_images(options):
    """
    Encode PNG images into a film.

    Parameters
    ----------

    options : dict
        Dictionary of options which control various program functions.
    """

    if options['encoder'] == 'avconv':
        os.system("avconv -threads " + str(options['nprocs']) + " -y -f "
                  "image2 -r " + str(options['fps']) + " -i " +
                  "'" + options['frame_dir'] + '/' +
                  str(options['file_name']) + "_%05d.png' -q 1 " +
                  options['film_dir'] + "/" + str(options['file_name']) +
                  ".mp4")
    elif options['encoder'] == 'ffmpeg':
        os.system("ffmpeg -threads " + str(options['nprocs']) + " -y "
                  "-r " + str(options['fps']) + " -i " + "'" +
                  options['frame_dir'] + '/' + str(options['file_name']) +
                  "_%05d.png' -pix_fmt yuv420p -c:v libx264 -q 1 " +
                  options['film_dir'] + "/" + str(options['file_name']) +
                  ".mp4")
