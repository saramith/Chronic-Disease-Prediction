CREATE DATABASE IF NOT EXISTS geeklogin DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE geeklogin ;
CREATE TABLE IF NOT EXISTS account_dia ( 
id int(11) NOT NULL AUTO_INCREMENT,
pregnancies int,
glucose int,
bloodpressure int,
skinthickness int,
insulin int,
bmi_dia float,
diabetes_pedigree_fnc float,
age_dia int,
outcome int,
PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;