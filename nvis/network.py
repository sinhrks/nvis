#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import collections
import os
import six
import traitlets

from nvis.base import _JSObject


class Network(_JSObject):
    """
    Base class for Network Widget / Viewer
    """

    def __init__(self, divid=None, width='100%', height='100%'):

        if divid is None:
            divid = 'container-{0}'.format(id(self))
        self.divid = divid

        self.width = width
        self.height = height

        self._nodes = []
        self._edges = []

    @property
    def _load_scripts(self):
        js = "https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"
        css = "http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css"

        def require_js(js_path):
            return """<script>
        require(["{0}"], function(lib) {{
            window.vis = jQuery.extend(true, {{}}, lib);
        }});
        </script>""".format(js_path)

        css = """<link rel="stylesheet" href="{0}" type="text/css">""".format(css)

        return [require_js(js), css]

    @property
    def container(self):
        container = """<div id="{0}" style="width:{1}; height:{2};"><div>"""
        return container.format(self.divid, self.height, self.width)

    def _repr_html_(self):
        return self.to_html()

    def to_html(self):
        headers = self._load_scripts
        container = self.container
        script = self._wrap_js(self.script)

        results = self._build_html(headers, container, script)
        return results

    def _build_html(self, *args):
        results = []
        for a in args:
            if isinstance(a, list):
                results.extend(a)
            elif isinstance(a, six.string_types):
                results.append(a)
            else:
                raise ValueError(type(a))
        return os.linesep.join(results)

    @property
    def script(self):
        scripts = ["var container = document.getElementById('{0}');".format(self.divid),
                   self._nodes_html,
                   self._edges_html,
                   self._data_html,
                   "var options = {};",
                   "var network = new vis.Network(container, data, options);"]
        return scripts

    def _wrap_js(self, script):
        if not isinstance(script, list):
            script = [script]
        # filter None and empty str
        script = [s for s in script if s is not None and len(s) > 0]
        script = self._add_indent(script)
        return ["""<script type="text/javascript">"""] + script + ["""</script>"""]

    def _add_indent(self, script, indent=2):
        """ Indent list of script with specfied number of spaces """
        if not isinstance(script, list):
            script = [script]

        indent = ' ' * indent
        return [indent + s for s in script]

    def add_node(self, node):
        self._nodes.append(node)

    def add_edge(self, node1, node2):
        edge = Edge(node1, node2)
        self._edges.append(edge)

    @property
    def _nodes_html(self):
        nodes_html = [n._repr_html() for n in self._nodes]
        return "var nodes = new vis.DataSet([" + ",".join(nodes_html) + "]);"

    @property
    def _edges_html(self):
        edges_html = [e._repr_html() for e in self._edges]
        return "var edges = new vis.DataSet([" + ",".join(edges_html) + "]);"

    @property
    def _data_html(self):
        return "var data = {nodes: nodes, edges: edges};"


class Color(object):

    def __init__(color=None):
        self.color = color

    def _validate_color(self, color):
        # ToDo: Py3
        if isinstance(color, str):
            return color
        elif isinstance(color, tuple):
            if len(color == 3):
                return "rgb({0}, {1}, {2})".format(*color)
            elif len(color == 4):
                return "rgb({0}, {1}, {2}, {3})".format(*color)
            else:
                raise ValueError


class Node(object):

    def __init__(self, id, label, color=None):
        self.id = id
        self.label = label
        self.color = color

    def _repr_html(self):
        attrs = ['id', 'label', 'color']

        result = []
        for attr in attrs:
            obj = getattr(self, attr)
            if obj is not None:
                if hasattr(obj, '_repr_html_'):
                    value = "{0}:{1}".format(attr, obj._repr_html_())

                elif isinstance(obj, str):
                    value = "{0}:'{1}'".format(attr, obj)
                else:
                    value = "{0}:{1}".format(attr, obj)
                result.append(value)

        return "{" + ', '.join(result) + "}"


class Edge(object):

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def _repr_html(self):
        fmt = "{{from: {node1}, to: {node2}}}"
        return fmt.format(node1=self.node1, node2=self.node2)


