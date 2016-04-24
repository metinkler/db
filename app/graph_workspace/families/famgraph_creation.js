var createGraph = require('ngraph.graph');
var createLayout = require('ngraph.offline.layout');
var save = require('ngraph.tobinary');
var g = createGraph();
var Client = require('pg-native');
var conString = "postgres://ncowen:1023714@localhost/ncowen_gamesdb";
var client = new Client();

maxNumGraphNodes = 10000000;

function getPublishers(game){
    var publishers =  client.querySync("SELECT pubname FROM boardpublisher WHERE boardname = $1::text", [game]); 
    for (i=0; i < publishers.length; i++){
        publishers[i] = publishers[i].pubname
    }
    return publishers;
}

function getNode(game_name, thumbnail, id){ 
    //publishers = getPublishers(game_name);
	return id + "<>" + game_name + "<>" +  thumbnail + "<>";// + publishers.join(", ");
}

query = "SELECT I.game1 as game1, G.thumbnail as thumbnail1, G.bgg_id as id1, I.game2 as game2, H.thumbnail as thumbnail2, H.bgg_id as id2\
         FROM ( SELECT a.boardname as game1, b.boardname as game2\
                FROM boardfamily a INNER JOIN boardfamily b\
                ON a.famname = b.famname\
                WHERE a.boardname < b.boardname\
                LIMIT " + maxNumGraphNodes + ") as I\
         INNER JOIN board G ON (G.name = I.game1)\
         INNER JOIN board H ON (H.name = I.game2);"

client.connectSync(conString);
var result = client.querySync(query);
for (i = 0; i < result.length; i++){
    firstnode = getNode(result[i].game1, result[i].thumbnail1, result[i].id1);
    secondnode = getNode(result[i].game2, result[i].thumbnail2, result[i].id2);
    g.addLink(firstnode, secondnode);  
}

result = client.querySync("SELECT name FROM card");
for (i = 0; i < result.length; i++){
    node = getNode(result[i].name, null, null);
    g.addNode(node);
}

result = client.querySync("SELECT name FROM domino");
for (i = 0; i < result.length; i++){
    node = getNode(result[i].name, null, null);
    g.addNode(node);
}

var createLayout = require('ngraph.offline.layout');
var layout = createLayout(g);
layout.run();

save(g);

