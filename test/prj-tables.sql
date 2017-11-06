CREATE TABLE IF NOT EXISTS agents (
  aid           text,
  name          text,
  pwd       	text,
  primary key (aid));
CREATE TABLE IF NOT EXISTS stores (
  sid		int,
  name		text,
  phone		text,
  address	text,
  primary key (sid));
CREATE TABLE IF NOT EXISTS categories (
  cat           char(3),
  name          text,
  primary key (cat));
CREATE TABLE IF NOT EXISTS products (
  pid		char(6),
  name		text,
  unit		text,
  cat		char(3),
  primary key (pid),
  foreign key (cat) references categories);
CREATE TABLE IF NOT EXISTS carries (
  sid		int,
  pid		char(6),
  qty		int,
  uprice	real,
  primary key (sid,pid),	
  foreign key (sid) references stores,
  foreign key (pid) references products);
CREATE TABLE IF NOT EXISTS customers (
  cid		text,
  name		text,
  address	text,
  pwd		text,
  primary key (cid));
CREATE TABLE IF NOT EXISTS orders (
  oid		int,
  cid		text,
  odate		date,
  address	text,
  primary key (oid),
  foreign key (cid) references customers);
CREATE TABLE IF NOT EXISTS olines (
  oid		int,
  sid		int,
  pid		char(6),
  qty		int,
  uprice	real,
  primary key (oid,sid,pid),
  foreign key (oid) references orders,
  foreign key (sid) references stores,
  foreign key (pid) references products);
CREATE TABLE IF NOT EXISTS deliveries (
  trackingNo	int,
  oid		int,
  pickUpTime	date,
  dropOffTime	date,
  primary key (trackingNo,oid),
  foreign key (oid) references orders);
