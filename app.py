import streamlit as st
import os
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.chains import RetrievalQA 
from streamlit_extras.add_vertical_space import add_vertical_space
st.title("Document Based Chatbot")

directory = './research_papers'
def load_docs(directory):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents

def split_docs(documents, chunk_size=1000, chunk_overlap = 20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs
documents = load_docs(directory)
docs = split_docs(documents)

embeddings = SentenceTransformerEmbeddings(model_name = "all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)
retriever = db.as_retriever()

load_dotenv()

groq_api_key=os.getenv('GROQ_API_KEY')
#st.title("Chatgroq With Llama3 Demo")

llm=ChatGroq(groq_api_key=groq_api_key,
             model_name="Llama3-8b-8192")

qa_chain = RetrievalQA.from_chain_type(llm = llm, retriever = retriever)

query = st.text_input("Enter your questions from the document")
with st.sidebar:
    st.write("Welcome to our document-based chatbot app! Leveraging Groq API with LLaMA 3 and FAISS for vector stores, our chatbot excels in quickly retrieving and understanding information from your documents. Enjoy intelligent, context-aware responses tailored to your needs, all powered by state-of-the-art AI technology.")
if "call_me" not in st.session_state:
    st.session_state.call_me = False

# Use the qa_chain to get an answer
response = qa_chain({"query": query})
button = st.button("Submit")
st.write("****For contact, type the text 'call me' and enter the submit button!****")
# Print the response
#print(response)
query = response['query']
reply = response['result']
if button:
    if query.lower() == 'call me':
        st.session_state.call_me = True
    else:
        st.write(f'User: {query}')
        st.write(f'Chatbot: {reply}')


# Sidebar with a form
if st.session_state.call_me:
    with st.sidebar:
        add_vertical_space(2)
        st.header("Sidebar Form")
        name = st.text_input("Enter your name")
        email = st.text_input("Enter your email")
        address = st.text_input("Enter your address")
        submit_button = st.button("Submit Form")

        # Process form data
        if submit_button:
            st.write("Your response has been recorded. Thank you!")
else:
    with st.sidebar:
        add_vertical_space(5)
        st.write("****Contact Form will be displayed here!.****")
