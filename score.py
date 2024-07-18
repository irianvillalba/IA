from monitoracao import Monitora

trace = Monitora()

trace.criaLangFuse('irian.villalba')

generations = trace.fetch_all_pages(trace_id='65c8d680-136a-48d8-81dc-16088fe00fb8')

trace.execute_eval_and_score(generations=generations)
trace.eval_hallucination(generations=generations)
 
