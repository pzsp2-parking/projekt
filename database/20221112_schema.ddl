DROP TABLE IF EXISTS requests CASCADE;
DROP TABLE IF EXISTS charging CASCADE;
DROP TABLE IF EXISTS chargers CASCADE;
DROP TABLE IF EXISTS cars CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS car_parks CASCADE;

CREATE TABLE accounts (
    account_no          SERIAL NOT NULL,
    name                VARCHAR(20) NOT NULL,
    password            VARCHAR(30) NOT NULL,
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

CREATE TABLE car_parks (
    car_park_id SERIAL NOT NULL,
    spaces_no   NUMERIC(3) NOT NULL,
    city        VARCHAR(20) NOT NULL,
    street      VARCHAR(20) NOT NULL,
    building_no VARCHAR(6) NOT NULL
);

ALTER TABLE car_parks ADD CONSTRAINT cpa_pk PRIMARY KEY ( car_park_id );

CREATE TABLE chargers (
    charger_id      SERIAL NOT NULL,
    maximal_power   NUMERIC(3) NOT NULL,
    charger_type    CHAR(2) NOT NULL,
    description     VARCHAR(100),
    cpa_car_park_id INTEGER NOT NULL
);

ALTER TABLE chargers 
	ADD CONSTRAINT cha_type_check CHECK ( ( charger_type = 'AC')
														OR
														( charger_type = 'DC' ) );

ALTER TABLE chargers ADD CONSTRAINT cha_pk PRIMARY KEY ( charger_id );

CREATE TABLE charging (
    datetime          TIMESTAMP NOT NULL,
	base_charge_level NUMERIC(4, 2) NOT NULL,
    charge_level      NUMERIC(4, 2) NOT NULL,
    departure_dateime TIMESTAMP NOT NULL,
    cha_charger_id    INTEGER NOT NULL,
    car_vin           VARCHAR(17) NOT NULL
);

CREATE INDEX cin_vin__idx ON
    charging (
        car_vin
    ASC );

CREATE INDEX cin_cha__idxv1 ON
    charging (
        cha_charger_id
    ASC );

ALTER TABLE charging
    ADD CONSTRAINT cin_pk PRIMARY KEY ( cha_charger_id,
                                        car_vin,
                                        datetime );


CREATE TABLE requests (
    datetime        TIMESTAMP NOT NULL,
    request         NUMERIC(4) NOT NULL,
    expenditure     NUMERIC(4),
    cpa_car_park_id INTEGER NOT NULL
);

CREATE INDEX req__idx ON
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
    ADD CONSTRAINT cin_char_fk FOREIGN KEY ( cha_charger_id )
        REFERENCES chargers ( charger_id );

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
    UPDATE OF cha_charger_id, car_vin ON charging
EXECUTE PROCEDURE msgnontransferable();

CREATE OR REPLACE TRIGGER fkntm_request BEFORE
    UPDATE OF cpa_car_park_id ON requests
EXECUTE PROCEDURE msgnontransferable();

CREATE OR REPLACE TRIGGER employee_car_update BEFORE 
	INSERT OR UPDATE OF acc_account_no on CARS
FOR EACH ROW
EXECUTE PROCEDURE car_account_changes();

CREATE OR REPLACE VIEW clients_list AS
SELECT account_no, name, password, email_address, phone_no FROM accounts WHERE account_type LIKE 'CLIENT';

CREATE OR REPLACE VIEW cars_charging AS
WITH currently_charged AS (
	SELECT DISTINCT ON (car_vin) 
	base_charge_level, charge_level, car_vin, cha_charger_id, datetime, departure_dateime
	FROM charging
	WHERE CURRENT_TIMESTAMP < departure_dateime
	ORDER BY car_vin
)
SELECT CIN.charge_level, CIN.base_charge_level, CIN.datetime, CIN.departure_dateime, CARS.capacity, CHA.Maximal_power, CHA.charger_type, CHA.charger_id, CPA.car_park_ID 
FROM (((car_parks as CPA join chargers AS CHA on CPA.car_park_id = CHA.cpa_car_park_id) JOIN currently_charged AS CIN ON CHA.charger_id = CIN.cha_charger_id) 
JOIN cars ON cars.vin = CIN.car_vin);

INSERT INTO car_parks (spaces_no, city, street, building_no)
VALUES (20, 'Warszawa', 'Glowna', '15');

INSERT INTO accounts (name, password, email_address, phone_no, account_type, cpa_car_park_id) 
VALUES ('employee', 'haslo123', 'mail@mail.com', '888666777', 'EMPLOYEE', 1);
INSERT INTO accounts (name, password, email_address, phone_no, account_type) 
VALUES ('client', 'haslo123', 'mail@mail.com', '999888777', 'CLIENT');

INSERT INTO chargers (maximal_power, charger_type, description, cpa_car_park_id)
VALUES (200, 'DC', 'Nice charger', 1);

INSERT INTO cars (vin, registration_no, model, brand, capacity, description, acc_account_no)
VALUES ('THAT15CRAZY34RCOD', 'REGI 1234', 'Karl', 'OPEL', 2000.20, 'That is some crazy description', 2);
