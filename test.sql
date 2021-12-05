CREATE TABLE phrases (
  phrase VARCHAR(1000) NOT NULL,
  str_time VARCHAR(100) NOT NULL,
  CONSTRAINT ID PRIMARY KEY(phrase, str_time)
);
