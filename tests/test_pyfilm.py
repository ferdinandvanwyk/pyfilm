import os

from pytest import raises
import numpy as np
from PIL import Image
import matplotlib
import warnings
matplotlib.use('Agg') # specifically for Travis CI to avoid backend errors

from pyfilm.pyfilm import *

class TestClass(object):
    """
    Class containing methods which test pyfilm.
    """
    def teardown_class(self):
        os.system('rm -rf films')
        os.system('rm -rf __pycache__')

    def test_set_default_options(self):
        options = {}
        options = set_default_options(options)
        assert options['aspect'] == 'auto'
        assert options['crop'] == True
        assert options['cbar_label'] == 'f(x,y)'
        assert options['encoder'] == None
        assert options['fps'] == 10
        assert options['file_name'] == 'f'
        assert options['grid'] == False
        assert options['img_fmt'] == 'png'
        assert options['ncontours'] == 11
        assert type(options['nprocs']) == int
        assert options['title'] == ''
        assert options['video_fmt'] == 'mp4'
        assert options['xlabel'] == 'x'
        assert options['xlim'] == None
        assert options['xticks'] == None
        assert options['ylabel'] == 'y'
        assert options['ylim'] == None
        assert options['yticks'] == None

    def test_set_user_options(self):
        options = {}
        options = set_default_options(options)
        user_options = {'xlabel':'test'}
        options = set_user_options(options, user_options)
        assert options['xlabel'] == 'test'

    def test_set_up_dirs(self):
        options = {}
        options = set_default_options(options)
        set_up_dirs(options)
        assert os.path.exists('films') == True
        assert os.path.exists('films/film_frames') == True

    def test_find_encoder(self):
        options = find_encoder({})
        assert (options['encoder'] == 'avconv' or options['encoder'] == 'ffmpeg')

    def test_set_ylim(self):
        y = np.array([range(5)]*5)
        options = {}
        set_ylim(y, options)
        assert(options['ylim'] == [0,4])
        y = np.array([range(5)]*5) - 3
        set_ylim(y, options)
        assert(options['ylim'] == [-3,3])
        y = np.array([range(5)]*5) - 4
        set_ylim(y, options)
        assert(options['ylim'] == [-4,0])

    def test_check_data_1d_with_wrong_size(self):
        x = np.arange(5)
        y = np.random.rand(5,4)
        with raises(ValueError):
            check_data_1d(x,y)

    def test_check_data_1d_with_wrong_shapes(self):
        x = np.random.rand(5,5)
        y = np.random.rand(5,5)
        with raises(IndexError):
            check_data_1d(x,y)

        x = np.arange(5)
        y = np.random.rand(5,5,4)
        with raises(IndexError):
            check_data_1d(x,y)

    def test_plot_1d(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        os.system('rm films/film_frames/*.png')
        options = {}
        options = set_default_options(options)
        set_up_dirs(options)
        make_plot_titles(2, options)
        args = (0, x, y[0,:], {}, options)
        plot_1d(args)
        assert ('f_00000.png' in os.listdir('films/film_frames/'))

    def test_1d_1_arg(self):
        y = np.random.rand(2,2)
        make_film_1d(y)
        assert ('f_00000.png' in os.listdir('films/film_frames/'))
        assert ('f.mp4' in os.listdir('films/'))

    def test_1d_2_arg(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        make_film_1d(x, y)
        assert ('f_00000.png' in os.listdir('films/film_frames/'))
        assert ('f.mp4' in os.listdir('films/'))

    def test_1d_argumets(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        with raises(ValueError):
            make_film_1d(x, x, y)

    def test_crop_images(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        make_film_1d(x, y)
        im = Image.open('films/film_frames/f_00000.png')
        w = im.size[0]
        h = im.size[1]
        assert (w%2 == 0 and h%2 == 0)

    def test_2d_1_arg(self):
        z = np.random.rand(2,2,2)
        make_film_2d(z)
        assert ('f_00000.png' in os.listdir('films/film_frames/'))
        assert ('f.mp4' in os.listdir('films/'))

    def test_2d_1_arg_negative(self):
        z = np.array([[[-10,  -6], [  1,  -5]],[[  0,  -8],[ -1,  -3]]])
        make_film_2d(z)
        assert ('f_00000.png' in os.listdir('films/film_frames/'))
        assert ('f.mp4' in os.listdir('films/'))

    def test_2d_3_arg(self):
        x = np.random.rand(2)
        y = np.random.rand(2)
        z = np.random.rand(2,2,2)
        make_film_2d(x, y, z)
        assert ('f_00000.png' in os.listdir('films/film_frames/'))
        assert ('f.mp4' in os.listdir('films/'))

    def test_plot_2d(self):
        x = np.arange(2)
        y = np.arange(2)
        z = np.random.rand(2,2,2)
        os.system('rm films/film_frames/*.png')
        options = {}
        options = set_default_options(options)
        set_up_dirs(options)
        make_plot_titles(2, options)
        args = (0, x, y, z[0,:,:], {}, options)
        plot_2d(args)
        assert ('f_00000.png' in os.listdir('films/film_frames/'))

    def test_check_data_2d_with_wrong_sizes(self):
        x = np.arange(5)
        y = np.arange(5)
        z = np.random.rand(5,4,5)
        with raises(ValueError):
            check_data_2d(x,y,z)
        z = np.random.rand(5,5,4)
        with raises(ValueError):
            check_data_2d(x,y,z)

    def test_check_data_2d_with_wrong_shapes(self):
        x = np.random.rand(5,5)
        y = np.random.rand(5)
        z = np.random.rand(5,5,5)
        with raises(IndexError): 
            check_data_2d(x,y,z)

        x = np.random.rand(5)
        y = np.random.rand(5,5)
        z = np.random.rand(5,5,5)
        with raises(IndexError): 
            check_data_2d(x,y,z)

        x = np.random.rand(5)
        y = np.random.rand(5)
        z = np.random.rand(5,5)
        with raises(IndexError): 
            check_data_2d(x,y,z)

    def test_2d_argumets(self):
        x = np.arange(2)
        y = np.arange(2)
        z = np.random.rand(2,2,2)
        with raises(ValueError):
            make_film_2d(x, z)
        with raises(ValueError):
            make_film_2d(x, y, y, z)

    def test_make_plot_titles(self, recwarn):
        options = {}
        options = set_default_options(options)
        options = make_plot_titles(10, options)
        assert len(options['title']) == 10

        options['title'] = ['test']*9
        with raises(ValueError):
            make_plot_titles(10, options)

    def test_img_fmt(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        make_film_1d(x, y, options={'img_fmt':'jpg'})
        assert ('f_00000.jpg' in os.listdir('films/film_frames/'))
        assert ('f.mp4' in os.listdir('films/'))

    def test_calculate_cbar_ticks(self):
        options = {}
        options = set_default_options(options)
        z = np.random.randint(low=0, high=2, size=[2,2,2])
        options = calculate_cbar_ticks(z, options)
        assert np.sum(options['cbar_ticks'] - np.linspace(0, 1, 5)) < 1e-5

        options = {}
        options = set_default_options(options)
        options['cbar_ticks'] = 7
        z = np.random.randint(low=0, high=2, size=[2,2,2])
        options = calculate_cbar_ticks(z, options)
        assert np.sum(options['cbar_ticks'] - np.linspace(0, 1, 7)) < 1e-5

    def test_calculate_contours(self):
        options = {}
        options = set_default_options(options)
        plot_options = {}
        z = np.reshape(np.arange(8), [2,2,2])
        options = calculate_contours(z, options, plot_options)
        assert np.sum(plot_options['levels'] - np.linspace(0, 7, 11)) < 1e-5

        options = {}
        options = set_default_options(options)
        options['ncontours'] = 21
        plot_options = {}
        z = np.reshape(np.arange(8), [2,2,2])
        options = calculate_contours(z, options, plot_options)
        assert np.sum(plot_options['levels'] - np.linspace(0, 7, 21)) < 1e-5


