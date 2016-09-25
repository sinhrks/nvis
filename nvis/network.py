#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os
import six

from nvis.base import _JSObject
from nvis.color import Color


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

        css_fmt = """<link rel="stylesheet" href="{0}" type="text/css">"""
        css = css_fmt.format(css)

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
                   self._nodes_script,
                   self._edges_script,
                   "var data = {nodes: nodes, edges: edges};",
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
    def _nodes_script(self):
        scripts = [n.script for n in self._nodes]
        return "var nodes = new vis.DataSet([" + ",".join(scripts) + "]);"

    @property
    def _edges_script(self):
        scripts = [e.script for e in self._edges]
        return "var edges = new vis.DataSet([" + ",".join(scripts) + "]);"


class Node(object):

    def __init__(self, id, label, color=None):
        self.id = id
        self.label = label

        if color is not None:
            self.color = Color(color=color)
        else:
            self.color = None

    @property
    def script(self):
        attrs = ['id', 'label', 'color']

        result = []
        for attr in attrs:
            obj = getattr(self, attr)
            if obj is not None:
                if hasattr(obj, 'script'):
                    value = "{0}:{1}".format(attr, obj.script)

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

    @property
    def script(self):
        fmt = "{{from: {node1}, to: {node2}}}"
        return fmt.format(node1=self.node1, node2=self.node2)
