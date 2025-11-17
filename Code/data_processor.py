import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import re

def extract_department(text):
    if not text:
        return None
    m = re.search(r'\b(?:in|of)\s+(.*)', text)
    if m:
        dept = m.group(1).strip()
    else:
        dept = text.strip()

    dept = re.sub(r'^(the\s+)?(Department|School|Practice)\s+of\s+', '', dept, flags=re.IGNORECASE).strip()
    dept = re.sub(r'^the\s+', '', dept, flags=re.IGNORECASE).strip()
    return dept

with open("../prelim-data-11-14.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for person in data['data']['people']['results']:
    #publication list
    pubs = person.get("publications", {})
    results = pubs.get("results", [])

    if pubs['count'] == 0:
        continue

    if not person.get("primaryAppointment", {}):
        continue 
    
    for paper in results:
    #paper information
        pub_id = paper.get("id")
        rows.append({
            "email": person.get("email"),
            "firstName": person.get("firstName"),
            "lastName": person.get("lastName"),
            "Appointment": extract_department(person.get("primaryAppointment", {}).get("title")),
            "pub_id": paper.get("id"),
            "pub_title": paper.get("publication").get("title"),
            "pub_abstract": paper.get("publication").get("abstract"),
            "authors": paper.get("publication").get("allAuthors").get("fullList"),
        })

df = pd.DataFrame(rows)

## Create embeddings for each abstract

model = SentenceTransformer("nreimers/MiniLM-L6-H384-uncased")
df['embeddings'] = df['pub_abstract'].apply(model.encode)
model.encode(df['pub_abstract'])