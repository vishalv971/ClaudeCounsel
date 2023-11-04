from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage

prompt = ChatPromptTemplate.from_messages([
    ("human", "Tell me the maximum weight of a {topic}"),
])

model = ChatAnthropic(anthropic_api_key='')

chain = prompt | model
print(chain.invoke({"topic": "hippopotamus"}))