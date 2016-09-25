#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import collections
import os
import six
import traitlets

from enum import Enum

import nvis.common as com


class _JSObject(traitlets.HasTraits):
    """
    Base class for JS instances, which can be converted to
    JavaScript instance
    """

    def __eq__(self, other):
        # conmpare with script
        if isinstance(other, _JSObject):
            return self.script == other.script
        return False

    @property
    def _klass(self):
        return "Cesium.{0}".format(self.__class__.__name__)

    @property
    def _props(self):
        raise NotImplementedError('must be overriden in child classes')

    @property
    def _property_dict(self):
        props = collections.OrderedDict()
        for p in self._props:
            props[p] = getattr(self, p)
        return props

    @property
    def script(self):
        props = self._property_dict
        results = com.to_jsobject(props)
        return ''.join(results)


class _Enum(Enum):

    @property
    def script(self):
        return self.value


class RistrictedList(_JSObject):

    widget = traitlets.Instance(klass=_JSObject)

    def __init__(self, widget, allowed, propertyname):
        self.widget = widget

        self._items = []
        self._allowed = allowed
        self._propertyname = propertyname

    def add(self, item, **kwargs):
        if com.is_listlike(item):
            for i in item:
                self.add(i, **kwargs)
        elif isinstance(item, self._allowed):
            for key, value in six.iteritems(kwargs):
                setattr(item, key, value)
            self._items.append(item)
        else:
            msg = 'item must be {allowed} instance: {item}'

            if isinstance(self._allowed, tuple):
                allowed = ', '.join([a.__name__ for a in self._allowed])
            else:
                allowed = self._allowed

            raise ValueError(msg.format(allowed=allowed, item=item))

    def clear(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def __getitem__(self, item):
        return self._items[item]

    @property
    def script(self):
        """
        return list of scripts built from entities
        each script may be a list of comamnds also
        """
        results = []
        for item in self._items:
            script = """{varname}.{propertyname}.add({item});"""
            script = script.format(varname=self.widget._varname,
                                   propertyname=self._propertyname,
                                   item=item.script)
            results.append(script)
        return results
