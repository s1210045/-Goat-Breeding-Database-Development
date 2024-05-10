create or replace view yob as select animal_id, extract(year from dob) as year, extract(month from dob) as month  from goat;
create or replace view ww2 as select y.animal_id, w.alpha_value from yob as y join weight as w on (y.animal_id=w.animal_id) and (extract(year from w.when_measured)=y.year) and ((extract(month from w.when_measured) > y.month+2) and (extract(month from w.when_measured)<y.month+5)) and y.month<8;
create or replace view ww as select animal_id, min(alpha_value) as alpha_value from ww2 group by animal_id;
