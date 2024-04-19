CREATE TABLE IF NOT EXISTS lms_UserProfiles ( 
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    password VARCHAR(100),
    username VARCHAR(100),
    grup VARCHAR(100),
    email VARCHAR(128),
    last_login DATE
);

-- CREATE TABLE IF NOT EXISTS lms_user(
--     user_profiles_id FOREIGN KEY lms,
    
-- )

-- ALTER TABLE lms_UserProfiles drop column user_id;

CREATE TABLE IF NOT EXISTS lms_Tasks(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    filename VARCHAR(100),
    theme VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS lms_TaskPacks(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Student_ID    int REFERENCES lms_UserProfiles (id) ON UPDATE CASCADE ON DELETE CASCADE,
    Teacher_ID    int REFERENCES lms_UserProfiles (id) ON UPDATE CASCADE,
    duetime Date
);

CREATE TABLE IF NOT EXISTS lms_Solutions(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Student_ID    int REFERENCES lms_UserProfiles (id) ON UPDATE CASCADE ON DELETE CASCADE,
    Teacher_ID    int REFERENCES lms_UserProfiles (id) ON UPDATE CASCADE ON DELETE CASCADE,
    Taskpack_id  int REFERENCES lms_TaskPacks (id) ON UPDATE CASCADE ON DELETE CASCADE,
    grade INT,
    sendtime Date,
    filename VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS lms_TaskPacks_Tasks(
    Tasks_id   int REFERENCES lms_Tasks (id) ON UPDATE CASCADE ON DELETE CASCADE,
    TaskPacks_id int REFERENCES lms_TaskPacks (id) ON UPDATE CASCADE
);

CREATE OR REPLACE FUNCTION set_sendtime() 
RETURNS TRIGGER AS $$
BEGIN
  NEW.sendtime = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_sendtime_trigger
BEFORE INSERT ON lms_Solutions
FOR EACH ROW
EXECUTE FUNCTION set_sendtime();

CREATE OR REPLACE FUNCTION update_grade_trigger()
RETURNS TRIGGER AS $$
BEGIN
IF NEW.sendtime < TaskPacks.duetime THEN
NEW.grade := 0;
END IF;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_sendtime_trigger
BEFORE INSERT OR UPDATE ON lms_Solutions
FOR EACH ROW
EXECUTE FUNCTION update_grade_trigger();