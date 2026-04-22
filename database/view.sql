create view provider_service_listing as
    select l.location_id, p.provider_id, s.service_id, concat(firstName," ",lastName) as 'Name', businessName as 'Business', serviceName as 'Service', listedPrice as 'Price', howLong as 'Time', city as 'City', state as 'State'
        from providers p join provider_has_service ps on p.provider_id=ps.provider_id
        join services s on ps.service_id=s.service_id
        join provider_has_location pl on p.provider_id=pl.provider_id
        join location l on l.location_id=pl.location_id;

create view booked_appointments as
	select b.booking_id, concat(p.firstName," ",p.lastName) as 'Provider Name', concat(c.firstName," ",c.lastName) as 'Customer Name', c.emailAddress as 'Customer Email', booking_date as 'Booking Date',
		status as 'Status', s.serviceName as 'Service Name', concat(l.streetName, ' ', l.city, ' ' ,l.state, ' ', zipCode) as 'Location'
	from booking b join customer c on b.customer_id=c.customer_id
	join providers p on b.provider_id=p.provider_id
	join services s on b.service_id=s.service_id
	join location l on b.location_id=l.location_id;