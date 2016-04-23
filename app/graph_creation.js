var createGraph = require('ngraph.graph');
var createLayout = require('ngraph.offline.layout');
var save = require('ngraph.tobinary');
var g = createGraph();

g.addNode('hello');
g.addNode('world');

g.addLink('space', 'bar');

function getLabel(id){ 
	publishers = ["Publisher One", "Publisher Two", "Publisher Three", "Publisher Four"]
	return id + "<>" + "this is a long game title" + "<>" + "https://cf.geekdo-images.com/images/pic934018_md.jpg" + "<>" + publishers.join(", ");
}

max = 10000

for (i = 0; i < max; i++){
	g.addLink(getLabel(i), getLabel(i+1));
}

for (i = 0; i < max; i += 3){
	g.addLink(getLabel(i), getLabel(i+3));
}

for (i = 0; i < max; i += 8){
	g.addLink(getLabel(i), getLabel(i+8));
}

var createLayout = require('ngraph.offline.layout');
var layout = createLayout(g);
layout.run();

save(g);