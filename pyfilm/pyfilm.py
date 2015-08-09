import os
import sys
import shutil

import numpy as np
from cpuinfo import cpuinfo
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
    
    options = set_default_options()
    try:
        options = set_user_options(options, kwargs['options'])
    except KeyError:
        pass
    try:
        plot_options = kwargs['plot_options']
    except KeyError:
        plot_options = {}

    set_up_dirs()

    if options['encoder'] == None:
        options = find_encoder(options)

    if len(args) == 1:
        y = np.array(args[0])

        nt = y.shape[0]
        nx = y.shape[1]

        for it in range(nt):
            print('\rSaving frame ', it, ' of ', nt, end='')
            plt.clf()
            plt.plot(range(nx), y[it,:], **plot_options)

            plt.xlabel(options['xlabel'])
            plt.ylabel(options['ylabel'])
        
            plt.xlim(options['xlim'])
            plt.ylim(options['ylim'])

            plt.grid(options['grid'])

            plt.savefig('films/film_frames/{0}_{1:05d}.png'.format(
                                                        options['fname'], it))

    elif len(args) == 2:
        x = np.array(args[0])
        y = np.array(args[1])

        nt = y.shape[0]
        nx = y.shape[1]

        check_data_1d(x, y)

        for it in range(nt):
            print('\rSaving frame ', it, ' of ', nt, end='')
            plt.clf()
            plt.plot(x, y[it,:], **plot_options)

            plt.xlabel(options['xlabel'])
            plt.ylabel(options['ylabel'])
        
            plt.xlim(options['xlim'])
            plt.ylim(options['ylim'])

            plt.grid(options['grid'])

            plt.savefig('films/film_frames/{0}_{1:05d}.png'.format(
                                                        options['fname'], it))

    else:
        raise ValueError('This function only takes in max. 2 arguments.')

    if options['crop']:
        crop_images(nt, options)

    if options['encoder'] == 'avconv':
        os.system("avconv -threads " + str(options['threads']) + " -y -f "
                  "image2 -r " + str(options['fps']) + " -i " + 
                  "'films/film_frames/" + str(options['fname']) + 
                  "_%05d.png' -q 1 films/" + str(options['fname']) + ".mp4")
    elif options['encoder'] == 'ffmpeg':
        os.system("ffmpeg -threads " + str(options['threads']) + " -y "
                  "-r " + str(options['fps']) + "-pix_fmt yuv420p -c:v libx264"
                  " -i" + "'films/film_frames/" + str(options['fname']) + 
                  "_%05d.png' -q 1 films/" + str(options['fname']) + ".mp4")

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
    pass
    
def set_default_options():
    """
    Sets the default options.
    """
    options = {}

    options['xlabel'] = 'x'
    options['ylabel'] = 'y'
    options['xlim'] = None
    options['ylim'] = None
    options['grid'] = False

    options['encoder'] = None
    options['fps'] = 10
    options['fname'] = 'y'
    options['crop'] = True
    options['threads'] = cpuinfo.get_cpu_info()['count']

    return(options)

def set_user_options(options, user_options):
    """
    Replace default options with user specified ones.

    An exhastive list of the available options is given in a table in the 
    documentation.
    """
    for key, value in user_options.items():
        options[key] = value

    return(options)

def set_up_dirs():
    """
    Checks for film directories and creates them if they don't exist.
    """
    if 'films' not in os.listdir():
        os.system("mkdir films")
    if 'film_frames' not in os.listdir('films'):
        os.system("mkdir films/film_frames")
    os.system("rm -f films/film_frames/y_*.png")

def check_data_1d(x, y):
    """
    Performs consistency checks on the data passed into make_film_1d.

    These checks are only done when both x and y arguments are passed into the
    function.
    """
    x_s = x.shape 
    y_s = y.shape 
    if x_s[0] != y_s[1]:
        raise ValueError('x and y must have the same length: '
                         '{0}, {1}'.format(x_s[0], y_s[1]))

def find_encoder(options):
    """
    Determines which encoder the user has on their system.
    """

    f = shutil.which('ffmpeg')
    a = shutil.which('avconv')
    
    if a == None and f == None:
        raise EnvironmentError('This system does not have FFMPEG or AVCONV '
                               'installed.')
    elif a and f:
        raise EnvironmentError('This system has both FFMPEG and AVCONV '
                               'installed. Please choose one by setting '
                               '"encoder" in the options dict.')
    elif a and not f:
        options['encoder'] = 'avconv'
    elif f and not a:
        options['encoder'] = 'ffmpeg'

    return(options)

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
    """
    w = np.empty([nt], dtype=int)
    h = np.empty([nt], dtype=int)
    for it in range(nt):
        im = Image.open('films/film_frames/{0}_{1:05d}.png'.format(
                                                        options['fname'], it))
        w[it] = im.size[0]
        h[it] = im.size[1]

    w_min = np.min(w)
    h_min = np.min(h)
    new_w = int(w_min/2)*2
    new_h = int(h_min/2)*2
    for it in range(nt):
        im = Image.open('films/film_frames/{0}_{1:05d}.png'.format(
                                                        options['fname'], it))
        im_crop = im.crop((0, 0, new_w, new_h))
        im_crop.save('films/film_frames/{0}_{1:05d}.png'.format(
                                                        options['fname'], it))











