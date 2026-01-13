from pinecone import Pinecone

from dotenv import load_dotenv
import os
load_dotenv() # Load the .env file
import math

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") # Access the key

pc = Pinecone(api_key=PINECONE_API_KEY, environment="us-west1-gcp")
index = pc.Index("complyrag")


query = input("enter your query: ")

results = index.search(
    namespace="cfr-regulations2", 
    query={
        "inputs": {"text": query}, 
        "top_k": 2
    },
    fields=["category", "text"]
)

print(results)