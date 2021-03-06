CREATE TABLE phrases (
  phrase VARCHAR(1000) NOT NULL,
  cur_time VARCHAR NOT NULL,
  cur_sec NUMERIC NOT NULL,
  len_word NUMERIC NOT NULL,
  num_now_min_p NUMERIC NOT NULL,
  num_cur_min_p NUMERIC NOT NULL,
  num_prior_min_p NUMERIC NOT NULL, 
  CONSTRAINT ID PRIMARY KEY(phrase, cur_time)
);
CREATE TABLE time(
  cur_time VARCHAR NOT NULL,
  V_cur_min NUMERIC NOT NULL,
  V_prior_min NUMERIC NOT NULL,
  total_cur_min_num_phrase NUMERIC NOT NULL,
  total_prior_min_num_phrase NUMERIC NOT NULL,
  PRIMARY KEY(cur_time)
);
