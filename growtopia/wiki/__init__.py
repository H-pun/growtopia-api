import re
import requests
from bs4 import BeautifulSoup


def get_item_data(item_name, include_subitems: bool = False) -> dict:
    try:
        item_found = search_item(item_name, allow_partial_match=False)[0]
        item_page = get_raw_html(item_found["Url"])
    except IndexError:
        raise Exception(f"Item '{item_name}' not found")
    result = {}
    if len(item_page.select(".gtw-card")) == 1:
        parse_html_content(item_page, result)
    else:
        for idx, html_content_tabber in enumerate(item_page.select(".wds-tab__content")):
            tabber_result = {}
            parse_html_content(html_content_tabber, tabber_result)
            if idx == 0:
                # at the first iteration, if subitems are not included, result is the first tabber
                result = tabber_result
                if not include_subitems:
                    break
            else:
                result.setdefault("SubItems", []).append(tabber_result)
    # Must be the last line
    result["Url"] = item_found["Url"]
    return result


def search_item(item_name: str, allow_partial_match: bool = True, show_url: bool = True) -> list[dict[str, str]]:
    # NOTE: partial match search sometimes returns irrelevant results
    try:
        params = {
            "action": "query",
            "srlimit": 20,
            "list": "search",
            "srsearch": item_name,
            "format": "json"
        } if allow_partial_match else {
            "query": item_name
        }
        url = "https://growtopia.fandom.com/api.php" if allow_partial_match else "https://growtopia.fandom.com/api/v1/SearchSuggestions/List"
        data = requests.get(url, params=params).json()
        items = [
            {
                "Title": item['title'],
                **({"Url": f"https://growtopia.fandom.com/wiki/{item['title'].replace(' ', '_')}"} if show_url else {})
            } for item in (data['query']['search'] if allow_partial_match else data['items'])
            if not allow_partial_match or allow_partial_match and (item_name.lower() in item['title'].lower()) and
            not any(kw in item['title'].lower() for kw in ['category:', 'update', 'disambiguation', 'week', 'mods/'])
        ]
        return items
    except requests.RequestException as error:
        raise Exception(f"Wiki search fetch failed: {error}")


def get_raw_html(url: str) -> BeautifulSoup:
    try:
        item_page_response = requests.get(url)
        return BeautifulSoup(item_page_response.text, "html.parser")
    except requests.RequestException as error:
        raise Exception(f"Wiki page fetch failed: {error}")


def parse_html_content(html_content: BeautifulSoup, result: dict):
    result["Title"] = get_item_title(html_content)
    result["Rarity"] = get_item_rarity(html_content)
    result["Description"] = get_item_description(html_content)
    result["Properties"] = get_item_properties(html_content)
    result["Type"] = get_simple_item_data(html_content, 1, " - ")
    result["Chi"] = get_simple_item_data(html_content, 2)
    result["TextureType"] = get_simple_item_data(html_content, 3)
    result["CollisionType"] = get_simple_item_data(html_content, 4)
    result["Hardness"] = get_item_hardness(html_content)
    result["SeedColor"] = get_simple_item_data(html_content, 6, " ")
    result["GrowTime"] = get_simple_item_data(html_content, 7)
    result["DefaultGemsDrop"] = get_simple_item_data(html_content, 8)
    result["Sprite"] = get_item_sprite(html_content)
    result["Recipe"] = get_item_recipes(html_content)


def get_item_title(html_content: BeautifulSoup) -> str:
    return html_content.select_one('span.mw-headline').get_text(strip=True, separator="\n").split("\n")[0].replace(u'\xa0', u' ')


def get_item_rarity(html_content: BeautifulSoup) -> int | str:
    rarity_tag = html_content.select_one('small:-soup-contains("Rarity")')
    return int(re.search(r'\d+', rarity_tag.text).group()) if rarity_tag else "None"


def get_item_description(html_content: BeautifulSoup) -> str:
    return html_content.select_one('div.card-text').text


def get_item_properties(html_content: BeautifulSoup) -> list[str]:
    properties_tag = html_content.select_one('b:-soup-contains("Properties") + div.card-text')
    for br in properties_tag.find_all("br"):
        br.replace_with("--split--")
    return properties_tag.text.split("--split--")


def get_simple_item_data(html_content: BeautifulSoup, order: int, separator: str = "") -> str | list[str]:
    data_tag = html_content.select_one(f'tbody > tr:nth-of-type({order}) > td').get_text(strip=True, separator=" ")
    return data_tag.split(separator) if separator else data_tag


def get_item_hardness(html_content: BeautifulSoup) -> dict[str, str]:
    text = get_simple_item_data(html_content, 5)
    digits = list(map(int, re.findall(r'\d+', text)))
    return {
        "Fist": digits[0] if len(digits) > 0 else None,
        "Pickaxe": digits[1] if len(digits) > 1 else None,
        "Restore": digits[2] if len(digits) > 2 else None
    }


def get_item_sprite(html_content: BeautifulSoup) -> dict[str, str]:
    return {
        "Item": html_content.select_one('div.card-header img')['src'],
        "Tree": html_content.select_one('th:-soup-contains("Grow Time") + td img')['src'],
        "Seed": html_content.select_one('td.seedColor img')['src']
    }

# Due to the inconsistency of the wiki page, which is sucks, I will only parse the title
def get_item_recipes(html_content: BeautifulSoup) -> list[str]:
    return [
        recipe.select_one("th").get_text(strip=True)
        for recipe in html_content.select("div.recipebox") # recursive
    ]
