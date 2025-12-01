import requests
import time
import json
from datetime import datetime
import os

# ---------------------------------------------------
# GraphQL Query Functions
# ---------------------------------------------------

# Note: replace with your own token from scholars GraphQL API
# https://help.scholars.duke.edu/sites/default/files/scholars_graphql_quickstart_guide.pdf
API_TOKEN = os.getenv("scholars_access_token")
print(API_TOKEN)

GRAPHQL_ENDPOINT = "https://graphql.scholars.duke.edu/graphiql"
HEADERS = {
    "Content-Type": "application/json",
    "scholars_access_token": f"{API_TOKEN}",
    
}

    
    # "scholars_access_token": f"{API_TOKEN}",

TOTAL_PAGES = 116 #known from graphQL query on the scholars platform

QUERY = """
query PeopleWithTheirPublications {
  people (
    pageSize: 100, startPage: 1) {
    count
     pagingInfo {
 totalPages
 pageNumber
 }
    results {
      firstName
      lastName
      email
      overview
      currentResearch {
        id
      }
      
      primaryAppointment{
        title
      }
      

      publications(
        pageSize: 1000 , startPage: 1) {
        count
        results {
          id
          publication{
            publicationDate {
              date

            }
            title
            doi
            abstract
            allAuthors {
              fullList
            }
          }
      }
    }
    }}
}
"""


def fetch_people_page(page_number: int):
    """Fetch a single page of people from the GraphQL endpoint."""
    payload = {
        "query": QUERY,
        "variables": {"pageNumber": page_number},
    }

    resp = requests.post(GRAPHQL_ENDPOINT, json=payload, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()

    if "errors" in data:
        raise RuntimeError(f"GraphQL errors on page {page_number}: {data['errors']}")

    return data["data"]["people"]


def fetch_all_people(max_pages: int = None):
    """
    Fetch all people across pages.
    If max_pages is provided, stop early (e.g., first 2 pages only).
    """
    all_people = []

    last_page = max_pages if max_pages is not None else TOTAL_PAGES

    for page in range(1, last_page + 1):
        print(f"Fetching page {page}/{last_page}...")
        people_page = fetch_people_page(page)
        all_people.extend(people_page["results"])

        time.sleep(0.1)  # avoid hammering API

    print(f"Done. Retrieved {len(all_people)} people.")
    return all_people


# ---------------------------------------------------
# Saving Functions
# ---------------------------------------------------

def generate_timestamped_filename(prefix="people"):
    """Return a filename with timestamp, e.g. people_2025-11-19_16-32-05.json"""
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{ts}.json"


def save_json(data, filename):
    """Save data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------
# Main Execution
# ---------------------------------------------------

if __name__ == "__main__":

    # Example: get first 2 pages (use None for all 116 pages)
    people = fetch_all_people(max_pages=2)
    # people = fetch_all_people()

    # Generate a timestamped output file
    filename = generate_timestamped_filename(prefix="people")

    # Save to JSON
    save_json(people, filename)

    from pprint import pprint
    pprint(f"Saved to: {filename}" if people else "No data")