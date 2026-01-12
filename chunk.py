from lxml import etree

xml_path = "CFR_Chapters/title_12_full.xml"

def create_smart_chunks(file_path):
    # We listen for DIV3 (Chapter), DIV5 (Part), and DIV8 (Section)
    context = etree.iterparse(file_path, events=('end',), tag=['DIV3', 'DIV5', 'DIV8'])
    
    current_chapter = "Unknown"
    current_part = "Unknown"
    final_chunks = []

    for event, elem in context:
        # 1. Update the 'State' (Where are we in the book?)
        if elem.tag == 'DIV3':
            current_chapter = elem.get('N', 'Unknown')
        elif elem.tag == 'DIV5':
            current_part = elem.get('N', 'Unknown')
            
        # 2. When we hit a Section (The actual law)
        elif elem.tag == 'DIV8' and elem.get('TYPE') == 'SECTION':
            section_num = elem.get('N', 'Unknown')
            
            # Extract the Head (Title of the section)
            head_elem = elem.find('HEAD')
            section_title = head_elem.text if head_elem is not None else ""
            
            # Extract all Paragraphs
            paragraphs = [p.text for p in elem.findall('.//P') if p.text]
            content_text = "\n".join(paragraphs)

            # 3. ADD CONTEXT TO THE TEXT
            # We don't just store the paragraphs; we prefix them with the metadata
            # This ensures the Vector Embedding "knows" what this text is about.
            contextualized_text = f"Chapter {current_chapter}, Part {current_part}, Section {section_num}: {section_title}\n\n{content_text}"

            # 4. Create the Dictionary for Pinecone
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
            
            # 5. Memory Cleanup (Don't skip this!)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
                
    return final_chunks

# Execute
all_chunks = create_smart_chunks(xml_path)
print(f"Success! Created {len(all_chunks)} contextualized chunks.")