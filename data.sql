DROP DATABASE IF EXISTS `app_data`;
CREATE DATABASE IF NOT EXISTS `app_data`;
USE `app_data`;

CREATE TABLE IF NOT EXISTS `user` (
    username        VARCHAR(20) NOT NULL,
    contactnumber   VARCHAR(10)     NOT NULL,
    fname           VARCHAR(20) NOT NULL,
    mname           VARCHAR(20) NOT NULL,
    lname           VARCHAR(20) NOT NULL,
    PRIMARY KEY (`username`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `category` (
    categoryname  VARCHAR(10) NOT NULL,
    datecreated   DATE        NOT NULL,
    PRIMARY KEY (`categoryname`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `task` (
    taskid          VARCHAR(20) NOT NULL,
    taskdescription VARCHAR(30) NOT NULL,
    dategiven       DATE        NOT NULL,
    datestarted     DATE        NULL,
    datefinished    DATE        NULL,
    deadline        DATE        NULL,
    taskstatus      BIT(8)      NOT NULL, 
    categoryname    VARCHAR(20) NOT NULL,
    PRIMARY KEY (`taskid`),
    KEY `task_categoryname_fk` (`categoryname`),
    CONSTRAINT `task_categoryname_fk` 
        FOREIGN KEY (`categoryname`) REFERENCES `category` (`categoryname`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `user_task` (
    username        VARCHAR(20) NOT NULL,
    taskid          VARCHAR(20) NOT NULL,
    KEY `user_task_username_fk` (`username`),
    KEY `user_task_taskid_fk` (`taskid`),
    CONSTRAINT `user_task_username_fk` 
        FOREIGN KEY (`username`) REFERENCES `user` (`username`),
    CONSTRAINT `user_task_taskid_fk` 
        FOREIGN KEY (`taskid`) REFERENCES `task` (`taskid`)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;