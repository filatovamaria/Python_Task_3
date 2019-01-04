# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 19:34:40 2018

@author: Masha
"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension('hello',
                         ['hello.pyx'],
                        )]
setup(
name = 'hello',
cmdclass = {'build_ext': build_ext},
ext_modules = ext_modules
)