-- Trigger Payment History Add

delimiter //

create trigger create_payment_history
	after insert on booking for each row
	begin
		declare price decimal(10,2);
        select listedPrice into price
        from services
        where service_id=new.service_id;

		insert into payment_history (payment_status, payment_method, paid_price, booking_id)
        values ('PENDING', 'CARD', price, new.booking_id);
	end //

delimiter ;