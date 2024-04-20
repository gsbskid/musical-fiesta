import json
from langchain_community.llms import Cohere
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts  import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
import ast

import ast
import base_utilites as bu
from langchain_cohere import CohereEmbeddings

from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage


import json
from langchain_community.llms import Cohere
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts  import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
import ast


def format_docs(docs):
    '''
    Function to format the documents

    Args :
        1) docs : list : list of documents

    Returns :
        1) str : formatted documents
    '''
    return "\n\n".join(doc.page_content for doc in docs)


def get_answer(question) :
    '''
    Function to get the answer

    Args :
        1) question : str : question to ask

    Returns :
        1) str : answer
    '''

    with open(bu.format_path(
        '''
        Assets/
            JSONs/
                data.json
        '''
    )) as fil : data = json.load(fil)
    data = ast.literal_eval(data)

    prompt = open(bu.format_path(
        '''
        Assets/
            Prompts/
                Context.txt
        '''
    )).read()

    chunks = [
        prompt.format(key , data[key])
        for key 
        in data.keys()
    ]

    cohere_api_key = open(bu.format_path(
        '''
        Assets/
            Prompts/
                api_key.txt
        '''
    )).read()

    embeddings = CohereEmbeddings(cohere_api_key = cohere_api_key)
    vectorstore = FAISS.from_texts(chunks , embedding = embeddings)
    similar_docs = vectorstore.similarity_search(question)

    context = ''
    for doc in similar_docs : context += doc.page_content
    if len(context.split()) > 4000 : st.write(f'The provided query has huge context of {len(context.split())} Tokens exceeding the 4801 Token Limit of the model, trucnating the context')
    context = ' '.join(context.split()[:4000])

    prompt = open('Assets/Prompts/Main.txt').read().format(context , question)

    llm = ChatCohere(cohere_api_key=cohere_api_key)
    message = [HumanMessage(content=prompt)]

    return llm.invoke(message).content
    

import streamlit as st 

def check_prompt(prompt) : 
    '''
    Function to check the prompt

    Args :
        1) prompt : str : prompt to check

    Returns :
        1) bool : True if prompt is valid else False
    '''

    try : 
        prompt.replace('' , '')
        return True 
    except : return False


def check_mesaage() : 
    '''
    Function to check the messages
    '''

    if 'messages' not in st.session_state : st.session_state.messages = []

check_mesaage()

for message in st.session_state.messages : 

    with st.chat_message(message['role']) : st.markdown(message['content'])

prompt = st.chat_input('Ask me anything')

if check_prompt(prompt) :

    with st.chat_message('user') : st.markdown(prompt)

    st.session_state.messages.append({
        'role' : 'user' , 
        'content' : prompt
    })

    if prompt != None or prompt != '' : 

        response = get_answer(prompt)

        with st.chat_message('assistant') : st.markdown(response)


        st.session_state.messages.append({
            'role' : 'assistant' , 
            'content' : response
        })
