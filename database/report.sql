-- Provider
select concat(p.firstName, ' ', p.lastName) as 'Name', sum(case when ph.payment_status = 'COMPLETED' then ph.paid_price else 0.00 end) as 'Total Revenue',
	count(case when b.booking_date > now() then b.booking_id else null end) as 'Future Booking'
from providers p  left join booking b on b.provider_id=p.provider_id
left join payment_history ph on ph.booking_id=b.booking_id
group by p.provider_id;

-- Customer
select concat(c.firstName, ' ', c.lastName) as 'Name', count(b.booking_id) as 'Total Booking'
from booking b join customer c on b.customer_id=c.customer_id
where b.status != 'CANCELLED'
group by c.customer_id