CREATE TABLE A (
  A_ID NUMBER PRIMARY KEY,
  B_ID NUMBER
);

CREATE TABLE B (
  B_ID NUMBER PRIMARY KEY,
  C_ID NUMBER
);

CREATE TABLE C (
  C_ID NUMBER PRIMARY KEY,
  A_ID NUMBER
);

ALTER TABLE A
  ADD CONSTRAINT FK_A_B
  FOREIGN KEY (B_ID) REFERENCES B(B_ID)
  DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE B
  ADD CONSTRAINT FK_B_C
  FOREIGN KEY (C_ID) REFERENCES C(C_ID)
  DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE C
  ADD CONSTRAINT FK_C_A
  FOREIGN KEY (A_ID) REFERENCES A(A_ID)
  DEFERRABLE INITIALLY DEFERRED;
