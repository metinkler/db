CREATE TABLE game
	(name 		varchar(256) 	not null unique,
	numPlayers	varchar(256),
	length		int,
	synopsis    varchar(10485760),
	complexity	varchar(15),
	description	varchar(10485760),
    min_players int,
    max_players int,
	primary key(name));


CREATE TABLE board
	(name		varchar(256)		not null unique,
    alt_names   varchar(10000),
    image       varchar(10000),
    min_age     int,
    max_age     int, 
	primary key(name));

CREATE TABLE card
	(name		varchar(256) 	not null unique,
	numCards	varchar(256),
	suits		varchar(256),
    num_players varchar(100),
	primary key(name));

CREATE TABLE domino
	(name			varchar(256)		not null unique,
	numDom			varchar(256),
	addMaterials	varchar(100),
    num_players     varchar(100),
	primary key(name));

CREATE TABLE genre
	(name		varchar(256)		not null unique,
	primary key(name));

CREATE TABLE publisher
	(name		varchar(256)		not null unique,
	primary key(name));

CREATE TABLE mechanic
	(name		varchar(256)		not null unique,
	primary key(name));

CREATE TABLE designer
	(name		varchar(256)		not null unique,
	primary key(name));

CREATE TABLE artist
	(name		varchar(256)		not null unique,
	primary key(name));

CREATE TABLE gameGenre
	(gameName	varchar(256)		not null,
	genreName	varchar(256)		not null,
	primary key(gameName, genreName),
	foreign key(gameName) references game(name),
	foreign key(genreName) references genre(name));

CREATE TABLE gamePublisher
	(gameName	varchar(256)		not null,
	pubName		varchar(256)		not null,
	primary key(gameName, pubName),
	foreign key(gameName) references game(name),
	foreign key(pubName) references publisher(name));

CREATE TABLE gameMechanic
	(gameName	varchar(256)		not null,
	mechName		varchar(256)		not null,
	primary key(gameName, mechName),
	foreign key(gameName) references game(name),
	foreign key(mechName) references mechanic(name));

CREATE TABLE gameDesigner
	(gameName	varchar(256)		not null,
	desName		varchar(256)		not null,
	primary key(gameName, desName),
	foreign key(gameName) references game(name),
	foreign key(desName) references designer(name));

CREATE TABLE gameArtist
	(gameName	varchar(256)		not null,
	artName		varchar(256)		not null,
	primary key(gameName, artName),
	foreign key(gameName) references game(name),
	foreign key(artName) references artist(name));
