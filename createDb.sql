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

CREATE TABLE genre
	(name		varchar(256)		not null unique,
	description	varchar(10485760),
	primary key(name));

CREATE TABLE publisher
	(name		varchar(256)		not null unique,
	address		varchar(100),
	website		varchar(100),
	description	varchar(10485760),
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
