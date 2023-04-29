create database geekprofile
DEFAULT CHARACTER SET uft8 COLLATE uft8_general_ci;
USE geekprofile;

CREATE TABLE accounts(
    id int(11) not null auto_increment,
    username varchar(50) not null,
    password varchar(255) not null,
    email varchar(100) not null,
    organisation varchar(100) not null,
    address varchar(100) not null,
    city varchar(100) not null,
    state varchar(100) not null,
    country varchar(100) not null,
    postalcode varchar(100) not null,
    PRIMARY KEY(id)
)ENGINE= InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;