import json

def check_unique_publications_from_file(data):
    """
    Count total unique publications, loading from a JSON file.
    """
    pub_ids = set()

    for person in data.get("results", []):
        publications = person.get("publications", {})
        results = publications.get("results", [])
        for item in results:
            pub_id = item.get("id")
            if pub_id:
                pub_ids.add(pub_id)

    total_unique = len(pub_ids)
    print(f"✔ Found {total_unique} unique publications.")

    return total_unique


def check_unique_authors_from_file(data, expected_min=None, expected_max=None):
    """
    Count total unique authors across all publications in the saved file.
    """

    unique_authors = set()

    for person in data.get("results", []):
        unique_authors.add(
            (person.get("firstName"), person.get("lastName"), person.get("email"))
        )

    total_unique = len(unique_authors)
    print(f"✔ Found {total_unique} unique authors.")

    return total_unique

if __name__ == "__main__":
    print('Running tests to check for unique publications and authors...')
    data_file_path = "people_2025-11-25_13-57-52.json"  

    with open(data_file_path, "r", encoding="utf-8") as f:
        data_file = json.load(f)

    check_unique_publications_from_file(data_file) 

    check_unique_authors_from_file(data_file)