from sentence_transformers import SentenceTransformer
from collections import OrderedDict
import numpy as np
import tqdm
import json
import re
from numpy import dot
from numpy.linalg import norm


def cosine_sim(a,b):
    return dot(a, b)/(norm(a)*norm(b))

 
def remove_html_tags(text): 
    clean = re.compile('<.*?>') 
    return re.sub(clean, '', text) 

 
class Wrapper():
    def __init__(self,answers_file,model_name="all-MiniLM-L6-v2",make_embeddings=True) -> None:
        self.model_name=model_name
        self.embeddings_file=f"{model_name}.npy"
        self.answers_file=answers_file
        self.model:SentenceTransformer=SentenceTransformer(model_name)
        self.embeddings={}
        with open(self.answers_file,'r',encoding='utf-8') as answersfile:
            self.answers=json.loads(answersfile.read())
        try:
            self._pair_embeddings_with_ids(np.load(self.embeddings_file))
        except Exception as e:
            if make_embeddings:
                self._create_embeddings()
            
            
    def _pair_embeddings_with_ids(self,embeddings):
        for embedding,answer in zip(embeddings,self.answers):
            self.embeddings[answer["Id"]]=embedding
    
    def _create_embeddings(self):
        embeddings=[]
        # Iterate over answers and encode the text without html
        for answer in tqdm.tqdm(self.answers):
            embeddings.append(self.model.encode(remove_html_tags(answer["Text"])))
            
        # Write embeddings back out to file
        np.save(self.embeddings_file,embeddings)
        self._pair_embeddings_with_ids(embeddings)
            
    def search(self,query,k=100)->dict[str,float]:
        results=OrderedDict()
        encoded=self.model.encode(query)
        for id in self.embeddings:
            results[id]=cosine_sim(encoded,self.embeddings[id])
        # Super lazy stupid code but I need to get it done
        return dict(sorted(results.items(), key=lambda x: x[1],reverse=True)[:k])