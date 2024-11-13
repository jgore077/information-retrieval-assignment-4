from ranx import Qrels,Run,evaluate
import sys


METRICS=['precision@1','precision@5','ndcg@5','mrr','map']
EVAL_DIR="evals/"
qrel_path=sys.argv[1]
qrel=Qrels.from_file(qrel_path,kind="trec")

for results_path in sys.argv[2:]:
    print(f"Evaluating results for {results_path}\n")
    run=Run.from_file(results_path,kind="trec")
    print(evaluate(qrel,run,METRICS))

