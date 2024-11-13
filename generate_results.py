from SentenceTransformersWrapper import Wrapper
from ranx import Run
from tqdm.contrib import tzip
import json
import sys
import os

RESULTS_DIR="results/"

if not os.path.exists(RESULTS_DIR):
    os.mkdir(RESULTS_DIR)
    
answers_file=sys.argv[1]
original_topics=sys.argv[2]
llm_topics=sys.argv[3]
output_file=RESULTS_DIR+sys.argv[4]


st=Wrapper(answers_file)


with open(original_topics,encoding="utf-8") as og_topics_file:
    og_topics_dict=json.load(og_topics_file)

with open(llm_topics,encoding="utf-8") as generated_topics_file:
    generated_topics_dict=json.load(generated_topics_file)

results_dict={}
# For every topic we append the original title with Llama generated answer
for original,generated in tzip(og_topics_dict,generated_topics_dict.keys()):
    assert original["Id"]==generated
    query=original["Title"]+"\n"+generated_topics_dict[generated]
    # generated is the query id in this case
    results_dict[generated]=st.search(query)
    
tmp_out_path=output_file+".trec"

Run(results_dict,name=llm_topics.split("_")[1].split(".")[0]).save(tmp_out_path)

os.rename(tmp_out_path,output_file)