# A class used to interface with the Llama model provided on our servers
import transformers
import torch
import dotenv
import os

# Audrey
PROMPT_1="""You are a helpful travel assistant who answers questions about travelling. 
          If you cannot provide a direct answer, you should give a step by step guide on how a
          traveller might get their question answered.
          """

# Jimmy
PROMPT_2=""

class Llama():
    def __init__(self,system_prompt,model="meta-llama/Meta-Llama-3.1-8B-Instruct",local=os.getenv('REMOTE')) -> None:
        # Load env variables
        dotenv.load_dotenv()
        # the local variable determines if the model is being ran locally or on the schools servers
        if local:
            os.environ['TRANSFORMERS_CACHE'] = '/mnt/netstore1_home/'
        self.system_prompt=system_prompt
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.pipeline = transformers.pipeline("text-generation", model=model,model_kwargs={"torch_dtype": torch.bfloat16}, device=self.device, token=os.getenv('HF_TOKEN'),)
        self.pipeline.model.generation_config.pad_token_id = self.pipeline.tokenizer.pad_token_id
        
    def generate(self,user_prompt,messages=None,temp=.6,top_p=.9):    
            if not messages:
                messages=[
                    {"role":"system","content":self.system_prompt},
                    {"role":"user","content":user_prompt},
                ]
            else:
                messages.append({"role":"user","content":prompt})
                
            prompt = self.pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            terminators = [self.pipeline.tokenizer.eos_token_id, self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")]
            outputs = self.pipeline(prompt, max_new_tokens=10000, eos_token_id=terminators, do_sample=True, temperature=temp,
                                    top_p=top_p, pad_token_id = self.pipeline.tokenizer.eos_token_id)

            result= outputs[0]["generated_text"][len(prompt):].strip()
            return result