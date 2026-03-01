# SPDX-License-Identifier: AGPL-3.0-or-later
"""Rust Standard Library (doc.rust-lang.org/std)"""

from urllib.parse import quote_plus
from lxml import html
from searx.utils import eval_xpath, eval_xpath_list, extract_text

about = {
    "website": "https://doc.rust-lang.org/std",
    "wikidata_id": None,
    "official_api_documentation": "https://doc.rust-lang.org/std",
    "use_official_api": False,
    "require_api_key": False,
    "results": "HTML",
}

categories = ["it", "software wikis"]
paging = False

base_url = "https://doc.rust-lang.org"


def request(query, params):
    # Rust stdlib docs use a search parameter
    params["url"] = f"{base_url}/stable/std/index.html?search={quote_plus(query)}"
    return params


def response(resp):
    results = []
    # The Rust docs search is JavaScript-based, so we return a direct link
    # In the future, this could be enhanced if a JSON API becomes available
    query = resp.search_params["q"]

    results.append(
        {
            "title": f'Search Rust stdlib for "{query}"',
            "url": f"{base_url}/stable/std/index.html?search={quote_plus(query)}",
            "content": f"Search the Rust Standard Library documentation for {query}",
        }
    )

    return results
