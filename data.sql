DROP DATABASE IF EXISTS `app_data`;
CREATE DATABASE IF NOT EXISTS `app_data`;
USE `app_data`;

CREATE TABLE IF NOT EXISTS `category` (
    categoryname  VARCHAR(20) NOT NULL,
    datecreated   DATE        NOT NULL,
    PRIMARY KEY (`categoryname`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `task` (
    taskid          VARCHAR(10) NOT NULL,
    taskdescription VARCHAR(30) NOT NULL,
    dategiven       DATE        NOT NULL,
    datestarted     DATE        NULL,
    datefinished    DATE        NULL,
    deadline        DATE        NULL,
    taskstatus      BIT(8)      NOT NULL, 
    categoryname    VARCHAR(20) NULL,
    PRIMARY KEY (`taskid`),
    KEY `task_categoryname_fk` (`categoryname`),
    CONSTRAINT `task_categoryname_fk` 
        FOREIGN KEY (`categoryname`) REFERENCES `category` (`categoryname`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;



INSERT INTO category VALUES ('academics', CURDATE());
INSERT INTO category VALUES ('chores', CURDATE());