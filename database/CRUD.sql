
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
