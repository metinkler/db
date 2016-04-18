CREATE TABLE game
	(name 		varchar(256) 	not null unique,
	length		int,
	synopsis    varchar(10485760),
	complexity	varchar(15),
	description	varchar(10485760),
    min_players int,
    max_players int,
	primary key(name));


CREATE TABLE board
    (bgg_id     int,
    alt_names   varchar(10000),
    image       varchar(10000),
    thumbnail   varchar(10000),
    year_est    int,
    min_age     int,
    users_owned int,
    rating      real,  
	primary key(name)) INHERITS (game);

CREATE TABLE card
	(numCards	varchar(256),
	suits		varchar(256),
    num_players varchar(100),
	primary key(name)) INHERITS (game);

CREATE TABLE domino
	(numDom			varchar(256),
	addMaterials	varchar(100),
    num_players     varchar(100),
	primary key(name)) INHERITS (game);

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

CREATE TABLE family
	(name		varchar(256)		not null unique,
	primary key(name));

CREATE TABLE boardgenre
	(boardName	varchar(256)		not null,
	genreName	varchar(256)		not null,
	primary key(boardName, genreName),
	foreign key(boardName) references board(name),
	foreign key(genreName) references genre(name));

CREATE TABLE boardpublisher
	(boardName	varchar(256)		not null,
	pubName		varchar(256)		not null,
	primary key(boardName, pubName),
	foreign key(boardName) references board(name),
	foreign key(pubName) references publisher(name));

CREATE TABLE boardmechanic
	(boardName	varchar(256)		not null,
	mechName		varchar(256)		not null,
	primary key(boardName, mechName),
	foreign key(boardName) references board(name),
	foreign key(mechName) references mechanic(name));

CREATE TABLE boarddesigner
	(boardName	varchar(256)		not null,
	desName		varchar(256)		not null,
	primary key(boardName, desName),
	foreign key(boardName) references board(name),
	foreign key(desName) references designer(name));

CREATE TABLE boardartist
	(boardName	varchar(256)		not null,
	artName		varchar(256)		not null,
	primary key(boardName, artName),
	foreign key(boardName) references board(name),
	foreign key(artName) references artist(name));

CREATE TABLE boardfamily
	(boardName	varchar(256)		not null,
	famName		varchar(256)		not null,
	primary key(boardName, famName),
	foreign key(boardName) references board(name),
	foreign key(famName) references family(name));
