-- Create
create table customer (
	customer_id int auto_increment primary key,
    firstName varchar(225) not null,
    lastName varchar(225) not null,
    emailAddress varchar(225) not null unique,
    phoneNumber varchar(225) not null
);

-- Read
select *
from customer

-- Update
insert into customer
values (customer_id, 'Rebecca', 'H', 'rh4207@nyu.edu', '9802674006');

-- Delete
delete from customer
where customer_id = " "