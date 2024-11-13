import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import os


PLOTS_PATH="plots/"
EVAL_PATH=sys.argv[1]
MODEL_NAME=sys.argv[2]

if not os.path.exists(PLOTS_PATH):
    os.mkdir(PLOTS_PATH)
    
METRIC="precision@5"


with open(EVAL_PATH,'r',encoding='utf-8') as evalfile:
    eval_results=json.load(evalfile)
    val_ids=eval_results[METRIC].items()    

plt.bar([tupl[0] for tupl in val_ids],[tupl[1] for tupl in val_ids],)
plt.title(f'precision@5 for {MODEL_NAME}')
plt.xticks([])
plt.xlabel(f"Range of precisions for {len(val_ids)} queries")
plt.ylabel('precision@5')
plt.savefig(f"{PLOTS_PATH}{MODEL_NAME}_ski_plot.png")