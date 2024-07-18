from flask import Flask, request, jsonify
from monitoracao import Monitora
from flask_cors import CORS
from tradutor import Tradutor

app = Flask(__name__)
CORS(app)

def validacao(id):
    score = Monitora()
    generations = score.fetch_all_pages(trace_id=id)
    score.execute_eval_and_score(generations=generations)
    score.eval_hallucination(generations=generations)
    
@app.route('/traducao', methods=['POST'])
def add_task():
    tradutor = Tradutor()

    lingua = request.json['lingua']
    texto = request.json['texto']
    resposta = tradutor.traduzir(lingua=lingua,texto=texto,usuario='irian')
    #validacao(trace.get_trace_id())
    return resposta, 201

if __name__ == '__main__':
    app.run(debug=True)