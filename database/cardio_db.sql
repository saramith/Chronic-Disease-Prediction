CREATE DATABASE IF NOT EXISTS geeklogin DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE geeklogin ;
CREATE TABLE IF NOT EXISTS account_stroke ( 
id int(11) NOT NULL AUTO_INCREMENT,
gender int,
age int,
hypertension int,
heart_disease int,
ever_married int,
work_type int,
residence_type int,
avg_glucose_level float,
bmi float,
smoking_status int,
stroke int,
PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;