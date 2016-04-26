var json = require('./labels.json');


var Client = require('pg-native');
var conString = "postgres://ncowen:1023714@localhost/ncowen_gamesdb";
var client = new Client();
client.connectSync(conString);

//for (i=0; i < json.length; i++){
    //publishers = client.querySync("SELECT pubname FROM boardpublisher WHERE boardname = $1::text", [json[i].split("<>")[1]]);
    //for (j=0; j < publishers.length; j++){
        //publishers[j] = publishers[j].pubname;
    //}
    ////console.log(publishers);
    //json[i] = json[i] + publishers.join(", ");
//}




for (i=0; i < json.length; i++){
    //publishers = client.querySync("SELECT pubname FROM boardpublisher WHERE boardname = $1::text", [json[i].split("<>")[1]]);
    if (json[i].split("<>")[0] === 'null'){
        //console.log(json[i].split("<>")[1]);
        result = client.querySync("SELECT url FROM card WHERE name = $1::text", [json[i].split("<>")[1]]);

        if (!result[0] || !(url = result[0].url)){
            result = client.querySync("SELECT url FROM domino WHERE name = $1::text", [json[i].split("<>")[1]]);
            url = result[0].url
        }
        //console.log(url);
        label = json[i].split("<>");
        label[0] = url;
        json[i] = label.join("<>");
    }
    //for (j=0; j < publishers.length; j++){
        //publishers[j] = publishers[j].pubname;
    //}
    //console.log(publishers);
    //json[i] = json[i] + publishers.join(", ");
}
console.log(JSON.stringify(json));

