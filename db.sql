create database ylog;
use ylog;
create table tags(
	tag_id int primary key auto_increment,
	tag_name varchar(20) not null
);
create table artical(
    ar_id int primary key auto_increment,
    ar_tittle varchar(30) not null,
    ar_content text not null,
    ar_date varchar(15) not null,
    ar_sketch text not null,
    ar_thumbnail varchar(50),
    ar_tags int not null,
    constraint ar_tags foreign key(ar_tags) references tags(tag_id)
);
create table admin(
	ad_id int primary key auto_increment,
	ad_user varchar(10) unique key not null,
	ad_pwd char(32) not null
);
create table note_categories(
	nc_id int primary key auto_increment,
	nc_name varchar(20) not null
);
create table notes(
	nt_id int primary key auto_increment,
	nt_tittle varchar(20) not null,
	nt_content text not null,
	nt_cate int not null,
	constraint nt_cate foreign key(nt_cate) references note_categories(nc_id)
);
create table yclass_users(
	yu_id int primary key auto_increment,
	yu_useranme varchar(20) not null,
	yu_realname varchar(20) not null,
	yu_email varchar(30),
	yu_phone varchar(11)
);
create table yallow_users(
	ya_id int primary key auto_increment,
	ya_username varchar(20) not null
);
create table yclass_code(
	yc_id int primary key auto_increment,
	code char(6) not null,
	isuse varchar(5) default 'False'
);