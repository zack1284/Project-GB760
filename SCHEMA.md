Relational Schema Table of Database

PHRASES(id, phrase, cur_time@, num_cur_min_p, num_prior_min_p)
TIME(time_pkey, cur_time, V_cur_min, V_prior_min, total_cur_min_num_phrase, total_prior_min_num_phrase)


Explanation of each variables

phrase: phrase in the calculation of the Trendiness 
cur_time: current time of the phrase posted
num_cur_min_p: number of times phrase was seen in the current minute at current time
num_prior_min_p: number of times phrase was seen in the prior minute at current time
V_cur_min: the number of unique phrases seen in the current minute to current time
V_prior_min: the number of unique phrases seen in the prior minute to current time
total_cur_min_num_phrase: total number of phrases seen in the current minute at current time 
total_prior_min_num_phrase: total number of phrases seen in the minute prior to current time


Summary of the logic behind it:

We created two tables connected by cur_time.
