# Information Retrieval Assignment 4

## Installation
Install the deps.
```
pip install -r requirements.txt
```
### Environment
If you want to use the `Llama` class you will need to set some environment variables. To do this fill out `.env.example` with your hugging face token and change its name to `.env`.

## Scripts
Every script has a brief description, the arguments it takes, and an example of its usage.
### `generate_answers.py`
Takes a topic file then uses the `Llama` class to generate pseudo-documents. The prefix argument is used give the output file a descriptive name.
```
python generate_answers.py <topics_path>.json <prefix>
```
```
python generate_answers.py data/topics_1.json "topics1"
```
### `generate_results.py`
This script generates the result files by using the `Wrapper` class to do a bi-encoder search with the expanded querys.
```
python generate_results <answers_path>.json <topics>.json <ai_answers>.json <output>.tsv 
```

```
python3 generate_results.py data/Answers.json data/topics_1.json data/topic1_prompt1.json topic1_prompt1.tsv
```

### `evaluate_individual.py`
This script takes one qrel and any number of results files (corresponding to that qrel) and saves their individual scores into the `evals` directory.
```
python evaluate_individual.py <qrel_path>.tsv <result_file1>.tsv <result_file2>.tsv ...
```

```
python evaluate_individual.py data/qrel_1.tsv results/prompt1_1.tsv results/prompt2_1.tsv
```

### `evaluate_mean.py`
This script prints out the mean metrics of any number of results files. It works similarly to `evaluate_individual.py`
```
python evaluate_mean.py <qrel_path>.tsv <result_file1>.tsv <result_file2>.tsv ...
```

```
python evaluate_mean.py data/qrel_1.tsv results/prompt1_1.tsv results/prompt2_1.tsv
```

### `skijump.py`
This script is used to generate ski jump plots and they get saved to the `plots` directory. The model name will be displayed in the plot so make it descriptive.
```
python skijump.py <eval_path>.json <model_name>
```

```
python skijump.py evals/topic1_prompt2_eval.json "Prompt 2"
```
## Classes

### `Wrapper`
This class provides an interface to use the [Sentence Transformers](https://sbert.net/) library with our data. It takes an answer file and a model name for arguments.

```python
from SentenceTransformersWrapper import Wrapper

# uses the answers file and the all-MiniLM-L6-v2 model
st_model=Wrapper("data/Answers.json","all-MiniLM-L6-v2")

# The k parameter controls how many results are returned, the key is the doc id and value is the cosine sim
st_model.search("How do I hitchhike from Lithuania to Estonia",k=3)
```
```javascript
{
'13641': 0.597, 
'175975':0.578, 
'13462':0.570, 
}
```
### `Llama.py`
This class encapsulates Metas `Meta-Llama-3.1-8B-Instruct` model. It allows loading of multiple messages or you can do zero-shot prompting by just providing the system prompt.

```python
from Llama import Llama

model=Llama("You are a cat, you cannot answers questions but can only respond with meow")
model.generate("Are you hungry kitty?")
```

```
meow
```