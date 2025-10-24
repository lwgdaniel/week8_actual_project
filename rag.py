
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)


##########      helper functions

def get_embedding(input, model='text-embedding-3-small'):
    response = client.embeddings.create(
        input=input,
        model=model
    )
    return [x.embedding for x in response.data]


##########      load faqs.csv

from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("faqs.csv")
pages = loader.load()

#print(type(pages))
#print('pages is a list')

#print(type(pages[0]))
#print('pages is a list of langchain documents')

docs = pages

#print(type(docs))          # <class 'list'>
#print(len(docs))           # number of chunks is 16
#print(type(docs[0]))       # <class 'langchain.schema.document.Document'>
#print(docs[0])
#print(docs[0].page_content)  # the text of the first chunk
#print(docs[0].metadata)      # metadata dictionary

###     recap == docs is a list of langchain documents 
### i have checked that docs is populated 



##########      create vector store

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

# Wrap your existing OpenAI client in LangChain embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", client=client)

# Create FAISS vector store from your documents
vector_store = FAISS.from_documents(docs, embeddings)

query = "How do I reset my password?"
results = vector_store.similarity_search(query, k=3)  # get top 3 matches

for i, doc in enumerate(results):
    print(f"Result {i+1}:")
    print(doc.page_content)
    print("-----")