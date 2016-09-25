#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import six


class Color(object):

    def __init__(self, color=None):
        color = self._validate_color(color)
        self.color = color

    def _validate_color(self, color):
        # ToDo: Py3
        if isinstance(color, six.string_types):
            return "'{0}'".format(color)
        elif isinstance(color, tuple):
            if len(color) == 3:
                return "'rgb({0}, {1}, {2})'".format(*color)
            elif len(color) == 4:
                return "'rgba({0}, {1}, {2}, {3})'".format(*color)
            else:
                msg = 'tuple must have 3 or 4 elements: {0}'
                raise ValueError(msg.format(color))

        elif isinstance(color, dict):
            allowed = ['background', 'border', 'highlight', 'hover']
            # validation
            for key in color:
                if key not in allowed:
                    raise KeyError(key)

            results = []
            for key in allowed:
                if key in color:
                    c = Color(color[key])
                    results.append("{0}:{1}".format(key, c.script))
            return "{" + ', '.join(results) + "}"

        else:
            raise ValueError(type(color))

    @property
    def script(self):
        return self.color
