#!/usr/bin/env python3
"""
Test direct search for the VM scanning page.
"""

import dotenv
import os
from confluence_tools import init_confluence_client, get_confluence_client

dotenv.load_dotenv()

def test_direct_search():
    """Test direct client search for VM scanning page"""

    # Initialize client
    init_confluence_client(
        os.getenv("CONFLUENCE_BASE_URL"),
        os.getenv("CONFLUENCE_TOKEN"),
        os.getenv("CONFLUENCE_EMAIL")
    )

    client = get_confluence_client()
    expected_page_id = "3278536757"

    print(f"Looking for page ID: {expected_page_id}")
    print(f"Expected: SRE Operations: Skip by Tag Functionality")
    print()

    # Test 1: Try to get the specific page directly
    print("=== Test 1: Direct page access ===")
    try:
        page = client.get_page_content(expected_page_id)
        if page:
            print(f"✅ Page exists: {page.get('title')}")
        else:
            print("❌ Page not accessible")
    except Exception as e:
        print(f"❌ Error accessing page: {e}")

    # Test 2: Search terms that should find this page
    search_terms = [
        "VM scanning whitelist",
        "skip by tag",
        "tag functionality",
        "VM whitelist",
        "scanning VMs"
    ]

    for search_term in search_terms:
        print(f"\n=== Search: '{search_term}' ===")
        try:
            results = client.search_content(search_term, limit=10, spaces=["OPR"])
            print(f"Found {len(results)} results")

            found_target = False
            for i, result in enumerate(results, 1):
                page_id = result.get('id')
                title = result.get('title', 'No title')
                space = result.get('space', {})

                print(f"{i}. {title} (ID: {page_id})")

                if page_id == expected_page_id:
                    print(f"   ✅ FOUND TARGET PAGE!")
                    found_target = True

            if not found_target:
                print(f"   ❌ Target page not found in results")

        except Exception as e:
            print(f"❌ Search error: {e}")

    # Test 3: Check what the raw CQL query returns
    print(f"\n=== Test 3: Raw CQL search ===")
    try:
        cql = 'text ~ "skip by tag" AND (space = "OPR")'
        params = {
            "cql": cql,
            "limit": 10,
            "expand": "space,version"
        }

        raw_result = client._make_request("GET", "content/search", params=params)
        results = raw_result.get("results", [])
        print(f"CQL '{cql}' returned {len(results)} results:")

        for result in results:
            page_id = result.get('id')
            title = result.get('title')
            print(f"  • {title} (ID: {page_id})")

            if page_id == expected_page_id:
                print(f"    ✅ TARGET PAGE FOUND!")

    except Exception as e:
        print(f"❌ CQL search error: {e}")

if __name__ == "__main__":
    test_direct_search()