# SPDX-License-Identifier: AGPL-3.0-or-later
"""Lobste.rs - Computing-focused community"""

from urllib.parse import quote_plus
from lxml import html
from searx.utils import eval_xpath, eval_xpath_list, extract_text

about = {
    "website": "https://lobste.rs",
    "wikidata_id": None,
    "official_api_documentation": "https://lobste.rs",
    "use_official_api": False,
    "require_api_key": False,
    "results": "HTML",
}

categories = ["it", "social media"]
paging = True

base_url = "https://lobste.rs"
results_xpath = '//div[@class="story"]'
url_xpath = './/a[@class="u-url"]/@href'
title_xpath = './/a[@class="u-url"]/text()'
content_xpath = './/div[@class="byline"]'
tags_xpath = './/a[@class="tag"]/text()'
score_xpath = './/div[@class="score"]/text()'
comments_xpath = './/a[contains(@href,"comments")]/text()'


def request(query, params):
    page = params["pageno"]
    params["url"] = (
        f"{base_url}/search?q={quote_plus(query)}&what=stories&order=relevance&page={page}"
    )
    return params


def response(resp):
    results = []
    doc = html.fromstring(resp.text)

    for result in eval_xpath_list(doc, results_xpath):
        title = extract_text(eval_xpath(result, title_xpath))
        if not title:
            continue

        url = extract_text(eval_xpath(result, url_xpath))
        if url and not url.startswith("http"):
            url = base_url + url

        content = extract_text(eval_xpath(result, content_xpath))
        tags = eval_xpath_list(result, tags_xpath)
        score = extract_text(eval_xpath(result, score_xpath))
        comments = extract_text(eval_xpath(result, comments_xpath))

        metadata = []
        if score:
            metadata.append(f"Score: {score}")
        if comments:
            metadata.append(comments)
        if tags:
            metadata.append(f"Tags: {', '.join(tags)}")

        results.append(
            {
                "title": title,
                "url": url or base_url,
                "content": content or "",
                "metadata": " | ".join(metadata) if metadata else "",
            }
        )

    return results
