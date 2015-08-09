import os
import sys

import pytest
import numpy as np
from PIL import Image

from pyfilm.pyfilm import *

class TestClass(object):
    """
    Class containing methods which test pyfilm.
    """
    def teardown_class(self):
        os.system('rm -rf films')

    def test_set_default_options(self):
        options = set_default_options()
        assert options['xlabel'] == 'x'
        assert options['ylabel'] == 'y'
        assert options['xlim'] == None
        assert options['ylim'] == None
        assert options['grid'] == False
        assert options['fps'] == 10

    def test_set_user_options(self):
        options = set_default_options()
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


    def test_1d_1_arg(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        make_film_1d(y)
        assert ('y_00000.png' in os.listdir('films/film_frames/'))
        assert ('y.mp4' in os.listdir('films/'))

    def test_1d_1_arg(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        make_film_1d(x, y)
        assert ('y_00000.png' in os.listdir('films/film_frames/'))
        assert ('y.mp4' in os.listdir('films/'))

    def test_crop_images(self):
        x = np.arange(2)
        y = np.random.rand(2,2)
        make_film_1d(x, y)
        im = Image.open('films/film_frames/y_00000.png') 
        w = im.size[0]
        h = im.size[1]
        assert (w%2 == 0 and h%2 == 0)
                 





