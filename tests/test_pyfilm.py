import os

import pytest
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg') # specifically for Travis CI to avoid backend errors

from pyfilm.pyfilm import *

class TestClass(object):
    """
    Class containing methods which test pyfilm.
    """
    def teardown_class(self):
        os.system('rm -rf films')

    def test_set_default_options(self):
        options = {}
        options = set_default_options(options)
        assert options['xlabel'] == 'x'
        assert options['ylabel'] == 'y'
        assert options['xlim'] == None
        assert options['ylim'] == None
        assert options['grid'] == False
        assert options['aspect'] == 'auto'

        assert options['fps'] == 10
        assert options['encoder'] == None
        assert options['file_name'] == 'f'
        assert options['crop'] == True
        assert options['cbar_label'] == 'f(x,y)'
        assert type(options['threads']) == int

    def test_set_user_options(self):
        options = {}
        options = set_default_options(options)
        user_options = {'xlabel':'test'}
        options = set_user_options(options, user_options)
        assert options['xlabel'] == 'test'

    def test_set_up_dirs(self):
        set_up_dirs()
        assert os.path.exists('films') == True
        assert os.path.exists('films/film_frames') == True

    def test_find_encoder(self):
        options = find_encoder({})
        assert (options['encoder'] == 'avconv' or options['encoder'] == 'ffmpeg')

    def test_check_data_1d(self):
        x = np.arange(5)
        y = np.random.rand(5,4)
        pytest.raises(ValueError, "check_data_1d(x,y)")
        
    def test_plot_1d(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        os.system('rm films/film_frames/*.png')
        options = {}
        options = set_default_options(options)
        plot_1d(0, x, y, plot_options={}, options=options)

    def test_1d_1_arg(self):
        y = np.random.rand(2,2)
        make_film_1d(y)
        assert ('f_1d_00000.png' in os.listdir('films/film_frames/'))
        assert ('f_1d.mp4' in os.listdir('films/'))

    def test_1d_2_arg(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        make_film_1d(x, y)
        assert ('f_1d_00000.png' in os.listdir('films/film_frames/'))
        assert ('f_1d.mp4' in os.listdir('films/'))
        
    def test_1d_argumets(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        pytest.raises(ValueError, "make_film_1d(x, x, y)")
        
    def test_crop_images(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        make_film_1d(x, y)
        im = Image.open('films/film_frames/f_1d_00000.png') 
        w = im.size[0]
        h = im.size[1]
        assert (w%2 == 0 and h%2 == 0)
                 
    def test_2d_1_arg(self):
        z = np.random.rand(2,2,2)
        make_film_2d(z)
        assert ('f_2d_00000.png' in os.listdir('films/film_frames/'))
        assert ('f_2d.mp4' in os.listdir('films/'))

    def test_2d_1_arg_negative(self):
        z = np.array([[[-10,  -6], [  1,  -5]],[[  0,  -8],[ -1,  -3]]]) 
        make_film_2d(z)
        assert ('f_2d_00000.png' in os.listdir('films/film_frames/'))
        assert ('f_2d.mp4' in os.listdir('films/'))

    def test_2d_3_arg(self):
        x = np.random.rand(2)
        y = np.random.rand(2)
        z = np.random.rand(2,2,2)
        make_film_2d(x, y, z)
        assert ('f_2d_00000.png' in os.listdir('films/film_frames/'))
        assert ('f_2d.mp4' in os.listdir('films/'))

    def test_plot_2d(self):
        x = np.arange(2)
        y = np.arange(2)
        z = np.random.rand(2,2,2)
        os.system('rm films/film_frames/*.png')
        options = {}
        options = set_default_options(options)
        plot_2d(0, x, y, z, plot_options={}, options=options)

    def test_check_data_2d(self):
        x = np.arange(5)
        y = np.arange(5)
        z = np.random.rand(5,4,5)
        pytest.raises(ValueError, "check_data_2d(x,y,z)")
        z = np.random.rand(5,5,4)
        pytest.raises(ValueError, "check_data_2d(x,y,z)")

    def test_2d_argumets(self):
        x = np.arange(2)
        y = np.arange(2)
        z = np.random.rand(2,2,2)
        pytest.raises(ValueError, "make_film_2d(x, z)")
        pytest.raises(ValueError, "make_film_2d(x, y, y, z)")
        
