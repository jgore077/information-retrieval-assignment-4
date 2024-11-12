#!/bin/bash
python3 generate_results.py data/Answers.json data/topics_1.json data/topic1_prompt1.json topic1_prompt1.tsv
python3 generate_results.py data/Answers.json data/topics_1.json data/topic1_prompt2.json topic1_prompt2.tsv
python3 generate_results.py data/Answers.json data/topics_2.json data/topic2_prompt1.json topic2_prompt1.tsv 
python3 generate_results.py data/Answers.json data/topics_2.json data/topic2_prompt2.json topic2_prompt2.tsv