var json = require('./labels.json');


var Client = require('pg-native');
var conString = "postgres://ncowen:1023714@localhost/ncowen_gamesdb";
var client = new Client();
client.connectSync(conString);

for (i=0; i < json.length; i++){
    publishers = client.querySync("SELECT famname FROM boardfamily WHERE boardname = $1::text", [json[i].split("<>")[1]]);
    for (j=0; j < publishers.length; j++){
        publishers[j] = publishers[j].famname;
    }
    //console.log(publishers);
    json[i] = json[i] + publishers.join(", ");
}
console.log(JSON.stringify(json));

