CREATE OR REPLACE FUNCTION datetoint(input_date TIMESTAMP) 
RETURNS INTEGER AS
$$
DECLARE
    year_val INTEGER;
    month_val INTEGER;
    day_val INTEGER;
    result INTEGER;
BEGIN
    -- Extracting year, month, and day from the input date
    year_val := EXTRACT(YEAR FROM input_date);
    month_val := EXTRACT(MONTH FROM input_date);
    day_val := EXTRACT(DAY FROM input_date);
    
    -- Calculating the result
    result := year_val * 365 + month_val * 30 + day_val;
    
    -- Returning the result
    RETURN result;
END;
$$
LANGUAGE plpgsql;
