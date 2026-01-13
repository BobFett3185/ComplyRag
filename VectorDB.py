from pinecone import Pinecone

from dotenv import load_dotenv
import os
load_dotenv() # Load the .env file
import math

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") # Access the key

pc = Pinecone(api_key=PINECONE_API_KEY, environment="us-west1-gcp")
index = pc.Index("complyrag")

from chunk import getChunks # this is the function we created in chunk.py to get the chunks for embedding
chunks = getChunks() # this will return the list of chunks we created in chunk.py


# split if the text is too big 
processed_records = []

for chunk in chunks:
    text = chunk["text"]
    if len(text) <= 35000: # we add it as it
        processed_records.append({
            "_id": chunk["id"],
            "text": text,
            **chunk["metadata"]
        })
    else: # if too big we split it up
        num_parts = math.ceil(len(text) / 35000)
        for i in range(num_parts):
            start = i * 35000
            end = start + 35000
            processed_records.append({
                "_id": f"{chunk['id']}_part{i+1}", # Unique ID for each part
                "text": text[start:end],
                **chunk["metadata"],
                "split_part": i + 1 # Metadata flag to know it's a split section
            })



'''
index.upsert_records(
    "example-namespace",
    [
        {
            "_id": "rec1",
            "text": "Apples are a great source of dietary fiber, which supports digestion and helps maintain a healthy gut.",
            "category": "digestive system", 
        },
        {
            "_id": "rec2",
            "text": "Apples originated in Central Asia and have been cultivated for thousands of years, with over 7,500 varieties available today.",
            "category": "cultivation",
        },
        {
            "_id": "rec3",
            "text": "Rich in vitamin C and other antioxidants, apples contribute to immune health and may reduce the risk of chronic diseases.",
            "category": "immune system",
        },
        {
            "_id": "rec4",
            "text": "The high fiber content in apples can also help regulate blood sugar levels, making them a favorable snack for people with diabetes.",
            "category": "endocrine system",
        },
    ])
    '''

# the upsert works 
# now we upsert our chunks from the cfr data 
'''
index.upsert_records(
    "cfr-regulations",
    [
        {
            "_id": chunk["id"],
            "text": chunk["text"],
            "metadata": chunk["metadata"]
        }
        for chunk in chunks
    ]
)




chunk = {
             "id": f"T12-C{current_chapter}-P{current_part}-S{section_num}",
                "text": contextualized_text,
                "metadata": {
                    "chapter": current_chapter,
                    "part": current_part,
                    "section": section_num,
                    "title": section_title
                }
            }
            

records_to_upsert = []
for chunk in chunks:
    records_to_upsert.append({
        "_id": chunk["id"],
        "text": chunk["text"],
        **chunk["metadata"]  # This moves 'chapter', 'part', etc. into the root of the dict
    })
'''



# start batching and upserting
batch_size = 30

print(f"Starting upsert of {len(processed_records)} records...")        


import time
for i in range(0, len(processed_records), batch_size):
    batch = processed_records[i : i + batch_size]
    
    for attempt in range(3): # try 3 times
        try:
            index.upsert_records(namespace="cfr-regulations2", records=batch)
            print(f"Success: Batch {i // batch_size + 1}")
            
            time.sleep(3)  # wait to not get rate limits
            break 
        except Exception as e: # take in any erroe message and do a cooldown
            if "429" in str(e):
                print("Rate limit hit. Cooling down for 20 seconds...")
                time.sleep(20)
            else:
                print(f"Error at index {i}: {e}")
                break

# everything is added to pincone

