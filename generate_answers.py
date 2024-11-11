from Llama import Llama,PROMPT_1,PROMPT_2
from SentenceTransformersWrapper import Wrapper
from tqdm import tqdm
import json
import sys

KEY="Title"
topics_path=sys.argv[1]

st=Wrapper("./data/Answers.json",make_embeddings=False)
llm=Llama(PROMPT_2)

with open(topics_path,'r',encoding='utf-8') as topics_file:
    topics_dict=json.load(topics_file)
    
for topic in topics_dict:
    text=topic[KEY]
    print(llm.generate(text))