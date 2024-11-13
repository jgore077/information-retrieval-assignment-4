from ranx import Qrels,Run,evaluate
import json_fix
import json
import sys
import os
import numpy
json.fallback_table[numpy.ndarray] = lambda array: array.tolist()

METRICS=['precision@1','precision@5','ndcg@5','mrr','map']
EVAL_DIR="evals/"

def sort_dict(dictionary):
    for key in dictionary.keys():
        print(dictionary[key])
        dictionary[key]=dict(sorted(dictionary[key].items(), key=lambda x: x[1],reverse=True))
    return dictionary

if not os.path.exists(EVAL_DIR):
    os.mkdir(EVAL_DIR)
    
qrel_path=sys.argv[1]
qrel=Qrels.from_file(qrel_path,kind="trec")

for results_path in sys.argv[2:]:
    directory, filename = os.path.split(results_path)
    save_path=EVAL_DIR+filename.split('.')[0]+"_eval"+".json"
    print(f"Saving individual query results for {results_path}\n")
    run=Run.from_file(results_path,kind="trec")
    results=evaluate(qrel,run,METRICS,return_mean=False,save_results_in_run=True)
    with open(save_path,'w',encoding='utf-8') as save_file:
        save_file.write(json.dumps(sort_dict(dict(run.scores)),indent=4))
