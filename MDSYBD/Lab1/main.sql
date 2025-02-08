create table MyTable (
    id number primary key,
    val number
);

--------------------------------------------------

begin
    for i in 1..10 loop
        insert into MyTable(id, val)
        values (i, trunc(DBMS_RANDOM.VALUE(1,10000)));
        end loop;
end;

select count(*) from MyTable;

truncate table MyTable;

--------------------------------------------------

create or replace function Check_Even_Odd_Values
return varchar2 as
    even_count number;
    odd_count number;
begin
    select count(*) into even_count from MyTable where mod(val, 2) = 0;
    select count(*) into odd_count from MyTable where mod (val, 2) != 0;
    if even_count > odd_count then
        return 'true';
    elsif odd_count > even_count then
        return 'false';
    else
        return 'equal';
    end if;
end;

SELECT Check_Even_Odd_Values() FROM dual;

--------------------------------------------------

create or replace function Generate_Insert_Statement(p_id number)
return varchar2 as
    v_val number;
    v_sql varchar2(4000);
begin
    select val into v_val from MyTable where id = p_id;
    v_sql := 'insert into MyTable(id, val) values (' || p_id || ', ' || v_val || ');';
    DBMS_OUTPUT.PUT_LINE(v_sql);
    return v_sql;
exception
    when NO_DATA_FOUND then
        return 'Ошибка: ID ' || p_id || ' не найден в MyTable.';
    when others then
        RETURN 'Ошибка выполнения: ' || SQLERRM;
end;

SELECT Generate_Insert_Statement(-8) FROM dual;

--------------------------------------------------

CREATE OR REPLACE PROCEDURE Insert_MyTable(
    p_id NUMBER,
    p_val NUMBER
) AS
BEGIN
    INSERT INTO MyTable (id, val) VALUES (p_id, p_val);
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Запись добавлена: ID = ' || p_id || ', VAL = ' || p_val);
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        DBMS_OUTPUT.PUT_LINE('Ошибка: запись с ID = ' || p_id || ' уже существует.');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Ошибка выполнения: ' || SQLERRM);
END Insert_MyTable;



CREATE OR REPLACE PROCEDURE Update_MyTable(
    p_id NUMBER,
    p_new_val NUMBER
) AS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM MyTable WHERE id = p_id;

    IF v_count = 0 THEN
        DBMS_OUTPUT.PUT_LINE('Ошибка: запись с ID = ' || p_id || ' не найдена.');
    ELSE
        UPDATE MyTable SET val = p_new_val WHERE id = p_id;
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('Обновлена запись: ID = ' || p_id || ', новый VAL = ' || p_new_val);
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Ошибка выполнения: ' || SQLERRM);
END Update_MyTable;



CREATE OR REPLACE PROCEDURE Delete_MyTable(
    p_id NUMBER
) AS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM MyTable WHERE id = p_id;

    IF v_count = 0 THEN
        DBMS_OUTPUT.PUT_LINE('Ошибка: запись с ID = ' || p_id || ' не найдена.');
    ELSE
        DELETE FROM MyTable WHERE id = p_id;
        COMMIT;
        DBMS_OUTPUT.PUT_LINE('Удалена запись: ID = ' || p_id);
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Ошибка выполнения: ' || SQLERRM);
END Delete_MyTable;

call Insert_MyTable(1,123);

call Update_MyTable(1, 321);

call Delete_MyTable(1);

--------------------------------------------------

create or replace function Calculate_Annual_Compensation(
    p_salary number,
    p_bonus_percent number
) return number as
    v_bonus_ratio number;
    v_total_compensation number;
begin
    IF p_salary <= 0 THEN
        DBMS_OUTPUT.PUT_LINE('Ошибка: месячная зарплата должна быть положительной.');
        RETURN NULL;
    ELSIF p_bonus_percent < 0 THEN
        DBMS_OUTPUT.PUT_LINE('Ошибка: процент премии не может быть отрицательным.');
        RETURN NULL;
    END IF;

    v_bonus_ratio := p_bonus_percent / 100;
    v_total_compensation := (1 + v_bonus_ratio) * 12 * p_salary;
    return v_total_compensation;
exception
    when others then
    return null;
end;

SELECT Calculate_Annual_Compensation(100, 10) FROM dual;
