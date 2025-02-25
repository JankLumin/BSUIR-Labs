CREATE OR REPLACE PROCEDURE Compare_Schemas(
  p_dev_schema  IN VARCHAR2,
  p_prod_schema IN VARCHAR2
)
AS
  TYPE t_varchar_table IS TABLE OF VARCHAR2(128);
  v_affected_tables t_varchar_table := t_varchar_table();
  TYPE t_issue_map IS TABLE OF VARCHAR2(10) INDEX BY VARCHAR2(128);
  v_issue_map t_issue_map;
  TYPE t_dep_count_map IS TABLE OF NUMBER INDEX BY VARCHAR2(128);
  v_dep_count t_dep_count_map;
  TYPE t_children_map IS TABLE OF t_varchar_table INDEX BY VARCHAR2(128);
  v_children t_children_map;
  v_sorted t_varchar_table := t_varchar_table();
  v_sorted_count PLS_INTEGER := 0;
  v_count NUMBER;
  v_table_name VARCHAR2(128);
  v_cycles_found BOOLEAN := FALSE;
BEGIN
  FOR rec IN (
    SELECT dt.table_name,
           CASE
             WHEN pt.table_name IS NULL THEN 'MISSING'
             WHEN (SELECT COUNT(*) FROM (
                      SELECT column_name, data_type, data_length, nullable
                      FROM all_tab_columns
                      WHERE owner = UPPER(p_dev_schema)
                        AND table_name = dt.table_name
                      MINUS
                      SELECT column_name, data_type, data_length, nullable
                      FROM all_tab_columns
                      WHERE owner = UPPER(p_prod_schema)
                        AND table_name = dt.table_name
                   )) > 0 THEN 'DIFF'
           END AS issue
    FROM (SELECT table_name FROM all_tables WHERE owner = UPPER(p_dev_schema)) dt
    LEFT JOIN (SELECT table_name FROM all_tables WHERE owner = UPPER(p_prod_schema)) pt
      ON dt.table_name = pt.table_name
    WHERE pt.table_name IS NULL OR
          ((SELECT COUNT(*) FROM (
              SELECT column_name, data_type, data_length, nullable
              FROM all_tab_columns
              WHERE owner = UPPER(p_dev_schema)
                AND table_name = dt.table_name
              MINUS
              SELECT column_name, data_type, data_length, nullable
              FROM all_tab_columns
              WHERE owner = UPPER(p_prod_schema)
                AND table_name = dt.table_name
            )) > 0)
  ) LOOP
    v_affected_tables.EXTEND;
    v_affected_tables(v_affected_tables.COUNT) := rec.table_name;
    v_issue_map(rec.table_name) := rec.issue;
  END LOOP;

  FOR i IN 1 .. v_affected_tables.COUNT LOOP
    v_dep_count(v_affected_tables(i)) := 0;
    v_children(v_affected_tables(i)) := t_varchar_table();
  END LOOP;

  FOR i IN 1 .. v_affected_tables.COUNT LOOP
    v_table_name := v_affected_tables(i);
    SELECT COUNT(*) INTO v_count
    FROM all_tables
    WHERE owner = UPPER(p_prod_schema)
      AND table_name = v_table_name;
    DECLARE
      v_schema_for_fk VARCHAR2(30);
    BEGIN
      IF v_count > 0 THEN
        v_schema_for_fk := UPPER(p_prod_schema);
      ELSE
        v_schema_for_fk := UPPER(p_dev_schema);
      END IF;
      FOR fk_rec IN (
        SELECT a.table_name AS child, c.table_name AS parent
        FROM all_constraints a
        JOIN all_constraints c
          ON a.r_constraint_name = c.constraint_name AND a.owner = c.owner
        WHERE a.constraint_type = 'R'
          AND a.owner = v_schema_for_fk
          AND a.table_name = v_table_name
      ) LOOP
        FOR j IN 1 .. v_affected_tables.COUNT LOOP
          IF fk_rec.parent = v_affected_tables(j) THEN
            v_dep_count(v_table_name) := v_dep_count(v_table_name) + 1;
            v_children(fk_rec.parent).EXTEND;
            v_children(fk_rec.parent)(v_children(fk_rec.parent).COUNT) := v_table_name;
          END IF;
        END LOOP;
      END LOOP;
    END;
  END LOOP;

  DECLARE
    TYPE t_queue IS TABLE OF VARCHAR2(128);
    v_queue t_queue := t_queue();
    v_queue_start PLS_INTEGER := 1;
    v_queue_end PLS_INTEGER := 0;
  BEGIN
    FOR i IN 1 .. v_affected_tables.COUNT LOOP
      IF v_dep_count(v_affected_tables(i)) = 0 THEN
        v_queue_end := v_queue_end + 1;
        v_queue.EXTEND;
        v_queue(v_queue_end) := v_affected_tables(i);
      END IF;
    END LOOP;
    WHILE v_queue_start <= v_queue_end LOOP
      DECLARE
        v_current VARCHAR2(128);
      BEGIN
        v_current := v_queue(v_queue_start);
        v_queue_start := v_queue_start + 1;
        v_sorted_count := v_sorted_count + 1;
        v_sorted.EXTEND;
        v_sorted(v_sorted_count) := v_current;
        FOR i IN 1 .. v_children(v_current).COUNT LOOP
          DECLARE
            v_child VARCHAR2(128) := v_children(v_current)(i);
          BEGIN
            v_dep_count(v_child) := v_dep_count(v_child) - 1;
            IF v_dep_count(v_child) = 0 THEN
              v_queue_end := v_queue_end + 1;
              v_queue.EXTEND;
              v_queue(v_queue_end) := v_child;
            END IF;
          END;
        END LOOP;
      END;
    END LOOP;
    FOR i IN 1 .. v_affected_tables.COUNT LOOP
      IF v_dep_count(v_affected_tables(i)) > 0 THEN
        v_cycles_found := TRUE;
        EXIT;
      END IF;
    END LOOP;
    IF v_sorted_count < v_affected_tables.COUNT THEN
      FOR i IN 1 .. v_affected_tables.COUNT LOOP
        IF v_dep_count(v_affected_tables(i)) > 0 THEN
          v_sorted_count := v_sorted_count + 1;
          v_sorted.EXTEND;
          v_sorted(v_sorted_count) := v_affected_tables(i);
        END IF;
      END LOOP;
    END IF;
  END;

  DBMS_OUTPUT.PUT_LINE('Перечень таблиц (либо отсутствуют в PROD, либо отличаются по структуре),');
  DBMS_OUTPUT.PUT_LINE('отсортированные по порядку создания:');
  FOR i IN 1 .. v_sorted_count LOOP
    DBMS_OUTPUT.PUT_LINE('  ' || v_sorted(i));
  END LOOP;

  DECLARE
    TYPE t_varchar_table_all IS TABLE OF VARCHAR2(128);
    v_all_tables_prod t_varchar_table_all := t_varchar_table_all();
    TYPE t_dep_count_map_all IS TABLE OF NUMBER INDEX BY VARCHAR2(128);
    v_all_dep_count_prod t_dep_count_map_all;
    TYPE t_children_map_all IS TABLE OF t_varchar_table_all INDEX BY VARCHAR2(128);
    v_all_children_prod t_children_map_all;
    v_all_sorted_count_prod PLS_INTEGER := 0;
  BEGIN
    FOR rec IN (SELECT table_name FROM all_tables WHERE owner = UPPER(p_prod_schema)) LOOP
      v_all_tables_prod.EXTEND;
      v_all_tables_prod(v_all_tables_prod.COUNT) := rec.table_name;
      v_all_dep_count_prod(rec.table_name) := 0;
      v_all_children_prod(rec.table_name) := t_varchar_table_all();
    END LOOP;
    FOR i IN 1 .. v_all_tables_prod.COUNT LOOP
      FOR fk_rec IN (
        SELECT a.table_name AS child, c.table_name AS parent
        FROM all_constraints a
        JOIN all_constraints c
          ON a.r_constraint_name = c.constraint_name AND a.owner = c.owner
        WHERE a.constraint_type = 'R'
          AND a.owner = UPPER(p_prod_schema)
          AND a.table_name = v_all_tables_prod(i)
      ) LOOP
        FOR j IN 1 .. v_all_tables_prod.COUNT LOOP
          IF fk_rec.parent = v_all_tables_prod(j) THEN
            v_all_dep_count_prod(v_all_tables_prod(i)) := v_all_dep_count_prod(v_all_tables_prod(i)) + 1;
            v_all_children_prod(fk_rec.parent).EXTEND;
            v_all_children_prod(fk_rec.parent)(v_all_children_prod(fk_rec.parent).COUNT) := v_all_tables_prod(i);
          END IF;
        END LOOP;
      END LOOP;
    END LOOP;
    DECLARE
      TYPE t_queue_all IS TABLE OF VARCHAR2(128);
      v_queue_all t_queue_all := t_queue_all();
      v_queue_all_start PLS_INTEGER := 1;
      v_queue_all_end PLS_INTEGER := 0;
    BEGIN
      FOR i IN 1 .. v_all_tables_prod.COUNT LOOP
        IF v_all_dep_count_prod(v_all_tables_prod(i)) = 0 THEN
          v_queue_all_end := v_queue_all_end + 1;
          v_queue_all.EXTEND;
          v_queue_all(v_queue_all_end) := v_all_tables_prod(i);
        END IF;
      END LOOP;
      WHILE v_queue_all_start <= v_queue_all_end LOOP
        DECLARE
          v_current VARCHAR2(128);
        BEGIN
          v_current := v_queue_all(v_queue_all_start);
          v_queue_all_start := v_queue_all_start + 1;
          v_all_sorted_count_prod := v_all_sorted_count_prod + 1;
          FOR i IN 1 .. v_all_children_prod(v_current).COUNT LOOP
            DECLARE
              v_child VARCHAR2(128) := v_all_children_prod(v_current)(i);
            BEGIN
              v_all_dep_count_prod(v_child) := v_all_dep_count_prod(v_child) - 1;
              IF v_all_dep_count_prod(v_child) = 0 THEN
                v_queue_all_end := v_queue_all_end + 1;
                v_queue_all.EXTEND;
                v_queue_all(v_queue_all_end) := v_child;
              END IF;
            END;
          END LOOP;
        END;
      END LOOP;
      IF v_all_sorted_count_prod < v_all_tables_prod.COUNT THEN
        DBMS_OUTPUT.PUT_LINE('Циклические зависимости в PROD: есть');
      ELSE
        DBMS_OUTPUT.PUT_LINE('Циклические зависимости в PROD: нет');
      END IF;
    END;
  END;

  DECLARE
    TYPE t_varchar_table_all IS TABLE OF VARCHAR2(128);
    v_all_tables_dev t_varchar_table_all := t_varchar_table_all();
    TYPE t_dep_count_map_all IS TABLE OF NUMBER INDEX BY VARCHAR2(128);
    v_all_dep_count_dev t_dep_count_map_all;
    TYPE t_children_map_all IS TABLE OF t_varchar_table_all INDEX BY VARCHAR2(128);
    v_all_children_dev t_children_map_all;
    v_all_sorted_count_dev PLS_INTEGER := 0;
  BEGIN
    FOR rec IN (SELECT table_name FROM all_tables WHERE owner = UPPER(p_dev_schema)) LOOP
      v_all_tables_dev.EXTEND;
      v_all_tables_dev(v_all_tables_dev.COUNT) := rec.table_name;
      v_all_dep_count_dev(rec.table_name) := 0;
      v_all_children_dev(rec.table_name) := t_varchar_table_all();
    END LOOP;
    FOR i IN 1 .. v_all_tables_dev.COUNT LOOP
      FOR fk_rec IN (
        SELECT a.table_name AS child, c.table_name AS parent
        FROM all_constraints a
        JOIN all_constraints c ON a.r_constraint_name = c.constraint_name AND a.owner = c.owner
        WHERE a.constraint_type = 'R'
          AND a.owner = UPPER(p_dev_schema)
          AND a.table_name = v_all_tables_dev(i)
      ) LOOP
        FOR j IN 1 .. v_all_tables_dev.COUNT LOOP
          IF fk_rec.parent = v_all_tables_dev(j) THEN
            v_all_dep_count_dev(v_all_tables_dev(i)) := v_all_dep_count_dev(v_all_tables_dev(i)) + 1;
            v_all_children_dev(fk_rec.parent).EXTEND;
            v_all_children_dev(fk_rec.parent)(v_all_children_dev(fk_rec.parent).COUNT) := v_all_tables_dev(i);
          END IF;
        END LOOP;
      END LOOP;
    END LOOP;
    DECLARE
      TYPE t_queue_all IS TABLE OF VARCHAR2(128);
      v_queue_all t_queue_all := t_queue_all();
      v_queue_all_start PLS_INTEGER := 1;
      v_queue_all_end PLS_INTEGER := 0;
    BEGIN
      FOR i IN 1 .. v_all_tables_dev.COUNT LOOP
        IF v_all_dep_count_dev(v_all_tables_dev(i)) = 0 THEN
          v_queue_all_end := v_queue_all_end + 1;
          v_queue_all.EXTEND;
          v_queue_all(v_queue_all_end) := v_all_tables_dev(i);
        END IF;
      END LOOP;
      WHILE v_queue_all_start <= v_queue_all_end LOOP
        DECLARE
          v_current VARCHAR2(128);
        BEGIN
          v_current := v_queue_all(v_queue_all_start);
          v_queue_all_start := v_queue_all_start + 1;
          v_all_sorted_count_dev := v_all_sorted_count_dev + 1;
          FOR i IN 1 .. v_all_children_dev(v_current).COUNT LOOP
            DECLARE
              v_child VARCHAR2(128) := v_all_children_dev(v_current)(i);
            BEGIN
              v_all_dep_count_dev(v_child) := v_all_dep_count_dev(v_child) - 1;
              IF v_all_dep_count_dev(v_child) = 0 THEN
                v_queue_all_end := v_queue_all_end + 1;
                v_queue_all.EXTEND;
                v_queue_all(v_queue_all_end) := v_child;
              END IF;
            END;
          END LOOP;
        END;
      END LOOP;
      IF v_all_sorted_count_dev < v_all_tables_dev.COUNT THEN
        DBMS_OUTPUT.PUT_LINE('Циклические зависимости в DEV: есть');
      ELSE
        DBMS_OUTPUT.PUT_LINE('Циклические зависимости в DEV: нет');
      END IF;
    END;
  END;
END;

BEGIN
  Compare_Schemas('DEV', 'PROD');
END;
