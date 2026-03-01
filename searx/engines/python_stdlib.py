# SPDX-License-Identifier: AGPL-3.0-or-later
"""Python Standard Library Documentation"""

from urllib.parse import quote_plus
from lxml import html
from searx.utils import eval_xpath, eval_xpath_list, extract_text

about = {
    "website": "https://docs.python.org",
    "wikidata_id": None,
    "official_api_documentation": "https://docs.python.org",
    "use_official_api": False,
    "require_api_key": False,
    "results": "HTML",
}

categories = ["it", "software wikis"]
paging = False

base_url = "https://docs.python.org"
search_path = "/3/search.html"


def request(query, params):
    # Python docs use Sphinx search
    params["url"] = f"{base_url}{search_path}?q={quote_plus(query)}"
    return params


def response(resp):
    results = []
    doc = html.fromstring(resp.text)

    # Sphinx search results structure
    search_results = eval_xpath_list(doc, '//ul[@class="search"]/li')

    if search_results:
        for result in search_results:
            link = eval_xpath(result, ".//a")
            if link:
                title = extract_text(link[0])
                url = extract_text(eval_xpath(link[0], "./@href"))
                content = extract_text(eval_xpath(result, "./p"))

                if title and url:
                    if not url.startswith("http"):
                        url = base_url + "/3/" + url
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
                "title": f'Search Python docs for "{query}"',
                "url": f"{base_url}{search_path}?q={quote_plus(query)}",
                "content": f"Search Python {query} in the official documentation",
            }
        )

    return results
