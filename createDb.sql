CREATE TABLE game
	(name 		varchar(20) 	not null unique,
	numPlayers	varchar(20),
	length		int,
	mechanics   varchar(10485760),
	complexity	varchar(15),
	description	varchar(10485760),
	primary key(name));

CREATE TABLE genre
	(name		varchar(20)		not null unique,
	description	varchar(10485760),
	primary key(name));

CREATE TABLE publisher
	(name		varchar(20)		not null unique,
	address		varchar(100),
	website		varchar(100),
	description	varchar(10485760),
	primary key(name));

CREATE TABLE board
	(name		varchar(20)		not null unique,
	age			varchar(20),
    alt_names   varchar(10000),
    artists     varchar(10485760),
	primary key(name));

CREATE TABLE card
	(name		varchar(20) 	not null unique,
	numCards	varchar(20),
	suits		varchar(20),
	primary key(name));

CREATE TABLE domino
	(name			varchar(20)		not null unique,
	numDom			varchar(20),
	addMaterials	varchar(100),
	primary key(name));

CREATE TABLE gameGenre
	(gameName	varchar(20)		not null,
	genreName	varchar(20)		not null,
	primary key(gameName, genreName),
	foreign key(gameName) references game(name),
	foreign key(genreName) references genre(name));

CREATE TABLE gamePublisher
	(gameName	varchar(20)		not null,
	pubName		varchar(20)		not null,
	primary key(gameName, pubName),
	foreign key(gameName) references game(name),
	foreign key(pubName) references publisher(name));
