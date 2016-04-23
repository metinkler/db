var createGraph = require('ngraph.graph');
var createLayout = require('ngraph.offline.layout');
var save = require('ngraph.tobinary');
var g = createGraph();
var pg = require('pg');
var conString = "postgres://ncowen:1023714@localhost/ncowen_gamesdb";


function getLabel(id){ 
	publishers = ["Publisher One", "Publisher Two", "Publisher Three", "Publisher Four"];
    game_name = "this is a long game title";
    thumbnail = "https://cf.geekdo-images.com/images/pic934018_md.jpg";
	return id + "<>" + game_name + "<>" +  thumbnail + "<>" + publishers.join(", ");
}

function queryGamesDb(query, callback){
    client = new pg.Client(conString);
    client.connect(function(err) {
        if(err) {
            return console.error('could not connect to postgres', err);
        }
        client.query(query, function(err, result) {
            if(err) {
                return console.error('error running query', err);
            }
            client.end();
            callback(result.rows);
            //output: Tue Jan 15 2013 19:12:47 GMT-600 (CST)
            //client.end();
        });
    });
}

//pubQuery = "SELECT A.name as game, B.pubname as publisher\
            //FROM game A \
            //LEFT JOIN boardpublisher B \
            //ON A.name = B.boardname \
            //AS GP;"

pubQuery = "SELECT a.boardname as game1, b.boardname as game2 \
            FROM boardpublisher a INNER JOIN boardpublisher b \
            ON a.pubname = b.pubname \
            WHERE a.boardname <> b.boardname\
            LIMIT 1000000;";

queryGamesDb(pubQuery, function (result){
    //console.log(result)
    var i;
    for (i = 0; i < result.length; i++){
       g.addLink(result[i].game1, result[i].game2);  
    }
    var createLayout = require('ngraph.offline.layout');
    var layout = createLayout(g);
    layout.run();

    save(g);
});



//client.end();
//max = 10000

//for (i = 0; i < max; i++){
	//g.addLink(getLabel(i), getLabel(i+1));
//}

//for (i = 0; i < max; i += 3){
	//g.addLink(getLabel(i), getLabel(i+3));
//}

//for (i = 0; i < max; i += 8){
	//g.addLink(getLabel(i), getLabel(i+8));
//}

