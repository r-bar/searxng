# SPDX-License-Identifier: AGPL-3.0-or-later
"""DevDocs API Documentation"""

from urllib.parse import quote_plus

about = {
    "website": "https://devdocs.io",
    "wikidata_id": None,
    "official_api_documentation": "https://devdocs.io",
    "use_official_api": True,
    "require_api_key": False,
    "results": "JSON",
}

categories = ["it", "software wikis"]
paging = False

base_url = "https://devdocs.io"
search_url = "https://devdocs.io/docs.json"


def request(query, params):
    # DevDocs uses a client-side search, but we can use the docs.json endpoint
    # to get all documentation names and create direct links
    params["url"] = f"{base_url}/#q={quote_plus(query)}"
    return params


def response(resp):
    results = []
    # Since DevDocs is client-side rendered, we extract from the URL hash
    # and provide a direct link to the search
    # The actual search is performed on the client side
    query = resp.search_params["q"]

    results.append(
        {
            "title": f'Search DevDocs for "{query}"',
            "url": f"{base_url}/#q={quote_plus(query)}",
            "content": f"Search DevDocs API documentation for {query}",
        }
    )

    return results
