drop database if exists manage_pic;
create database manage_pic DEFAULT CHARACTER SET utf8;
use manage_pic;
set names utf8;
SET SESSION storage_engine ="InnoDB";
SET SESSION time_zone ="+8:00";
drop table if exists ordinary_user;
create table ordinary_user(
    id int auto_increment,
    username varchar(50) NOT NULL,
    password varchar(50) NOT NULL,
    companyname  varchar(50) NOT NULL,
    telephone  varchar(11)  NOT NULL,
    email  varchar(50) NOT NULL,
    license varchar(50) NOT NULL,
    created_at DATETIME NOT NULL,
    status int NOT NULL default 2,   -- 放到数据库默认为2,审核通过更改为0， 审核不通过更改为1， 啦黑设置为3
    primary key(id)
)default charset = utf8;
insert into ordinary_user (username, password, companyname, telephone, email, license, status ,created_at) values("mac", "macforlinux", "xuanfengkeji", "15972225587", "jslzc1990@163.com","IMG_00921429279098.JPG" ,0, now());

drop table if exists admin_user;
create table admin_user(
    id int auto_increment,
    username varchar(50) NOT NULL,
    password varchar(50) NOT NULL,
    primary key(id)
    )default charset= utf8;
insert into admin_user (username, password) values("admin","nimda");

drop table if exists menu;
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

drop table if exists game;
create table game(
    id int auto_increment,
    game_name varchar(50) NOT NULL,
    introduction varchar(250) NOT NULL,
    pic varchar(50) NOT NULL,
    created_at DATETIME NOT NULL,
    status int NOT NULL  default 2,    -- 放到数据库默认为2,审核通过更改为0， 审核不通过更改为1   删除 设置为3
    primary key(id)
    )default charset = utf8;

insert into game (game_name, introduction, pic, created_at, status) values ("贪食蛇", "不要贪吃哟，当心吃到了自己的尾巴", "snake.png", now(), 0);

insert into game (game_name, introduction, pic, created_at, status) values ("2048", "人生就像一场游戏，你永远不知道下一个线索出现在哪里", "2048.png", now(), 0);

drop table if exists menu_game;
create table menu_game(
    id int auto_increment,
    menu_id int NOT NULL,
    game_id int NOT NULL,
    user_id int NOt NULL,
    status  int NOT NULL default 2,    -- 菜品游戏放到数据库为2    审核菜单通过后更改status 通过为0   失效为1   删除设置为3

    primary key(id)
    )default charset = utf8;


drop table if exists menu_bonus;
create table menu_bonus(
    id int auto_increment,
    menu_id int NOT NULL,
    user_id int NOt NULL,
    bonus float  NOT NULL default 1,
    created_at DATETIME NOT NULL ,
    status int NOT NULL default 2,    -- 菜品优惠放到数据库为2     审核菜单通过后更改   通过为0 ， 失败为1   删除设置为3
    primary key(id)
    )default charset = utf8;



drop table if exists log;
create table log(
    id int auto_increment,
    ids varchar(20) not null,
    type int not null,
    content varchar(100) not null,
    operator_id int not null,
    created_at DATETIME not null,
    admin int not null, -- 0 普通用户  1  高级用户
    primary key(id)
    )default charset=utf8;



-- 审核 注册公司  通过后 更改status为0 不通过为1
-- 审核 菜单    通过后   更改为0    不通过为1
-- 新增菜单     审核菜单通过后， 设置游戏-菜单为0   同时设置 菜单-优惠为0
-- 删除菜单     设置菜单status为3  设置菜单游戏为1  设置 菜单-优惠为1

drop table if exists menu_material;
create table menu_material(
   id int auto_increment,
   menu_id int not null,
   material_id int not null,
   user_id int not null,
   status int not null default 2,
   primary key(id)
)default charset=utf8;

drop table if exists menu_type;
create table menu_type(
   id int auto_increment,
   menu_id int not null,
   type_id int not null,
   user_id int not null,
   status int not null default 2,
   primary key(id)
   )default charset=utf8;


