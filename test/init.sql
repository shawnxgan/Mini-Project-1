-- Data prepared by CMPUT 291 TAs
-- Published after the assignments are marked

-- First, Let's delete existing data:

PRAGMA foreign_keys = ON;

delete from deliveries;
delete from olines;
delete from orders;
delete from carries;
delete from customers;
delete from stores;
delete from products;
delete from categories;
delete from agents;


--Now, Let's insert some test data:

INSERT INTO categories VALUES('dai','dairy');
INSERT INTO categories VALUES('bak','Bakery');
INSERT INTO categories VALUES('mea','Meat and seafood');
INSERT INTO categories VALUES('bev','Beverages ');
INSERT INTO categories VALUES('can','Canned Goods ');
INSERT INTO categories VALUES('dry','Dry Goods ');
INSERT INTO categories VALUES('cle','Cleaners');
INSERT INTO categories VALUES('per','Personal Care');


INSERT INTO products VALUES('p1','4L milk 1%','ea','dai');
INSERT INTO products VALUES('p2','dozen large egg','ea','dai');
INSERT INTO products VALUES('p3','cream cheese','ea','dai');
INSERT INTO products VALUES('p4','400g coffee','ea','bev');
INSERT INTO products VALUES('p5','1.5L orange juice','ea','bev');
INSERT INTO products VALUES('p6','600g lean beef','ea','mea');
INSERT INTO products VALUES('p7','500g poultry','ea','mea');
INSERT INTO products VALUES('p8','1L detergent','ea','cle');
INSERT INTO products VALUES('p9','300ml dishwashing liquid','ea','cle');
INSERT INTO products VALUES('p10','400ml canned beef ravioli','ea','can');
INSERT INTO products VALUES('p11','500ml canned noodle soup','ea','can');


INSERT INTO stores VALUES(1,'Canadian Tire','780-111-2222','Edmonton South Common');
INSERT INTO stores VALUES(2,'Canadian Superstore','780-111-3333','Edmonton South Common');
INSERT INTO stores VALUES(3,'Walmart','587-111-222','Edmonton Westmount');
INSERT INTO stores VALUES(4,'Save-On-Foods','780-333-444','101-109 St NW');
INSERT INTO stores VALUES(5,'No Frills','780-444-555','104-80 Ave');
INSERT INTO stores VALUES(6,'Safeway','780-555-666','109-82 Ave');
INSERT INTO stores VALUES(7,'Organic Market','780-666-777','110-83 Ave');
INSERT INTO stores VALUES(8,'lucky 97','780-666-777','56-132 St NW');


INSERT INTO customers VALUES('c1','davood','CS Dept,University of Alberta', 'b7d5e587cf10383345c7739474da087c03a9cb6cf736a6e222aef9837cc54191');
INSERT INTO customers VALUES('c2','john doe','111-222 Ave', '96d9632f363564cc3032521409cf22a852f2032eec099ed5967c0d000cec607a');
INSERT INTO customers VALUES('c3','peter','102-83 Ave', '026ad9b14a7453b7488daa0c6acbc258b1506f52c441c7c465474c1a564394ff');
INSERT INTO customers VALUES('c4','jessica','101-54 St NW', 'e1fc45f7880e0505ff0b6a079b9af149f225e260f59b1d20225357a8cce8ffd8');
INSERT INTO customers VALUES('c5','allen','4520-9569 Vegas Rd NW', 'ec47860233d36cad00db3ed18c8ed7d57690cb8689caa86cce93ef75d767e7f1');
INSERT INTO customers VALUES('c6','paul','105-74 Ave', '0357513deb903a056e74a7e475247fc1ffe31d8be4c1d4a31f58dd47ae484100');
INSERT INTO customers VALUES('c7','ashley','78-23 Ave', 'c64975ba3cf3f9cd58459710b0a42369f34b0759c9967fb5a47eea488e8bea79');
INSERT INTO customers VALUES('c8','emma','96-89 St NW', 'f4aa0655cdb8d4fcf6f719c7a786de10556783c70bfb8ef1d78923482fe6ebbc');
INSERT INTO customers VALUES('c9','mia','87 Strathearn Crescent NW', 'a6ae07ad556c5f9348cc09c16ed17a437e65acc71e689c1b19f872f1dab3c9c1');
INSERT INTO customers VALUES('c10','oliver','91 Saskatchewan Dr', '7dfef7aed2105b7eceb4d34e1ad84fdad4693bd5de041e1b47079efeb6001a83');

INSERT INTO agents VALUES('a1', 'steve rogers', 'f148389d080cfe85952998a8a367e2f7eaf35f2d72d2599a5b0412fe4094d65c');
INSERT INTO agents VALUES('a2', 'tony stark', 'e9e326d5f3b4741fe5967b5f9f3997e6275331ba18567ef9ef9e0e3a00e78371');
INSERT INTO agents VALUES('a3', 'bruce banner', '17fc19d5d0ffa46dbe6a1c7c57e969aa6d5760544d96d5f2b0e96a1f66c7ea4b');
INSERT INTO agents VALUES('a4', 'natasha romanoff', 'd334cbac4bb3f242dfe5e11a656333345ce05c8409bc347be201f2447e14b480');
INSERT INTO agents VALUES('a5', 'clint barton', '0a2e07846fb8c883bceaa0b0f8486ec093b93a6b149c3db5de241a14037575c9');
INSERT INTO agents VALUES('a6', 'stan lee', '1a5e497a2bfa7bfd8aab38a1d576ed882f4a82e855ec610880b4c186ec3f4e73');

INSERT INTO carries VALUES(2,'p1',0,4.7);
INSERT INTO carries VALUES(2,'p2',80,2.6);
INSERT INTO carries VALUES(1,'p1',60,5.5);
INSERT INTO carries VALUES(3,'p1',100,4.5);
INSERT INTO carries VALUES(1,'p3',0,3.5);
INSERT INTO carries VALUES(4,'p4',50,5);
INSERT INTO carries VALUES(4,'p7',70,9);
INSERT INTO carries VALUES(6,'p5',65,5);
INSERT INTO carries VALUES(5,'p1',100,6.5);
INSERT INTO carries VALUES(5,'p9',150,6);
INSERT INTO carries VALUES(2,'p8',90,7);
INSERT INTO carries VALUES(2,'p3',0,2.0);
INSERT INTO carries VALUES(4,'p3',0,.5);


INSERT INTO orders VALUES(1,'c1','2017-09-26','Athabasca Hall, University of Alberta');
INSERT INTO orders VALUES(2,'c2','2017-09-26','111-222 Ave');
INSERT INTO orders VALUES(3,'c3',date('now','-5 day'),'134-53 Ave');
INSERT INTO orders VALUES(4,'c3',date('now','-6 day'),'134-53 Ave');
INSERT INTO orders VALUES(5,'c4',date('now','-3 day'),'75-103 St');
INSERT INTO orders VALUES(6,'c4',date('now','-2 day'),'75-103 St');
INSERT INTO orders VALUES(7,'c5',date('now','-12 day'),'102-114 St');
INSERT INTO orders VALUES(8,'c6',date('now'),'87-Jasper Ave');
INSERT INTO orders VALUES(9,'c2',date('now'),'76-102 St');
INSERT INTO orders VALUES(10,'c2',date('now'),'79-101 St');
INSERT INTO orders VALUES(11,'c8',date('now'),'105-83 Ave');


INSERT INTO olines VALUES(1, 2,'p2',2,2.8);
INSERT INTO olines VALUES(2, 2,'p1',1,4.7);
INSERT INTO olines VALUES(3, 2,'p2',4,2.6);
INSERT INTO olines VALUES(4, 1,'p1',1,3);
INSERT INTO olines VALUES(5, 2,'p2',2,2.6);
INSERT INTO olines VALUES(5, 3,'p1',6,5.5);
INSERT INTO olines VALUES(6, 4,'p4',1,6);
INSERT INTO olines VALUES(6, 4,'p7',1,10);
INSERT INTO olines VALUES(6, 6,'p5',2,4.3);
INSERT INTO olines VALUES(7, 5,'p1',2,6);
INSERT INTO olines VALUES(7, 5,'p9',1,6);
INSERT INTO olines VALUES(8, 2,'p8',1,7);
INSERT INTO olines VALUES(1, 4,'p3',1,5);
INSERT INTO olines VALUES(7, 2,'p2',1,6);
INSERT INTO olines VALUES(11, 3,'p1',2,4.5);



INSERT INTO deliveries VALUES(1, 1,'2017-10-02 23:37:46',NULL);
INSERT INTO deliveries VALUES(2, 2,'2017-10-02 19:37:46','2017-10-02 23:37:46');
INSERT INTO deliveries VALUES(3, 10,datetime('now'),NULL);
INSERT INTO deliveries VALUES(4, 3,datetime('now','-4 day'),datetime('now','-3 day'));
INSERT INTO deliveries VALUES(5, 4,datetime('now','-6 day'),datetime('now','-2 day'));
INSERT INTO deliveries VALUES(6, 5,datetime('now','-2 day'),datetime('now','-1 day'));
INSERT INTO deliveries VALUES(7, 6,datetime('now','-1 day'),NULL);
INSERT INTO deliveries VALUES(8, 7,datetime('now','-6 day'),NULL);
INSERT INTO deliveries VALUES(9, 8,datetime('now'),NULL);
INSERT INTO deliveries VALUES(10, 9,datetime('now'),NULL);
