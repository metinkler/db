var createGraph = require('ngraph.graph');
var createLayout = require('ngraph.offline.layout');
var save = require('ngraph.tobinary');
var g = createGraph();

g.addNode('hello');
g.addNode('world');

g.addLink('space', 'bar');

max = 10000

for (i = 0; i < max; i++){
	g.addLink(i, i+1);
}

for (i = 0; i < max; i += 3){
	g.addLink(i, i+3);
}

for (i = 0; i < max; i += 8){
	g.addLink(i, i+8);
}

var createLayout = require('ngraph.offline.layout');
var layout = createLayout(g);
layout.run();

save(g);