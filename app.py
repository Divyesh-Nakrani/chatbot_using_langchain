from flask import Flask,render_template
from flask_socketio import SocketIO, send, emit
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

#logging.basicConfig(filename='chat.log', level=logging.INFO)


@socketio.on('message')
def handle_message(message):
  
  
    # Process the text here
    
  from langchain import LLMChain,PromptTemplate
  from langchain.llms import OpenAI



  template=""" Give answer of one following question

  Questions:{message}
  Answer:
  """

  prompt=PromptTemplate(template=template,input_variables=['message'])

  import os
  os.environ['OPENAI_API_KEY']='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'

  opn_llm=OpenAI(model_name='text-davinci-003')

  llm_chain=LLMChain(prompt=prompt,llm=opn_llm)
  
  
  processed_text=llm_chain.run(message)
  #logging.info(f"Received message: {message}")
    # Emit the processed text back to the client
  emit('response', {'message': processed_text}, broadcast=True)
  



if __name__ == '__main__':
    socketio.run(app,debug=True,port=8080)
