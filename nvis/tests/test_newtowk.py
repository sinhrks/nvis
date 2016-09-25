#!/usr/bin/env python
# coding: utf-8

import unittest

from nvis import Network, Node


class TestNetwork(unittest.TestCase):

    def test_basic(self):
        """ http://visjs.org/examples/network/basicUsage.html """

        n = Network(divid='xxx')
        n.add_node(Node(1, 'Node1'))
        n.add_node(Node(2, 'Node2'))
        n.add_node(Node(3, 'Node3'))
        n.add_node(Node(4, 'Node4'))
        n.add_node(Node(5, 'Node5'))
        n.add_edge(1, 3)
        n.add_edge(1, 2)
        n.add_edge(2, 4)
        n.add_edge(2, 5)

        result = n.to_html()
        exp = """<script>
  require(["https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"], function(lib) {
    window.vis = jQuery.extend(true, {}, lib);
  });
</script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="xxx" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var container = document.getElementById('xxx');
  var nodes = new vis.DataSet([{id:1, label:'Node1'},{id:2, label:'Node2'},{id:3, label:'Node3'},{id:4, label:'Node4'},{id:5, label:'Node5'}]);
  var edges = new vis.DataSet([{from: 1, to: 3},{from: 1, to: 2},{from: 2, to: 4},{from: 2, to: 5}]);
  var data = {nodes: nodes, edges: edges};
  var options = {};
  var network = new vis.Network(container, data, options);
</script>"""
        self.assertEqual(result, exp)

    def test_colors(self):
        """ http://visjs.org/examples/network/nodeStyles/colors.html """

        # ToDo: hover doesn't work

        n = Network(divid='xxx')
        n.add_node(Node(1, 'Node1', color='lime'))
        n.add_node(Node(2, 'Node2', color=(255, 168, 7)))
        n.add_node(Node(3, 'Node3', color='#7BE141'))
        n.add_node(Node(4, 'Node4', color=(97, 195, 238, 0.5)))
        n.add_node(Node(5, 'Node5', color={'background': 'pink', 'border': 'purple'}))
        n.add_node(Node(6, 'Node6', color={'background': '#F03967', 'border': '#713E7F',
                                           'highlight': {'background': 'red', 'border': 'black'}}))
        n.add_node(Node(7, 'Node7', color={'background': 'cyan', 'border': 'blue',
                                           'highlight': {'background': 'red', 'border': 'blue'},
                                           'hover': {'background': 'white', 'border': 'red'}}))
        n.add_edge(1, 3)
        n.add_edge(1, 2)
        n.add_edge(2, 4)
        n.add_edge(2, 5)
        n.add_edge(2, 6)
        n.add_edge(4, 7)

        result = n.to_html()
        exp = """<script>
  require(["https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"], function(lib) {
    window.vis = jQuery.extend(true, {}, lib);
  });
</script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="xxx" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var container = document.getElementById('xxx');
  var nodes = new vis.DataSet([{id:1, label:'Node1', color:'lime'},{id:2, label:'Node2', color:'rgb(255, 168, 7)'},{id:3, label:'Node3', color:'#7BE141'},{id:4, label:'Node4', color:'rgba(97, 195, 238, 0.5)'},{id:5, label:'Node5', color:{background:'pink', border:'purple'}},{id:6, label:'Node6', color:{background:'#F03967', border:'#713E7F', highlight:{background:'red', border:'black'}}},{id:7, label:'Node7', color:{background:'cyan', border:'blue', highlight:{background:'red', border:'blue'}, hover:{background:'white', border:'red'}}}]);
  var edges = new vis.DataSet([{from: 1, to: 3},{from: 1, to: 2},{from: 2, to: 4},{from: 2, to: 5},{from: 2, to: 6},{from: 4, to: 7}]);
  var data = {nodes: nodes, edges: edges};
  var options = {};
  var network = new vis.Network(container, data, options);
</script>"""
        self.assertEqual(result, exp)
