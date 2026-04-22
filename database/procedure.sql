delimiter //
create procedure provided_service(in p_provider_id int)
begin
	select concat(p.firstName, ' ',p.lastName) as 'Provider Name', p.businessName as 'Bussiness Name', s.serviceName as 'Service Name', s.listedPrice as 'Price', l.state as 'State',
    avg_rating(p.provider_id) as 'Average Rating'
    from providers p join provider_has_service ps on p.provider_id=ps.provider_id
        join services s on ps.service_id=s.service_id
        join provider_has_location pl on p.provider_id=pl.provider_id
        join location l on l.location_id=pl.location_id
	where p.provider_id=p_provider_id;
end //
delimiter ;

-- Calling Procedure
call provided_service(3);

delimiter //
create procedure booking_per_customer(in c_customer_id int)
begin
	select concat(c.firstName, ' ',c.lastName) as 'Customer Name', s.serviceName as 'Service Name', b.booking_date as 'Date/Time', b.status as 'Status',
	       concat(p.firstName, ' ',p.lastName) as 'Provider Name', p.businessName as 'Business Name', avg_rating(p.provider_id) as 'Average Rating'
    from booking b join customer c on c.customer_id=b.customer_id
        join providers p on b.provider_id=p.provider_id
        join services s on b.service_id=s.service_id
	where c.customer_id=c_customer_id;
end //
delimiter ;

call booking_per_customer(7);