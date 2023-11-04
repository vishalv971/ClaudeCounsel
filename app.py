from flask import Flask, request, render_template
from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage


app = Flask(__name__, template_folder="templates")

@app.route("/")
def hello_world():
    return render_template('index.html')


# prompt = ChatPromptTemplate.from_messages([
#     ("human", "Tell me the maximum weight of a {topic}"),
# ])

# model = ChatAnthropic(anthropic_api_key='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')

# chain = prompt | model
# print(chain.invoke({"topic": "hippopotamus"}))


app.run(debug=True)