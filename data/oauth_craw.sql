CREATE DATABASE IF NOT EXISTS OauthCraw DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
use OauthCraw;
CREATE TABLE IF NOT EXISTS `target`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `url` VARCHAR(60) NOT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `result`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `url` VARCHAR(60) NOT NULL,
   `isUse` TINYINT NOT NULL,
   `oauthService` VARCHAR(30) NOT NULL,
   `oauthLink` TEXT NOT NULL,
   `loginLink` TEXT NOT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


#load data infile '/home/rebirth/Desktop/oauth_craw/top-100000.csv' into table target fields terminated by ',' optionally enclosed by '"' escaped by '"' lines terminated by '\n';