# ComplyRag


This is an app to help compliance specialists in the banking industry. 

The main funcitonality is a chatbot, which is powered by gemini API. This chatbot's accuracy and tracing are bolstered by a RAG mechanism. 

The RAG mechanism works this way:

- Used electronic Code of Federal Regulations to collect all of title 12 regulations which are all the banking regulations.
- Then this was parsed in XML format.
- From there the regulations were chunked by regulation section into about 7.2k records
- Using pinecone indexing and vector embeddings I upserted these records into a pinecone vector database
- Each records text was stored alongside its chapter and part
- When a user has a query that query is also vectorized by pinecone, and the most relevant or similar records are returned
- Then these records are passed as context to the the llm.

This method was used to enhance traceability from the LLM. Oftentimes we get an answer from an LLM but don't know where they got it from. Retrieving records allows the LLM to easily cite the source it got it's information from, leading to higher traceability resulting in answers that compliance specialists can trust.


The other functionality is an api to recieve news for the banking industry and provide that news in our platform

Another feature is the interactive checklist to help compliance specialists track every step of the way. 


