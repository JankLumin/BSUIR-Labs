create table groups
(
    id    number primary key,
    name  varchar2(255) not null,
    c_val number,
    constraint check_c_val check ( c_val >= 0 )
)

--------------------------------------------------

create table students
(
    id number primary key,
    name varchar2(255) not null,
    group_id number,
    constraint fk_group foreign key (group_id) references groups (id)
)

--------------------------------------------------

create or replace trigger check_group_id
before insert on groups
for each row
declare
    v_count number;
begin
    select count(*) into v_count
    from groups
    where id = :new.id;

    if v_count > 0 then
        raise_application_error(-20002, 'Группа с таким ID уже существует');
    end if;
end check_group_id;

--------------------------------------------------

CREATE OR REPLACE TRIGGER check_student_id_compound
FOR INSERT ON students
COMPOUND TRIGGER
  TYPE t_id_tab IS TABLE OF students.id%TYPE INDEX BY PLS_INTEGER;
  new_ids t_id_tab;
  cnt PLS_INTEGER := 0;

  BEFORE EACH ROW IS
  BEGIN
    cnt := cnt + 1;
    new_ids(cnt) := :NEW.id;
  END BEFORE EACH ROW;

  AFTER STATEMENT IS
  BEGIN
    FOR i IN 1..cnt LOOP
      DECLARE
        v_count NUMBER;
      BEGIN
        SELECT COUNT(*) INTO v_count
        FROM students
        WHERE id = new_ids(i);

        IF v_count > 1 THEN
          RAISE_APPLICATION_ERROR(-20001, 'Студент с таким ID уже существует');
        END IF;
      END;
    END LOOP;
  END AFTER STATEMENT;
END;

--------------------------------------------------

create sequence seq_student_id
start with 1
increment by 1
nocache;

create or replace trigger auto_increment_student_id
before insert on students
for each row
declare
    v_count number;
begin
    if :new.id is null then
        loop
            select seq_student_id.nextval into :new.id from dual;
            select count(*) into v_count
            from students
            where id = :new.id;
            exit when v_count = 0;
        end loop;
    end if;
end auto_increment_student_id;

--------------------------------------------------

create sequence seq_group_id
start with 1
increment by 1
nocache;

create or replace trigger auto_increment_group_id
before insert on groups
for each row
declare
    v_count number;
begin
    if :new.id is null then
        loop
            select seq_group_id.nextval into :new.id from dual;
            select count(*) into v_count
            from groups
            where id = :new.id;
            exit when v_count = 0;
        end loop;
    end if;
end auto_increment_group_id;

--------------------------------------------------

create or replace trigger check_group_name
before insert on groups
for each row
declare
    v_count number;
begin
    select count(*) into v_count
    from groups
    where name = :new.name;

    if v_count > 0 then
        raise_application_error(-20003, 'Группа с таким названием уже существует');
    end if;
end check_group_name;

--------------------------------------------------

create or replace trigger cascade_delete_students
before delete on groups
for each row
begin
    delete from students where group_id = :old.id;
end cascade_delete_students;

--------------------------------------------------

create table students_audit
(
    audit_id number primary key,
    action_type varchar2(10),
    action_time timestamp,
    user_name varchar2(255),
    student_id number,
    student_name varchar2(255),
    group_id number,
    old_value varchar2(255),
    new_value varchar2(255)
);

create sequence students_audit_seq
start with 1
increment by 1
nocache;

create or replace trigger audit_insert_students
after insert on students
for each row
begin
    insert into students_audit (audit_id, action_type, action_time, user_name, student_id, student_name, group_id, new_value)
    values (students_audit_seq.nextval, 'INSERT', sysdate, user, :new.id, :new.name, :new.group_id, 'New student added');
end audit_insert_students;

create or replace trigger audit_update_students
after update on students
for each row
begin
    insert into students_audit (audit_id, action_type, action_time, user_name, student_id, student_name, group_id, old_value, new_value)
    values (students_audit_seq.nextval, 'UPDATE', sysdate, user, :new.id, :new.name, :new.group_id, :old.name, :new.name);
end audit_update_students;

create or replace trigger audit_delete_students
after delete on students
for each row
begin
    insert into students_audit (audit_id, action_type, action_time, user_name, student_id, student_name, group_id, old_value)
    values (students_audit_seq.nextval, 'DELETE', sysdate, user, :old.id, :old.name, :old.group_id, 'Student deleted');
end audit_delete_students;

--------------------------------------------------

CREATE OR REPLACE PROCEDURE restore_students_to_time(target_time TIMESTAMP) IS
BEGIN
  DELETE FROM students;
  INSERT INTO students (id, name, group_id)
  SELECT student_id, student_name, group_id
  FROM (
    SELECT
      student_id,
      student_name,
      group_id,
      action_type,
      ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY action_time DESC) AS rn
    FROM students_audit
    WHERE action_time < target_time
  )
  WHERE rn = 1
    AND action_type <> 'DELETE';

  COMMIT;
END restore_students_to_time;


CREATE OR REPLACE PROCEDURE restore_students_to_offset(time_shift INTERVAL DAY TO SECOND) IS
  target_time TIMESTAMP;
BEGIN
  target_time := SYSTIMESTAMP + time_shift;
  DELETE FROM students;
  INSERT INTO students (id, name, group_id)
  SELECT student_id, student_name, group_id
  FROM (
    SELECT
      student_id,
      student_name,
      group_id,
      action_type,
      ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY action_time DESC) AS rn
    FROM students_audit
    WHERE action_time <= target_time
  )
  WHERE rn = 1
    AND action_type <> 'DELETE';

  COMMIT;
END restore_students_to_offset;

--------------------------------------------------

create or replace type num_table as table of number;

create or replace trigger update_group_student_count_compound
for insert or update or delete on students
compound trigger

  affected_groups num_table := num_table();

after each row is
begin
  IF INSERTING THEN
    IF :NEW.group_id IS NOT NULL THEN
      affected_groups.EXTEND;
      affected_groups(affected_groups.COUNT) := :NEW.group_id;
    END IF;

  ELSIF DELETING THEN
    IF :OLD.group_id IS NOT NULL THEN
      affected_groups.EXTEND;
      affected_groups(affected_groups.COUNT) := :OLD.group_id;
    END IF;

  ELSIF UPDATING THEN
    IF :OLD.group_id IS NOT NULL THEN
      affected_groups.EXTEND;
      affected_groups(affected_groups.COUNT) := :OLD.group_id;
    END IF;
    IF :NEW.group_id IS NOT NULL THEN
      affected_groups.EXTEND;
      affected_groups(affected_groups.COUNT) := :NEW.group_id;
    END IF;
  END IF;
END AFTER EACH ROW;

AFTER STATEMENT IS
BEGIN
  FOR rec IN (
    SELECT DISTINCT column_value AS group_id
    FROM TABLE(affected_groups)
  ) LOOP
    DECLARE
      v_exist NUMBER;
    BEGIN
      SELECT COUNT(*) INTO v_exist
      FROM groups
      WHERE id = rec.group_id;

      IF v_exist > 0 THEN
        UPDATE groups
          SET c_val = (SELECT COUNT(*) FROM students WHERE group_id = rec.group_id)
        WHERE id = rec.group_id;

        DBMS_OUTPUT.PUT_LINE('Updated group_id=' || rec.group_id);
      END IF;
    EXCEPTION
      WHEN OTHERS THEN
        NULL;
    END;
  END LOOP;
END AFTER STATEMENT;
END;

--------------------------------------------------

select * from groups;
select * from students;
SELECT * FROM students_audit;

INSERT INTO groups (id, name, c_val) VALUES (1, 'Группа А', 0);
INSERT INTO groups (id, name, c_val) VALUES (2,'Группа Б', 0);
INSERT INTO groups (id, name, c_val) VALUES (3,'Группа В', 0);

delete from groups where id = 1;

INSERT INTO students (name, group_id) VALUES ('Иванов Иван', 1);

UPDATE students SET group_id = 12 WHERE id = 40;


BEGIN
    restore_students_to_offset(INTERVAL '-10'  minute );
END;

delete from students where id = 21;

BEGIN
  restore_students_to_time(TO_TIMESTAMP('2025-02-21 10:20:29', 'YYYY-MM-DD HH24:MI:SS'));
END;
