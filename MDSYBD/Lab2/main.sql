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

insert into groups (id, name, c_val) values (1, 'Группа А', 25);
insert into groups (id, name, c_val) values (1, 'Группа Б', 30);

select * from groups;

--------------------------------------------------

create or replace trigger check_student_id
before insert on students
for each row
declare
    v_count number;
begin
    select count(*) into v_count
    from students
    where id = :new.id;

    if v_count > 0 then
        raise_application_error(-20001, 'Студент с таким ID уже существует');
    end if;
end check_student_id;

insert into students (id, name, group_id) values (1, 'Иванов Иван', 1);
insert into students (id, name, group_id) values (1, 'Петров Петр', 1);

select * from students;

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

insert into students (name, group_id) values ('Иванов Иван', 1);

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

insert into groups (name, c_val) values ('Группа А', 25);

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

insert into groups (name, c_val) values ('Группа А', 25);
insert into groups (name, c_val) values ('Группа А', 30);

--------------------------------------------------

create or replace trigger cascade_delete_students
before delete on groups
for each row
begin
    delete from students where group_id = :old.id;
end cascade_delete_students;

delete from groups where groups.id = 1;

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

insert into students (name, group_id) values ('Иванов Иван', 2);
update students set name = 'Иванова Ирина' where id = 8;

select * from students;

delete from students where id = 8;

select * from students_audit;

--------------------------------------------------

create or replace procedure restore_students_to_time (target_time timestamp) is
begin
    for rec in (
        select student_id, student_name, group_id
        from students_audit
        where action_type = 'INSERT' and action_time <= target_time
        order by action_time desc
    ) loop
        insert into students (id, name, group_id)
        values (rec.student_id, rec.student_name, rec.group_id);
    end loop;

    for rec in (
        select student_id, student_name, group_id, old_value, new_value, action_time
        from students_audit
        where action_type = 'UPDATE' and action_time <= target_time
        order by action_time desc
    ) loop
        update students
        set name = rec.student_name,
            group_id = rec.group_id
        where id = rec.student_id;
    end loop;

    for rec in (
        select student_id, student_name, group_id
        from students_audit
        where action_type = 'DELETE' and action_time <= target_time
        order by action_time desc
    ) loop
        delete from students where id = rec.student_id;
    end loop;
end restore_students_to_time;

begin
    restore_students_to_time(to_timestamp('2025-02-21 15:02:30', 'YYYY-MM-DD HH24:MI:SS'));
end;

insert into students (name, group_id) values ('Иванов Иван', 2);

select * from students;

create or replace procedure restore_students_to_offset (time_shift interval day to second) is
    target_time timestamp;
begin
    target_time := sysdate + time_shift;

    for rec in (
        select student_id, student_name, group_id
        from students_audit
        where action_type = 'INSERT' and action_time <= target_time
        order by action_time desc
    ) loop
        insert into students (id, name, group_id)
        values (rec.student_id, rec.student_name, rec.group_id);
    end loop;

    for rec in (
        select student_id, student_name, group_id, old_value, new_value, action_time
        from students_audit
        where action_type = 'UPDATE' and action_time <= target_time
        order by action_time desc
    ) loop
        update students
        set name = rec.student_name,
            group_id = rec.group_id
        where id = rec.student_id;
    end loop;

    for rec in (
        select student_id, student_name, group_id
        from students_audit
        where action_type = 'DELETE' and action_time <= target_time
        order by action_time desc
    ) loop
        delete from students where id = rec.student_id;
    end loop;
end restore_students_to_offset;

begin
    restore_students_to_offset(interval '-2' day);
end;

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
    UPDATE groups
      SET c_val = (SELECT COUNT(*) FROM students WHERE group_id = rec.group_id)
    WHERE id = rec.group_id;

    DBMS_OUTPUT.PUT_LINE('Updated group_id=' || rec.group_id);
  END LOOP;
END AFTER STATEMENT;

END;

--------------------------------------------------

select * from groups;
select * from students;
SELECT * FROM students_audit;

INSERT INTO groups (id, name, c_val) VALUES (1, 'Группа Б', 0);
INSERT INTO groups (name, c_val) VALUES ('Группа B', 0);
INSERT INTO groups (name, c_val) VALUES ('Группа C', 0);

delete from groups where id = 1 --- если есть студенты

INSERT INTO students (name, group_id) VALUES ('Иванов Иван', 1);

UPDATE students SET group_id = 7 WHERE id = 21;



BEGIN
    restore_students_to_offset(INTERVAL '-1'  minute );
END;

delete from students where id = 21

BEGIN
  restore_students_to_time(TO_TIMESTAMP('2025-02-21 15:46:52', 'YYYY-MM-DD HH24:MI:SS'));
END;
