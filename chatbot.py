from google import genai
import os
import types

from pinecone import Pinecone

import math

from dotenv import load_dotenv # just loading up the .env file to automatically get the api key 
load_dotenv() # Load the .env file


# get the pinecone api key, index and environment

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") # Access the key

pc = Pinecone(api_key=PINECONE_API_KEY, environment="us-west1-gcp")
index = pc.Index("complyrag")





client = genai.Client() # intiialize the gemini client

#question = input("Ask a question and the chatbot will help you!: ") # get a question from the user

system_instruction = \
"You are the HELPER to a compliance specialist at a bank. " \
"You will assist them in answering questions about the regulations that they have to follow. " \
"You have access to some context of the relevant regulations given to you.You can also keep track of the conversation " \
"context and use that to answer follow up questions. Always try to use the context to help you find the correct the answer " \
"to the user's question, if you dont know the answer then say you dont know instead of making something up. If you do find " \
"the answer in the vector database, make sure to cite which regulation you found it in so that the user can easily find it " \
"themselves. Always be concise and to the point in your answers, just give the information that is relevant to answering " \
"the user's question and nothing more." \
"If the user doesnt specificially ask a question don't try and cite any regulations. For exmample if they say hi or ask " \
"you about something not compliance related you dont need to refer to the context. " \
"" \
"If a user asks a follow up question that is related to the same topic, you can use the previous conversation context to answer the question " \
"even if the context from the vector database doesnt specifically answer the follow up question. " \
"additionally you have memory and can see an array of past chats. If a user asks a non specific question that seems like a follow up, " \
"you can assume they are still talking about the last question and then you can keep in mind what the conversation is about from the memory array" \
"each memory array has a dictionary with the past question and response"




'''
prompt = f"Here are your system instructions on how to answer the question: {system_instruction}\n\n Here is theQuestion: {question}\n\now answer it:" # create the prompt for the model

response = client.models.generate_content_stream( # response from the gemini api for a simple prompt
    model="gemini-3-flash-preview",
    contents= prompt,
) # i think these are the only 2 aruments you can pass in


# stream the results
for chunk in response:
    print(chunk.text, end="")
    
'''

def getContext(query): # this function will get the relevant context from pinecone for a given question
    results = index.search(
    namespace="cfr-regulations2", 
    query={
        "inputs": {"text": query}, 
        "top_k": 2
    },
    fields=["category", "text"]
    )

    return results


if __name__ == "__main__": #prevent side effects when importing this file into the fastapi server, only run this code if this file is run directly
    while True:
        print("\n\nType exit to quit, otherwise keep talking to the compliance helper chatbot")

        question = input("\n\nAsk a compliance related question and the chatbot will help you!: \n") # get a question from the user
        if question.lower() == "exit":
            print("\n\nSee you later")
            break

        context = getContext(question) # pass the question to the function that gets top results from pinecone

        context_prompt = f"Here is some relevant context from the raw text of the regulations that might help you answer the question:{context} \n\n"

        prompt = f"Here are your system instructions on how to answer the question: {system_instruction}\n\n Here is the question: {question}\n\nNow try your best to answer it, with respect to this context pulled from the database of regulations{context_prompt}:" # create the prompt for the model

        response = client.models.generate_content_stream( # stream response from the gemini api for a simple prompt
        model="gemini-3-flash-preview",
        contents= prompt,
        ) # i think these are the only 2 aruments you can pass in


        # stream the results
        for chunk in response:
            print(chunk.text, end="")



memory = []

# create a function to call from the other file to get a response from the chatbot for a given query.
def getResponse(query): # this function will take in a query and return a response from the chatbot

    global memory 

    context = getContext(query) # get the relevant context from pinecone for the query

    context_prompt = f"Here is some relevant context from the raw text of the regulations that might help you answer the question:{context} \n\n"
    prompt = f"Here are your system instructions on how to answer the question: {system_instruction}\n\n Here is the question: {query}\n\nNow try your best to answer it, with respect to this context pulled from the database of regulations{context_prompt}: Keep in mind that you have a memory and can see the past chats in their order in this: {memory}"
    responseStream = client.models.generate_content_stream(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    response = ""
    for chunk in responseStream:
        response += chunk.text

#copied_portion = original_array[start_index:end_index].copy()

    if len(memory) > 10:
        memory = memory[-10:]

    chat = {"query": query, "response": response}
    memory.append(chat)

    

    return response