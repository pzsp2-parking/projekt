DROP TABLE IF EXISTS requests CASCADE;
DROP TABLE IF EXISTS charging CASCADE;
DROP TABLE IF EXISTS chargers CASCADE;
DROP TABLE IF EXISTS cars CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS car_parks CASCADE;

CREATE TABLE accounts (
    account_no          SERIAL NOT NULL,
    name                VARCHAR(20) NOT NULL,
    password            VARCHAR(64) NOT NULL,
    email_address       VARCHAR(20) NOT NULL,
    phone_no            CHAR(9) NOT NULL,
	account_type        VARCHAR(8) NOT NULL,
	cpa_car_park_id			INTEGER
);

ALTER TABLE accounts
    ADD CONSTRAINT acc_arc CHECK ( ( account_type = 'EMPLOYEE' )
										
									OR ( ( account_type = 'CLIENT')
										AND 
										( cpa_car_park_id IS NULL ) ) ) ;

ALTER TABLE accounts ADD CONSTRAINT acc_pk PRIMARY KEY ( account_no );

ALTER TABLE accounts ADD CONSTRAINT acc_name_un UNIQUE ( name );

CREATE INDEX acc_cpa__idx ON
    accounts (
        cpa_car_park_ID
    ASC );


CREATE TABLE cars (
    vin             VARCHAR(17) NOT NULL,
    registration_no VARCHAR(9) NOT NULL,
    model           VARCHAR(20) NOT NULL,
    brand           VARCHAR(20) NOT NULL,
    capacity        NUMERIC(6, 2) NOT NULL,
    description     VARCHAR(100),
    acc_account_no  INTEGER NOT NULL
);

ALTER TABLE cars ADD CONSTRAINT car_pk PRIMARY KEY ( vin );

ALTER TABLE cars ADD CONSTRAINT car_reg_no_un UNIQUE ( registration_no );

CREATE INDEX car_acc__idx ON
    cars (
        acc_account_no
    ASC );


CREATE TABLE car_parks (
    car_park_id SERIAL NOT NULL,
    spaces_no   NUMERIC(3) NOT NULL,
    city        VARCHAR(20) NOT NULL,
    street      VARCHAR(20) NOT NULL,
    building_no VARCHAR(6) NOT NULL
);

ALTER TABLE car_parks ADD CONSTRAINT cpa_pk PRIMARY KEY ( car_park_id );

CREATE TABLE chargers (
    charger_code    CHAR(8) NOT NULL,
    maximal_power   NUMERIC(3) NOT NULL,
    charger_type    CHAR(2) NOT NULL,
    description     VARCHAR(100),
    cpa_car_park_id INTEGER NOT NULL
);

ALTER TABLE chargers 
	ADD CONSTRAINT cha_type_check CHECK ( ( charger_type = 'AC')
														OR
														( charger_type = 'DC' ) );

ALTER TABLE chargers ADD CONSTRAINT cha_pk PRIMARY KEY ( charger_code );

CREATE INDEX cha_cpa__idx ON
    chargers (
        CPA_car_park_ID
    ASC );


CREATE TABLE charging (
    datetime          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	base_charge_level NUMERIC(6, 2) NOT NULL,
    charge_level      NUMERIC(6, 2) NOT NULL,
    departure_datetime TIMESTAMP NOT NULL,
    cha_charger_code  CHAR(8) NOT NULL,
    car_vin           VARCHAR(17) NOT NULL
);

CREATE INDEX cin_cha__idxv1 ON
    charging (
        cha_charger_code
    ASC );

ALTER TABLE charging
    ADD CONSTRAINT cin_pk PRIMARY KEY ( car_vin,
                                        datetime );


CREATE TABLE requests (
    datetime        TIMESTAMP NOT NULL,
    request         NUMERIC(4) NOT NULL,
    expenditure     NUMERIC(4),
    cpa_car_park_id INTEGER NOT NULL
);

CREATE INDEX req_cpa__idx ON
    requests (
        cpa_car_park_id
    ASC );

ALTER TABLE requests ADD CONSTRAINT req_pk PRIMARY KEY ( datetime,
                                                        cpa_car_park_id );

ALTER TABLE cars
    ADD CONSTRAINT car_cli_fk FOREIGN KEY ( acc_account_no )
        REFERENCES accounts ( account_no );

ALTER TABLE charging
    ADD CONSTRAINT cha_car_fk FOREIGN KEY ( car_vin )
        REFERENCES cars ( vin );

ALTER TABLE chargers
    ADD CONSTRAINT cha_cpa_fk FOREIGN KEY ( cpa_car_park_id )
        REFERENCES car_parks ( car_park_id );

ALTER TABLE charging
    ADD CONSTRAINT cin_char_fk FOREIGN KEY ( cha_charger_code )
        REFERENCES chargers ( charger_code );

ALTER TABLE accounts
    ADD CONSTRAINT acc_cpa_fk FOREIGN KEY ( cpa_car_park_id )
        REFERENCES car_parks ( car_park_id );

ALTER TABLE requests
    ADD CONSTRAINT req_cpa_fk FOREIGN KEY ( cpa_car_park_id )
        REFERENCES car_parks ( car_park_id );

CREATE OR REPLACE FUNCTION msgnontransferable() 
RETURNS trigger AS 
$$
BEGIN 
  RAISE EXCEPTION 'Cant change nontransferable value';
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION car_account_changes()
RETURNS trigger AS
$$
BEGIN
	PERFORM account_no FROM accounts WHERE account_no = NEW."acc_account_no" AND account_type = 'EMPLOYEE';
	IF FOUND THEN
		RAISE EXCEPTION 'Employee account cant have assigned cars!';
	ELSE 
		RETURN NEW;
	END IF;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER fkntm_charging BEFORE
    UPDATE OF cha_charger_code, car_vin ON charging
EXECUTE PROCEDURE msgnontransferable();

CREATE OR REPLACE TRIGGER fkntm_request BEFORE
    UPDATE OF cpa_car_park_id ON requests
EXECUTE PROCEDURE msgnontransferable();

CREATE OR REPLACE TRIGGER employee_car_update BEFORE 
	INSERT OR UPDATE OF acc_account_no on CARS
FOR EACH ROW
EXECUTE PROCEDURE car_account_changes();

CREATE OR REPLACE VIEW clients_list AS
SELECT account_no, name, password, email_address, phone_no 
FROM accounts 
WHERE account_type LIKE 'CLIENT';

CREATE OR REPLACE VIEW parked_cars AS
SELECT vin, registration_no, model, brand, capacity, description, acc_account_no 
FROM cars CAR JOIN charging CIN on CAR.vin = CIN.CAR_vin 
WHERE cin.departure_datetime > CURRENT_TIMESTAMP;

CREATE OR REPLACE VIEW cars_charging AS
WITH currently_charged AS (
	SELECT DISTINCT ON (car_vin) 
	base_charge_level, charge_level, car_vin, cha_charger_code, datetime, departure_datetime
	FROM charging
	WHERE CURRENT_TIMESTAMP < departure_datetime
	ORDER BY car_vin
)
SELECT CIN.charge_level, CIN.base_charge_level, CIN.datetime, CIN.departure_datetime, CARS.capacity, CHA.Maximal_power, CHA.charger_type, CHA.charger_code, CPA.car_park_ID, CARS.vin 
FROM (((car_parks as CPA join chargers AS CHA on CPA.car_park_id = CHA.cpa_car_park_id) JOIN currently_charged AS CIN ON CHA.charger_code = CIN.cha_charger_code) 
JOIN cars ON cars.vin = CIN.car_vin);

INSERT INTO car_parks (spaces_no, city, street, building_no) VALUES 
(15, 'Warszawa', 'Glowna', '15'),
(20, 'Gdansk', 'Posrednia', '22a'),
(10, 'Warszawa', 'Dluga', '4');

INSERT INTO accounts (name, password, email_address, phone_no, account_type) 
VALUES ('gregory', '829fa778d0063cc51b767a8e405ee17ce791131921183ec777b9bd60ac97eae1', 'gregory@gmail.com', '991888777', 'CLIENT'),    
('barian', '829fa778d0063cc51b767a8e405ee17ce791131921183ec777b9bd60ac97eae1', 'barian@gmail.com', '992888777', 'CLIENT'),
('carian', '829fa778d0063cc51b767a8e405ee17ce791131921183ec777b9bd60ac97eae1', 'carian@gmail.com', '993888777', 'CLIENT'),
('darian', '829fa778d0063cc51b767a8e405ee17ce791131921183ec777b9bd60ac97eae1', 'darian@gmail.com', '994888777', 'CLIENT'),
('marian', '829fa778d0063cc51b767a8e405ee17ce791131921183ec777b9bd60ac97eae1', 'marian@gmail.com', '995888777', 'CLIENT');

INSERT INTO accounts (name, password, email_address, phone_no, account_type, cpa_car_park_id) 
VALUES ('employee', '15a7274356a34fc22820f5a8dbfdef63843051fff087f352e56b4056f6e887f4', 'mail@mail.com', '888666777', 'EMPLOYEE', 1),
('a.bonk', '15a7274356a34fc22820f5a8dbfdef63843051fff087f352e56b4056f6e887f4', 'bonk@gmail.com', '818656777', 'EMPLOYEE', 1),
('b.donk', '15a7274356a34fc22820f5a8dbfdef63843051fff087f352e56b4056f6e887f4', 'donk@gmail.com', '828666777', 'EMPLOYEE', 1),
('c.wonk', '15a7274356a34fc22820f5a8dbfdef63843051fff087f352e56b4056f6e887f4', 'wonk@gmail.com', '838676777', 'EMPLOYEE', 2),
('d.gonk', '15a7274356a34fc22820f5a8dbfdef63843051fff087f352e56b4056f6e887f4', 'gonk@gmail.com', '848686777', 'EMPLOYEE', 2),
('e.monk', '15a7274356a34fc22820f5a8dbfdef63843051fff087f352e56b4056f6e887f4', 'monk@gmail.com', '858696777', 'EMPLOYEE', 3);

INSERT INTO chargers (charger_code, maximal_power, charger_type, description, cpa_car_park_id)
VALUES 
 ('01-00-00', 200, 'DC', 'Nice charger', 1),
 ('01-00-01', 200, 'DC', 'Nice charger', 1),
 ('01-00-02', 200, 'DC', 'Nice charger', 1),
 ('01-00-03', 200, 'DC', 'Nice charger', 1),
 ('01-00-04', 200, 'DC', 'Nice charger', 1),
 ('01-00-05', 200, 'DC', 'Nice charger', 1),
 ('01-00-06', 200, 'DC', 'Nice charger', 1),
 ('01-00-07', 200, 'DC', 'Nice charger', 1),
 ('01-00-08', 200, 'DC', 'Nice charger', 1),
 ('01-00-09', 200, 'DC', 'Nice charger', 1),
 ('01-01-00', 200, 'DC', 'Nice charger', 1),
 ('01-01-01', 200, 'DC', 'Nice charger', 1),
 ('01-01-02', 200, 'DC', 'Nice charger', 1),
 ('01-01-03', 200, 'DC', 'Nice charger', 1),
 ('01-01-04', 200, 'DC', 'Nice charger', 1),
 ('02-00-00', 150, 'AC', 'Nice charger', 2),
 ('02-00-01', 150, 'AC', 'Nice charger', 2),
 ('02-00-02', 150, 'AC', 'Nice charger', 2),
 ('02-00-03', 150, 'AC', 'Nice charger', 2),
 ('02-00-04', 150, 'AC', 'Nice charger', 2),
 ('02-00-05', 150, 'AC', 'Nice charger', 2),
 ('02-00-06', 150, 'AC', 'Nice charger', 2),
 ('02-00-07', 150, 'AC', 'Nice charger', 2),
 ('02-00-08', 150, 'AC', 'Nice charger', 2),
 ('02-00-09', 150, 'AC', 'Nice charger', 2),
 ('02-01-00', 150, 'AC', 'Nice charger', 2),
 ('02-01-01', 150, 'AC', 'Nice charger', 2),
 ('02-01-02', 150, 'AC', 'Nice charger', 2),
 ('02-01-03', 150, 'AC', 'Nice charger', 2),
 ('02-01-04', 150, 'AC', 'Nice charger', 2),
 ('02-01-05', 150, 'AC', 'Nice charger', 2),
 ('02-01-06', 150, 'AC', 'Nice charger', 2),
 ('02-01-07', 150, 'AC', 'Nice charger', 2),
 ('02-01-08', 150, 'AC', 'Nice charger', 2),
 ('02-01-09', 150, 'AC', 'Nice charger', 2),
 ('03-00-00', 250, 'DC', 'Nice charger', 3),
 ('03-00-01', 250, 'DC', 'Nice charger', 3),
 ('03-00-02', 250, 'DC', 'Nice charger', 3),
 ('03-00-03', 250, 'DC', 'Nice charger', 3),
 ('03-00-04', 250, 'DC', 'Nice charger', 3),
 ('03-01-00', 200, 'AC', 'Nice charger', 3),
 ('03-01-01', 200, 'AC', 'Nice charger', 3),
 ('03-01-02', 200, 'AC', 'Nice charger', 3),
 ('03-01-03', 200, 'AC', 'Nice charger', 3),
 ('03-01-04', 200, 'AC', 'Nice charger', 3);

INSERT INTO cars (vin, registration_no, model, brand, capacity, description, acc_account_no) VALUES
('8AGW25JT38KC66775', 'FWS2936', 'R1S', 'Rivian', 100, 'That is some crazy description', 1),
('TMBWUTC46MZ3J9161', 'RP59547', 'R1T', 'Rivian', 100, 'That is some crazy description', 2),
('8BCTTKUX8JX8L4378', 'NKE9095', 'Taycan Cross Turismo', 'Porsche', 100, 'That is some crazy description', 3),
('2TNH62B71YD1W6237', 'PL91879', 'I-Pace', 'Jaguar', 100, 'That is some crazy description', 3),
('YS4PPFMR05D2E1952', 'SZA9020', 'e-tron Sportback', 'Audi', 100, 'That is some crazy description', 4),
('WBAMPXN54ZLLL6978', 'WGR0691', 'e-tron', 'Audi', 100, 'That is some crazy description', 5),
('2DGRZV4Y52D4B5641', 'ESI8184', 'Taycan Sport Turismo', 'Porsche', 100, 'That is some crazy description', 5),
('3F1P667R76TZJ9662', 'DWR8470', 'e-tron GT', 'Audi', 100, 'That is some crazy description', 5);

INSERT INTO charging (base_charge_level, charge_level, departure_datetime, cha_charger_code, car_vin) VALUES
(500, 500, (NOW() + interval '1 month'), '01-00-00', '8AGW25JT38KC66775'), 
(500, 500, (NOW() + interval '1 month'), '01-00-01', 'TMBWUTC46MZ3J9161'), 
(500, 500, (NOW() + interval '1 month'), '01-00-08', '8BCTTKUX8JX8L4378'), 
(500, 500, (NOW() + interval '1 month'), '01-01-01', '2TNH62B71YD1W6237'), 
(500, 500, (NOW() + interval '1 month'), '01-01-03', 'YS4PPFMR05D2E1952'), 
(500, 500, (NOW() + interval '1 month'), '01-01-04', '2DGRZV4Y52D4B5641'), 
(500, 500, (NOW() + interval '1 month'), '01-00-05', '3F1P667R76TZJ9662');
