drop database if exists manage_pic;
create database manage_pic DEFAULT CHARACTER SET utf8;

set names utf8;
SET SESSION storage_engine ="InnoDB";
SET SESSION time_zone ="+8:00";
use manage_pic;
create table user(
    id int auto_increment,
    username varchar(50) NOT NULL ,
    password varchar(50) NOT NULL ,
    primary key (id)
    ) default charset = utf8;
