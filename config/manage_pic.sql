drop database if exists manage_pic;
create database manage_pic DEFAULT CHARACTER SET utf8;
use manage_pic;
set names utf8;
SET SESSION storage_engine ="InnoDB";
SET SESSION time_zone ="+8:00";

create table ordinary_user(
    id int auto_increment,
    username varchar(50) NOT NULL,
    password varchar(50) NOT NULL,
    companyname  varchar(50) NOT NULL,
    telephone  varchar(11)  NOT NULL,
    email  varchar(50) NOT NULL,
    license varchar(50) NOT NULL,
    created_at DATETIME NOT NULL,
    status int NOT NULL default 2,   -- 放到数据库默认为2,审核通过更改为0， 审核不通过更改为1
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
    created_at DATETIME NOT NULL ,
    status int NOT NULL default 2,   -- 放到数据库默认为2,审核通过更改为0， 审核不通过更改为1， 删除状态为3
    primary key(id)
    )default charset = utf8;

create table game(
    id int auto_increment,
    game_name varchar(50) NOT NULL,
    introduction varchar(250) NOT NULL,
    pic varchar(50) NOT NULL,
    created_at DATETIME NOT NULL,
    status int NOT NULL  default 0,    -- 放到数据库默认为2,审核通过更改为0， 审核不通过更改为1
    primary key(id)
    )default charset = utf8;

create table menu_game(
    id int auto_increment,
    menu_id int NOT NULL,
    game_id int NOT NULL,
    status  int NOT NULL default 0,    -- 菜品游戏有效为0   设置失效为1

    primary key(id)
    )default charset = utf8;



create table menu_bonus(
    id int auto_increment,
    menu_id int NOT NULL,
    bonus float  NOT NULL default 1,
    created_at DATETIME NOT NULL ,
    status int NOT NULL default 0,    -- 菜品优惠默认为有效  设置失效为1
    primary key(id)
    )default charset = utf8;





-- 审核 注册公司  通过后 更改status为0 不通过为1
-- 审核 菜单    通过后   更改为0    不通过为1
-- 新增菜单     审核菜单通过后， 设置游戏-菜单为0   同时设置 菜单-优惠为0
-- 删除菜单     设置菜单status为3  设置菜单游戏为1  设置 菜单-优惠为1