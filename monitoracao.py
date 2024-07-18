from langfuse.callback import CallbackHandler
from langfuse import Langfuse
from langchain.evaluation import load_evaluator
from langchain_community.llms import Ollama # type: ignore
from langchain.evaluation.criteria import LabeledCriteriaEvalChain
import os

os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-18f27d2b-2268-4daf-a9d4-6390acd2660d"
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-ffb55d36-23a1-4b69-a076-54c060b04ff6"
os.environ["LANGFUSE_HOST"] = "http://localhost:3000"

class Monitora:
       
    EVAL_TYPES={
        "hallucination": True,
        "conciseness": True,
        "relevance": True,
        "coherence": True,
        "harmfulness": True,
        "maliciousness": True,
        "helpfulness": True,
        "controversiality": True,
        "misogyny": True,
        "criminality": True,
        "insensitivity": True
    } 

    def __init__(self):
        self.langfuse = Langfuse()
        
    def criaLangFuse(self, user):
        langfuse_handler = CallbackHandler(user_id=user)
        return langfuse_handler
    
    def fetch_all_pages(self, name=None, user_id = None, trace_id=None, limit=50):
        page = 1
        all_data = []
    
        while True:
            response = self.langfuse.get_generations(name=name, limit=limit, user_id=user_id, page=page, trace_id=trace_id)
            if not response.data:
                break
    
            all_data.extend(response.data)
            page += 1
    
        return all_data
    
    def get_evaluator_for_key(self, key: str):
        model = Ollama(model="llama3")
        return load_evaluator("criteria", criteria=key, llm=model)

    def execute_eval_and_score(self, generations):
 
        for generation in generations:
            criteria = [key for key, value in self.EVAL_TYPES.items() if value and key != "hallucination"]
        
            for criterion in criteria:
                eval_result = self.get_evaluator_for_key(criterion).evaluate_strings(
                    prediction=generation.output,
                    input=generation.input,
                )
                print(eval_result)
        
                self.langfuse.score(name=criterion, trace_id=generation.trace_id, observation_id=generation.id, value=eval_result["score"], comment=eval_result['reasoning'])
    
    def get_hallucination_eval(self):
        criteria = {
            "hallucination": (
            "Este envio contém informações"
            " não presentes na entrada ou referência?"
            ),
        }
        model = Ollama(model="llama3")
        
        return LabeledCriteriaEvalChain.from_llm(
            llm=model,
            criteria=criteria
        )  
    
    def eval_hallucination(self, generations):
 
        chain = self.get_hallucination_eval()
        
        for generation in generations:
            eval_result = chain.evaluate_strings(
            prediction=generation.output,
            input=generation.input,
            reference=generation.input
            )
            print(eval_result)
            if eval_result is not None and eval_result["score"] is not None and eval_result["reasoning"] is not None:
                self.langfuse.score(name='hallucination', trace_id=generation.trace_id, observation_id=generation.id, value=eval_result["score"], comment=eval_result['reasoning'])          