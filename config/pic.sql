drop database if exists manage_pic;
create database manage_pic DEFAULT CHARACTER SET utf8;
use manage_pic;
set names utf8;
SET SESSION storage_engine ="InnoDB";
SET SESSION time_zone ="+8:00";

-- create table user(
--    id int auto_increment,
--    username varchar(50) NOT NULL ,
--    password varchar(50) NOT NULL ,
--    primary key (id)
--    ) default charset = utf8;
-- */
create table ordinary_user(
    id int auto_increment,
    username varchar(50) NOT NULL,
    password varchar(50) NOT NULL,
    companyname  varchar(50) NOT NULL,
    telephone  varchar(11)  NOT NULL,
    email  varchar(50) NOT NULL,
    license varchar(50) NOT NULL,
    status int NOT NULL default 0,   -- 注册放到数据库默认为0,审核通过更改为1， 审核不通过更改为2
    primary key(id)
)default charset = utf8;

create table admin_user(
    id int auto_increment,
    username varchar(50) NOT NULL,
    password varchar(50) NOT NULL,
    primary key(id)
    )default charset= utf8;

create table menu(
    id int auto_increment,
    name varchar(50) NOT NULL,
    introduction varchar(250) NOT NULL,
    pic varchar(50) NOT NULL,
    user_id int NOT NULL,
    status int NOT NULL default 0,
    primary key(id)
    )default charset = utf8;

create table game(
    id int auto_increment,
    game_name varchar(50) NOT NULL,
    introduction varchar(250) NOT NULL,
    pic varchar(50) NOT NULL,

    status int NOT NULL  default 0,
    primary key(id)
    )default charset = utf8;

create table menu_game(
    id int auto_increment,
    menu_id int NOT NULL,
    game_id int NOT NULL,
    status  int NOT NULL default 0,

    primary key(id)
    )default charset = utf8;



create table menu_bonus(
    id int auto_increment,
    menu_id int NOT NULL,
    bonus float  NOT NULL default 1,
    status int NOT NULL default 0,
    primary key(id)
    )default charset = utf8;



