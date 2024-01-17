drop database  accelerate;
drop database  cerbos;
create database if not exists accelerate;
create database if not exists cerbos;
create user if not exists 'accelerate'@'%' identified WITH mysql_native_password BY 'accelerate';
grant all privileges on accelerate.* to 'accelerate'@'%';
grant all privileges on cerbos.* to 'accelerate'@'%';