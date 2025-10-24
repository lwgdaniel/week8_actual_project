
########## note from Daniel: when we import this module into the main script, everything runs from top to bottom

from openai import OpenAI
from dotenv import load_dotenv
import os
import openai
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

##########      load faqs.csv

from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("faqs.csv")
pages = loader.load()

docs = pages
print(docs[0])  #tested ok
print(len(docs))    #tested ok

##########      test connection to open AI - tested ok

def get_completion_by_messages(messages, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1
    )
    return response.choices[0].message.content

### tested ok
#test_message = [{"role": "user", "content": "what is a pikachu"}]
#test_response = get_completion_by_messages(test_message)
#print(test_response)


##########      create vector store



embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')

vector_store= Chroma.from_documents(
    collection_name="faqs_on_gstv",
    documents=docs,
    embedding=embeddings_model,
    )

print(type(vector_store))
