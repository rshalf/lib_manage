CREATE DATABASE IF NOT EXISTS LibManage;
USE `LibManage`;
 
 -- create tables
 -- this database contain 4 main tables
 -- 1.Admin - login details of all the admins.
 --  2.Book -details of books in the library
 -- 3.Member - details of all members
 -- 4.borrowHistory
-- 5. cuurentborrowed
 
CREATE TABLE IF NOT EXISTS `admin`(
    `admin_id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(255)NOT NULL,
    PRIMARY KEY (`admin_id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO `admin` (`admin_id`,`username`, `password`) 
VALUES (1,'admin1', 'password123'),
	   (2,'admin1', 'password245');


CREATE TABLE IF NOT EXISTS `books`(
    `book_id` int(11) NOT NULL AUTO_INCREMENT,
    `book_name` varchar(200)NOT NULL,
    `author_name` varchar(100) NOT NULL,
    `genre` varchar(100) NOT NULL,
    `quantity` int DEFAULT 0,
    CHECK(quantity>=0)  ,  
    PRIMARY KEY (`book_id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO `books` (`book_name`, `author_name`, `genre`, `quantity`) 
VALUES ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 10),
       ('1984', 'George Orwell', 'Dystopian', 5),
       ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 8);


CREATE TABLE IF NOT EXISTS `members`(
    `member_id` int(11) NOT NULL AUTO_INCREMENT,
    `member_name` varchar(100) NOT NULL    ,
    PRIMARY KEY(`member_id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO `members` (`member_id`,`member_name`) 
VALUES (1,'member1'),
       (2,'member2'),
       (3,'member3');

CREATE TABLE IF NOT EXISTS `borrowhistory`(
    `borrow_id` int(100) NOT NULL AUTO_INCREMENT,
    `member_id` int (11) NOT NULL ,
    `member_name` varchar(100) NOT NULL,
    `book_id` int(11) NOT NULL,
    `book_name` varchar(200) NOT NULL,
    `borrow_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `return_date` TIMESTAMP NULL,
    PRIMARY KEY(`borrow_id`),
    FOREIGN KEY (`member_id`) REFERENCES members(`member_id`),
    FOREIGN KEY (`book_id`) REFERENCES books(`book_id`)

)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `currentborrowed`(
    `member_id` int (11) NOT NULL ,
    `member_name` varchar(100) NOT NULL,
    `book_id` int(11) NOT NULL,
    `borrow_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `book_name` varchar(200) NOT NULL,
    PRIMARY KEY (`member_id`, `book_id`),  -- Composite primary key
    FOREIGN KEY (`member_id`) REFERENCES `members`(`member_id`),
    FOREIGN KEY (`book_id`) REFERENCES `books`(`book_id`)

)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
