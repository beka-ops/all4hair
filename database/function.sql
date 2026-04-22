delimiter //
create function avg_rating(p_provider_id int)
returns decimal(10,1)
not deterministic
begin
    declare result decimal(10,1);
    select avg(rating) into result from rating_comment rc
        join booking b on rc.booking_id=b.booking_id
        join providers p on b.provider_id=p.provider_id
        where p.provider_id=p_provider_id;
    return result;
end //
delimiter ;