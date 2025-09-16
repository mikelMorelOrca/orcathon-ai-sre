#!/usr/bin/env python3
"""
Test the exact search terms the agent would use for VM scanning whitelist.
"""

import dotenv
import os
from confluence_tools import init_confluence_client, search_confluence_content

dotenv.load_dotenv()

def test_vm_search_terms():
    """Test the exact search terms that should find the Skip by Tag page"""

    # Initialize client
    init_confluence_client(
        os.getenv("CONFLUENCE_BASE_URL"),
        os.getenv("CONFLUENCE_TOKEN"),
        os.getenv("CONFLUENCE_EMAIL")
    )

    # Test the search terms the agent would likely use based on the request:
    # "Customer would like to have the whitelist for scanning VMs"
    search_terms = [
        "VM scanning whitelist tags",
        "scanning whitelist",
        "VM whitelist",
        "skip by tag",
        "tag functionality",
        "VM scanning tags",
        "whitelist scanning VMs",
        "scan configuration VM",
        "VM tag based scanning"
    ]

    expected_page_id = "3278536757"
    expected_title = "SRE Operations: Skip by Tag Functionality"

    print(f"Looking for page: {expected_title}")
    print(f"Expected ID: {expected_page_id}")
    print(f"Expected URL: https://orcasecurity.atlassian.net/wiki/spaces/OPR/pages/{expected_page_id}/SRE+Operations+Skip+by+Tag+Functionality")
    print()

    found_target_page = False

    for search_term in search_terms:
        print(f"=== Testing search term: '{search_term}' ===")

        results = search_confluence_content(search_term, limit=5, spaces="OPR")
        print(f"Found {len(results)} results:")

        for i, result in enumerate(results, 1):
            page_id = result.get('id')
            title = result.get('title', 'No title')
            url = result.get('url', 'No URL')

            print(f"{i}. {title}")
            print(f"   ID: {page_id}")
            print(f"   URL: {url}")

            if page_id == expected_page_id:
                print(f"   ✅ FOUND TARGET PAGE!")
                found_target_page = True
            elif "skip by tag" in title.lower() or "tag functionality" in title.lower():
                print(f"   🔍 Related tag page found")

        print()

        if found_target_page:
            break

    if not found_target_page:
        print("❌ Target page not found with any search term")
        print("\nTrying broader searches...")

        # Try broader terms
        broad_terms = ["skip", "tag", "VM", "whitelist"]

        for term in broad_terms:
            print(f"\n=== Broad search: '{term}' ===")
            results = search_confluence_content(term, limit=10, spaces="OPR")

            for result in results:
                if result.get('id') == expected_page_id:
                    print(f"✅ Found target page with broad term '{term}'!")
                    print(f"   Title: {result.get('title')}")
                    found_target_page = True
                    break

    if found_target_page:
        print(f"\n✅ SUCCESS: The target page can be found")
    else:
        print(f"\n❌ PROBLEM: The target page is not being returned by searches")

if __name__ == "__main__":
    test_vm_search_terms()