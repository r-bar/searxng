# SPDX-License-Identifier: AGPL-3.0-or-later
"""The Rust Programming Language Book"""

from urllib.parse import quote_plus
from lxml import html
from searx.utils import eval_xpath, eval_xpath_list, extract_text

about = {
    "website": "https://doc.rust-lang.org/book",
    "wikidata_id": None,
    "official_api_documentation": "https://doc.rust-lang.org/book",
    "use_official_api": False,
    "require_api_key": False,
    "results": "HTML",
}

categories = ["it", "software wikis"]
paging = False

base_url = "https://doc.rust-lang.org/book"


def request(query, params):
    params["url"] = f"{base_url}/search.html?q={quote_plus(query)}"
    return params


def response(resp):
    results = []
    # The Rust book uses mdBook which has a search feature
    # We attempt to parse the search results if available
    doc = html.fromstring(resp.text)

    # mdBook search results structure
    search_results = eval_xpath_list(doc, '//ul[@id="search-results"]/li')

    if search_results:
        for result in search_results:
            title = extract_text(eval_xpath(result, ".//a/text()"))
            url = extract_text(eval_xpath(result, ".//a/@href"))
            content = extract_text(eval_xpath(result, ".//p"))

            if title and url:
                if not url.startswith("http"):
                    url = base_url + "/" + url
                results.append(
                    {
                        "title": title,
                        "url": url,
                        "content": content or "",
                    }
                )

    if not results:
        # Fallback: provide direct search link
        query = resp.search_params["q"]
        results.append(
            {
                "title": f'Search Rust Book for "{query}"',
                "url": f"{base_url}/search.html?q={quote_plus(query)}",
                "content": f"Search The Rust Programming Language book for {query}",
            }
        )

    return results
