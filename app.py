# Bring in deps
import os 
from apikey import apikey 
import clipboard

import streamlit as st 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

os.environ['GOOGLE_API_KEY'] = apikey
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=1)

# App framework
st.title('🦜🔗 👉 Blog GPT')
st.subheader('Generate Blog  in just 20 sec. 😎 ')
prompt = st.text_input('Enter Your Prompt') 

# Prompt templates
blog_template = PromptTemplate(
    input_variables = ['BlogTopic'], 
    template='genearate a finacial blog on {BlogTopic} for this https://smartcard.ltd/ ,without palgarism and use easy word'
)

# Memory 
blog_memory = ConversationBufferMemory(input_key='BlogTopic', memory_key='chat_history')

# Llms
blog_chain = LLMChain(llm=llm, prompt=blog_template, verbose=True, output_key='blog', memory=blog_memory)

wiki = WikipediaAPIWrapper()

# Show stuff on the screen if there's a prompt
if prompt: 
    blog = blog_chain.run(prompt)
    wiki_research = wiki.run(prompt) 

    st.write(blog) 

    # Copy button
    if st.button("Copy to Clipboard"):
        clipboard.copy(blog)
        st.success("Content copied to clipboard!")

    with st.expander('blog History'): 
        st.info(blog_memory.buffer)

    with st.expander('Wikipedia Research'): 
        st.info(wiki_research)
