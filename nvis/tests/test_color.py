#!/usr/bin/env python
# coding: utf-8

import unittest

import nvis


class TestColor(unittest.TestCase):

    def test_basic(self):
        """ http://visjs.org/examples/network/basicUsage.html """

        c = nvis.Color(color='lime')
        self.assertEqual(c.script, "'lime'")

        c = nvis.Color(color=(255, 168, 7))
        self.assertEqual(c.script, "'rgb(255, 168, 7)'")

        c = nvis.Color(color=(97, 195, 238, 0.5))
        self.assertEqual(c.script, "'rgba(97, 195, 238, 0.5)'")

        c = nvis.Color(color={'background': 'pink', 'border': 'purple'})
        self.assertEqual(c.script, "{background:'pink', border:'purple'}")

        c = nvis.Color({'background': '#F03967', 'border': '#713E7F',
                        'highlight': {'background': 'red',
                                      'border': 'black'}})
        self.assertEqual(c.script, "{background:'#F03967', border:'#713E7F', highlight:{background:'red', border:'black'}}")

        c = nvis.Color({'background': 'cyan', 'border': 'blue',
                        'highlight': {'background': 'red', 'border': 'blue'},
                        'hover': {'background': 'white', 'border': 'red'}})
        self.assertEqual(c.script, "{background:'cyan', border:'blue', highlight:{background:'red', border:'blue'}, hover:{background:'white', border:'red'}}")
