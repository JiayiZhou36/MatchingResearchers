import requests
import time
import json
from datetime import datetime
import os

# ---------------------------------------------------
# GraphQL Query Functions
# ---------------------------------------------------

# Note: replace with your own token from Scholars GraphQL API
# https://help.scholars.duke.edu/sites/default/files/scholars_graphql_quickstart_guide.pdf
API_TOKEN = os.getenv("SCHOLARS_API")
print(API_TOKEN)

GRAPHQL_ENDPOINT = "https://graphql.scholars.duke.edu/graphiql"
HEADERS = {
    "Content-Type": "application/json",
    # get a key from Scholars@Duke data streamer 
    "scholars_access_token": f"{API_TOKEN}",
    
}

TOTAL_PAGES = 116  # known from GraphQL query on the Scholars platform

# Note the $pageNumber variable and its use in startPage
QUERY = """
query PeopleWithTheirPublications($pageNumber: Int!) {
  people (
    pageSize: 100,
    startPage: $pageNumber
  ) {
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
      primaryAppointment {
        title
      }
      publications(pageSize: 1000, startPage: 1) {
        count
        results {
          id
          publication {
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
    }
  }
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
    If max_pages is provided, stop early (for example, first 2 pages only).

    Returns a dict with:
      - count: total number of people (from API)
      - pagingInfo: paging info from the API
      - results: list of all people across pages
    """
    all_results = []

    # Fetch first page to get metadata (count, pagingInfo)
    first_page_number = 1
    print("Fetching first page to get metadata...")
    first_page = fetch_people_page(first_page_number)

    total_count = first_page.get("count")
    paging_info = first_page.get("pagingInfo", {})
    total_pages_from_api = paging_info.get("totalPages", TOTAL_PAGES)

    # Decide how many pages to fetch
    last_page = max_pages if max_pages is not None else total_pages_from_api

    print(f"Fetching page {first_page_number}/{last_page}...")
    all_results.extend(first_page["results"])

    # Fetch remaining pages
    for page in range(first_page_number + 1, last_page + 1):
        print(f"Fetching page {page}/{last_page}...")
        people_page = fetch_people_page(page)
        all_results.extend(people_page["results"])
        time.sleep(0.1)  # avoid hammering API

    print(f"Done. Retrieved {len(all_results)} people (Expected count: {total_count}).")

    # Return structure similar to the GraphQL shape for "people"
    return {
        "count": total_count,
        "pagingInfo": paging_info,
        "results": all_results,
    }


# ---------------------------------------------------
# Saving Functions
# ---------------------------------------------------

def generate_timestamped_filename(prefix="people"):
    """Return a filename with timestamp, for example people_2025-11-19_16-32-05.json."""
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{ts}.json"


def save_json(data, filename):
    """Save data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------------------------------------------------
# Validation Functions
# ---------------------------------------------------

def validate_people_results(people_data):
    """
    Validate that the number of downloaded results matches the API metadata count.
    Raises ValueError if they do not match.
    """
    api_count = people_data.get("count")
    downloaded_count = len(people_data.get("results", []))

    if api_count != downloaded_count:
        raise ValueError(
            f"Validation failed: expected {api_count} results, "
            f"but downloaded {downloaded_count}."
        )
    
    print("✔ Validation successful: downloaded results match API count.")


def check_dupes(people_data):
    """
    Check for duplicate people entries based on email.
    Prints duplicates if found.
    """
    emails = {}
    duplicates = []

    for person in people_data.get("results", []):
        email = person.get("email")
        if email:
            if email in emails:
                duplicates.append(email)
            else:
                emails[email] = person

    if duplicates:
        print(f"⚠ Found {len(duplicates)} duplicate emails:")
        for dup in duplicates:
            print(f" - {dup}")
    else:
        print("✔ No duplicate emails found.")

# ---------------------------------------------------
# Main Execution
# ---------------------------------------------------

if __name__ == "__main__":
    
  # Set to False to run validation
    people_data = fetch_all_people(max_pages=2)
    # people_data = fetch_all_people()


    filename = generate_timestamped_filename(prefix="people")
    save_json(people_data, filename)

    from pprint import pprint
    pprint(f"Saved to: {filename}" if people_data else "No data")


    # Run validation
    validate_people_results(people_data)

    # Check for duplicates
    check_dupes(people_data)



