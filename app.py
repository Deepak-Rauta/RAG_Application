import time
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Streamlit UI
st.title("RAG App Demo")

# URLs to fetch
urls = [
    'https://www.victoriaonmove.com.au',
    'https://www.victoriaonmove.com.au/index.html',
    'https://www.victoriaonmove.com.au/contact.html'
]

# Load and split documents
loader = UnstructuredURLLoader(urls=urls)
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
docs = text_splitter.split_documents(data)

# Create vector store
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=google_api_key
    ),
    collection_name="rag_collection",
    persist_directory="./chroma_db"  # saves the vectorstore so you can reuse it
)

# Set up retriever and LLM
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
llm = GoogleGenerativeAI(model='gemini-1.5-pro', temperature=0, max_tokens=500)

# Chat prompt
query = st.chat_input("Ask me anything:")
if query:
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise.\n\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # Run chain
    response = rag_chain.invoke({"input": query})
    st.write(response["answer"])
