CREATE TABLE game
	(name 		varchar(20) 	not null unique,
	numPlayers	int,
	length		int,
	price		decimal(6,2),
	rules		text,
	complexity	varchar(15),
	description	text,
	primary key(name));

CREATE TABLE genre
	(name		varchar(20)		not null unique,
	description	text,
	primary key(name));

CREATE TABLE publisher
	(name		varchar(20)		not null unique,
	address		varchar(100),
	website		varchar(100),
	description	text,
	primary key(name));

CREATE TABLE board
	(name		varchar(20)		not null unique,
	age			int,
	pieces		varchar(100),
	primary key(name));

CREATE TABLE dice
	(name		varchar(20)		not null unique,
	numDice		int,
	type		varchar(20),
	primary key(name));

CREATE TABLE card
	(name		varchar(20)	not null unique,
	numCards	int,
	suits		varchar(20),
	primary key(name));

CREATE TABLE domino
	(name			varchar(20)		not null unique,
	numDom			int,
	addMaterials	varchar(100),
	primary key(name));

CREATE TABLE rpg
	(name			varchar(20)		not null unique,
	loreMaterials	varchar(100),
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
	foreign key(pubName) references publisher(name));CREATE TABLE game
	(name 		varchar(20) 	not null unique,
	numPlayers	int,
	length		int,
	price		decimal(6,2),
	rules		varchar(max),
	complexity	varchar(15),
	description	varchar(max),
	primary key(name));

CREATE TABLE genre
	(name		varchar(20)		not null unique,
	description	varchar(max),
	primary key(name));

CREATE TABLE publisher
	(name		varchar(20)		not null unique,
	address		varchar(100),
	website		varchar(100),
	description	varchar(max),
	primary key(name));

CREATE TABLE board
	(name		varchar(20)		not null unique,
	age			int,
	pieces		varchar(100)
	primary key(name));

CREATE TABLE dice
	(name		varchar(20)		not null unique,
	numDice		int,
	type		varchar(20)
	primary key(name));

CREATE TABLE card
	(name		varchar(20))	not null unique,
	numCards	int,
	suits		varchar(20)
	primary key(name));

CREATE TABLE domino
	(name			varchar(20)		not null unique,
	numDom			int,
	addMaterials	varchar(100),
	primary key(name));

CREATE TABLE rpg
	(name			varchar(20)		not null unique,
	loreMaterials	varchar(100),
	primary key(name));

CREATE TABLE gameGenre
	(gameName	varchar(20)		not null,
	genreName	varchar(20)		not null,
	primary key(gameName, gameGenre),
	foreign key(gameName) references game(name),
	foreign key(genreName) references genre(name));

CREATE TABLE gamePublisher
	(gameName	varchar(20)		not null,
	pubName		varchar(20)		not null,
	primary key(gameName, pubName),
	foreign key(gameName) references game(name),
	foreign key(pubName) references publisher(name));