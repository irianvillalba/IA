from langchain_community.llms import Ollama # type: ignore
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from monitoracao import Monitora

class Tradutor:
    model = Ollama(model="llama3", temperature=0)
    prompt = ''' traduza para {lang} o texto abaixo:
    {text}

    não adicione nota no inicio e nem no final da resposta
    '''

    chat_template = ChatPromptTemplate.from_template(prompt)
    
    def dividir_texto(self, texto, max_caracteres):
        # Divide o texto em partes menores que o limite de caracteres
        partes = []
        while len(texto) > max_caracteres:
            # Encontra o último espaço antes do limite de caracteres
            corte = texto[:max_caracteres].rfind(' ')
            if corte == -1:
                corte = max_caracteres
            partes.append(texto[:corte])
            texto = texto[corte:].strip()
        partes.append(texto)
        return partes

    def traduzir(self, lingua, texto, usuario):
        trace = Monitora().criaLangFuse(usuario)
        partes_texto = self.dividir_texto(texto, max_caracteres=3000)
        traducao_completa = []
        
        for parte in partes_texto:
            conteudo = self.chat_template.format_messages(
                lang=lingua,
                text=parte
            )
            resposta = self.model.invoke(conteudo, config={"callbacks": [trace]})
            
            # Imprimir a resposta bruta para verificar sua estrutura
            print("Resposta bruta do modelo:", resposta)
            
            # Acessar a mensagem traduzida de acordo com a estrutura da resposta
            mensagem_traduzida = resposta['choices'][0]['message']['content']
            traducao_completa.append(mensagem_traduzida)
        
        return '\n'.join(traducao_completa)
    
# Exemplo de uso
tradutor = Tradutor()
texto_longo = "Seu texto longo aqui..."
traducao = tradutor.traduzir("es", texto_longo, "usuario123")
print(traducao)