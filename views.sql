-- all commented lines have to do with wean weight, sale weight, or winter weights.
-- waiting on guidance from stakeholder
--Create or replace view winws as select * from winter_weight natural join weight order by weight.animal_id;
--Create or replace view weanws as select * from wean_weight  natural join weight order by weight.animal_id;
--Create or replace view sws as select * from sale_weight natural join weight order by weight.animal_id;
-- drop view damtags cascade;

drop view dams;
Create or replace view damtags as select distinct dam as tag from goat;
Create or replace view dams as select a.* from goat as a natural join damtags as d; 
Create or replace view kids as select a.* from goat as a inner join dams as d on a.dam = d.tag order by a.dam;
Create or replace view nk as select dam, count(animal_id) as num_kids from kids group by dam;
Create or replace view damwnk as select dams.*, nk.num_kids from dams inner join nk on dams.tag = nk.dam;
Create or replace view kidwns as select kids.*, nk.num_kids as num_sibs from kids join nk on kids.dam = nk.dam;
Create or replace view damwbw as select d.*, b.alpha_value as birth_weight from damwnk as d join birth_weight as b on d.animal_id = b.animal_id order by d.dob;
Create or replace view kidwbw as select k.*, b.alpha_value as birth_weight from kidwns as k join birth_weight as b on k.animal_id = b.animal_id order by k.dob;
create view bbm as select extract(month from dob) as month ,count(*) from goat group by month order by month;
--Create or replace view damwweanw as select d.*, w.WValue from damwbw as d join weanws as w on d.animal_id = w.animal_id;
--Create or replace view kidwweanw as select k.*, w.WValue from kidwbw as k join weanws as w on b.animal_id = w.animal_id;


--Create or replace view damwsw as select d.*, s.WValue from damwweanw as d join sws as s on d.animal_id = s.animal_id;
--Create or replace view kidwsw as select k.*, s.WValue from kidwweanw as k join winws as s on b.animal_id = s.animal_id;
