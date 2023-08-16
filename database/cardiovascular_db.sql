CREATE DATABASE IF NOT EXISTS geeklogin DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE geeklogin ;
CREATE TABLE IF NOT EXISTS account_cardiovascular ( 
id int(11) NOT NULL AUTO_INCREMENT,
age1 int,
gender1 int,
height float,
weight float,
ap_hi int,
ap_lo int,
cholesterol int,
glu int,
smoke int,
alco int,
active int,
CARDIO_DISEASE int,
PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;