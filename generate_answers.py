from Llama import Llama,PROMPT_1,PROMPT_2
from SentenceTransformersWrapper import Wrapper
from tqdm import tqdm
import json
import sys

KEY="Title"
ID="Id"
DATA_DIR="data/"
topics_path=sys.argv[1]
prefix=sys.argv[2]

prompt_1_dict={}
prompt_2_dict={}
llm=Llama(PROMPT_1)

with open(topics_path,'r',encoding='utf-8') as topics_file:
    topics_dict=json.load(topics_file)
    
# Assign generated text to new dictionary
for topic in tqdm(topics_dict,desc="Generating answers for PROMPT_1"):
    text=topic[KEY]
    answer=llm.generate(text)
    print(answer)
    prompt_1_dict[topic[ID]]=answer

# Write file to data directory
with open(f'{DATA_DIR}{prefix}_prompt1.json','w') as prompt_1_file:
    prompt_1_file.write(json.dumps(prompt_1_dict,indent=4))

# For prompt 2   
llm=Llama(PROMPT_2)

for topic in tqdm(topics_dict,desc="Generating answers for PROMPT_2"):
    text=topic[KEY]
    answer=llm.generate(text)
    print(answer)
    prompt_2_dict[topic[ID]]=answer
    
with open(f'{DATA_DIR}{prefix}_prompt2.json','w') as prompt_2_file:
    prompt_2_file.write(json.dumps(prompt_2_dict,indent=4))
    