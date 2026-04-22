
-- Create customer
create table if not exists customer (
	customer_id int auto_increment primary key,
    firstName varchar(225) not null,
    lastName varchar(225) not null,
    emailAddress varchar(225) not null unique,
    phoneNumber varchar(225) not null
);

-- Create Services
create table if not exists services (
	service_id int auto_increment primary key,
    serviceName varchar(225) not null,
    listedPrice decimal(10, 2) not null,
    howLong time not null
);

-- sample data
insert into services (serviceName, listedPrice, howLong) values('Braids', 120.50, '6:30:00'),
('Locks', 200.00, '4:00:00'),
('Wash-n-Go', 60.89, '2:00:00'),
('Trim', 15.00, '1:00:00');



-- Create Providers
create table if not exists providers (
	provider_id int auto_increment primary key,
    firstName varchar(225) not null,
    lastName varchar(225) not null,
    businessName varchar(225) not null,
    emailAddress varchar(225) not null unique,
    phoneNumber varchar(225) not null,
    providerStatus enum('Active','In Active') not null default 'Active'
);

-- Add Sample Data
insert into providers (firstName, lastName, businessName, emailAddress, phoneNumber, providerStatus) values
('Nichole', 'Matthews', 'Nicky Hair Salon','nichole.matthews@nickyhair.com', '704-908-2394', 'Active'),
('Lewis', 'Fanklin', 'Lewis Barber Shop', 'lewiee@gmail.com', '394-209-20398', 'Active'),
('Marie', 'King', 'Maries Braiders', 'marie.king@gmail.com', '202-192-3920', 'Active'),
('Wanda', 'Morris', 'Modern Salon', 'morris.w@hotmail.com', '409-983-2357', 'Active');



-- Add Location

create table if not exists location (
	location_id int auto_increment primary key,
    streetName varchar(255) not null,
    city varchar(255) not null,
    state char(2) not null,
    zipCode int not null
);

-- Sample Data for Location

insert into location (streetName, city, state, zipCode) values
('Jefferson Rd','Matthew','NC','28937'),
('Hilldale Way','Concord','NY','70897'),
('Meadows Ln','Shoreview','AL','43237'),
('MikeWidow Ln','Oxmoor','LS','33347');


-- Create a Provider has Location

create table if not exists provider_has_location (
	provider_id int not null,
    location_id int not null,
	foreign key (provider_id) references providers(provider_id),
    foreign key (location_id) references location(location_id),
    primary key (provider_id, location_id)
);

-- Create a Provider has Service

create table if not exists provider_has_service (
	provider_id int not null,
    service_id int not null,
	foreign key (provider_id) references providers(provider_id),
    foreign key (service_id) references services(service_id),
    primary key (provider_id, service_id)
);

-- Create a Favorite

create table if not exists favorites (
    customer_id int not null,
	provider_id int not null,
    service_id int not null,
    created_at date not null default (current_date),
    foreign key (customer_id) references customer(customer_id),
	foreign key (provider_id) references providers(provider_id),
    foreign key (service_id) references services(service_id),
    primary key (customer_id, provider_id, service_id)
);

insert into favorites (customer_id, provider_id, service_id, created_at) values (4,1,1, now()), (5,2,2,now())

-- Create Booking

create table if not exists booking (
    booking_id int not null auto_increment,
    booking_date datetime not null,
    status enum('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED'),
    customer_id int not null,
	provider_id int not null,
    service_id int not null,
    location_id int not null,
    created_at datetime not null default current_timestamp,
    updated_at datetime not null default current_timestamp on update current_timestamp,
    foreign key (customer_id) references customer(customer_id),
	foreign key (provider_id) references providers(provider_id),
    foreign key (service_id) references services(service_id),
    foreign key (location_id) references location(location_id),
    primary key (booking_id),
    constraint booking_detail unique (provider_id,booking_date)
);

insert into booking (booking_date, status,customer_id,provider_id,service_id,location_id) values ('2026-05-01 10:00:00', 'PENDING', 4, 1, 1, 1),
('2026-05-02 14:00:00', 'CONFIRMED', 5, 2, 3, 2),
('2026-05-03 11:00:00', 'CANCELLED', 7, 3, 1, 3);


-- Create Payment History

create table payment_history (
	payment_history_id int auto_increment,
    paid_price decimal(10,2),
    paid_date datetime,
    payment_status enum('PENDING','COMPLETED','FAILED','REFUNDED') default 'PENDING',
    payment_method enum('CASH','CARD') not null,
    booking_id int not null,
    foreign key(booking_id) references booking(booking_id),
    created_at datetime not null default current_timestamp,
    primary key (payment_history_id)
);

insert into payment_history (paid_price, paid_date, payment_status, payment_method, booking_id) values
    (150.00, NOW(), 'COMPLETED', 'CARD', 1),
    (175.00, NOW(), 'PENDING', 'CASH', 2),
    (80.00, NOW(), 'COMPLETED', 'CARD', 3);

-- Create Rating_Comment

create table rating_comment(
    rc_id int auto_increment,
    rating tinyint not null,
    comment text,
    created_at datetime not null default current_timestamp,
    booking_id int not null unique,
    foreign key (booking_id) references booking(booking_id),
    primary key (rc_id)
);

insert into rating_comment (rating, comment, booking_id)
values
(5, 'Amazing braids, will definitely book again!', 1),
(4, 'Great service, very professional', 2),
(3, 'Good but took longer than expected', 3);
