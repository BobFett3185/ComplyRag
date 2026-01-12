from lxml import etree

xml_path = "CFR_Chapters/title_12_1.xml"

def create_smart_chunks(file_path):
    #context = etree.iterparse(file_path, events=('end',), tag=['DIV3', 'DIV5', 'DIV8'])

    # we set some events and tags to look for. 
    context = etree.iterparse(xml_path, events=('start', 'end'), tag=['DIV3', 'DIV5', 'DIV8'])

    current_chapter = "Unknown"
    current_part = "Unknown"
    final_chunks = [] # where chunks are stored

    for event, elem in context:
        if event == 'start': # if event is start then we update chapter/part
            if elem.tag == 'DIV3': # chapter
                current_chapter = elem.get('N') # this gets the chapter number from the XML  'N' # works like a dictionary
            elif elem.tag == 'DIV5': # part 
                current_part = elem.get('N', 'Unknown')
                
        elif event == 'end' and elem.tag == 'DIV8' and elem.get('TYPE') == 'SECTION': # if the event is end and the tag is DIV8 and the 
            #type is section then we create a chunk for the regulation text

            section_num = elem.get('N', 'Unknown')
            
            # get the head for the title
            head_elem = elem.find('HEAD')
            section_title = head_elem.text if head_elem is not None else ""
            
            # Extract all Paragraphs
            paragraphs = [p.text for p in elem.findall('.//P') if p.text]
            content_text = "\n".join(paragraphs) 
            # content_text is the text of the regulation without any of the context


            # Join the text and context together for embedding
            # the embedding knows what this text is about.
            contextualized_text = f"Chapter {current_chapter}, Part {current_part}, Section {section_num}: {section_title}\n\n{content_text}"

            # make dictionary for the chunk
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
            final_chunks.append(chunk)
            
            # 5. Memory Cleanup
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
                
    return final_chunks

# Execute
chunky = create_smart_chunks(xml_path) # return the list of chunks in list chunky 
print(f" created {len(chunky)}  chunks.")

print(chunky[7199]) 

# so now we have all our chunks , next is to embed them using pinecone

def getChunks(): # this will be called in VectorDB file to get the chunks for embedding
    return chunky

