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
        for idx, html_content_tabber in enumerate(item_page.select(".gtw-card")):   
            tabber_result = {}   
            parse_html_content(html_content_tabber, tabber_result)
            if idx == 0:
                # at the first iteration, if subitems are not included, result is the first tabber
                result = tabber_result
                if not include_subitems: break
            else:
                # sub items has different title
                title_tag = html_content_tabber.find('span', class_="mw-headline")
                if title_tag and title_tag.small:
                    title_tag.small.decompose()
                tabber_result["Title"] = title_tag.get_text(strip=True).replace('\xa0', ' ')
                result.setdefault("SubItems", []).append(tabber_result)
    # This has to be done at the end
    result["Title"] = item_found["Title"]
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
            if not any(kw in item['title'].lower() for kw in ['category:', 'update', 'disambiguation', 'week', 'mods/'])
            and (item_name.lower() in item['title'].lower())
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
    properties_result = []
    properties = html_content.find_all('div', class_="card-text")
    data_fields = html_content.select(".card-field")

    rarity_text = BeautifulSoup((str((html_content.find('small'))).replace("(Rarity: ", "")).replace(")", ""), "html.parser").text
    try: result.update({"Rarity": int(rarity_text)})
    except: result.update({"Rarity": "None"})
    
    for property in properties:
        parsed_property = BeautifulSoup(str(property).replace("<br/>", "--split--"), "html.parser")
        properties_result.append(parsed_property.text)
    properties_list = (properties_result[1].strip()).split("--split--")
    result.update({"Description": properties_result[0].strip()})
    result.update({"Properties": "None" if properties_list == ['None'] else properties_list})
        
    data_result = []
    for data_field in data_fields:
        parsed_data = BeautifulSoup((str(data_field).replace("</tr>", ",")).replace("</th>", ","), "html.parser")
        data_result = (((parsed_data.text).split(",")))
    
    for i in range(0, len(data_result) - 2, 2):
        key = data_result[i].strip().replace(" ", "")
        value = data_result[i + 1].strip()
        result[key] = value

    for idx, (key, value) in enumerate(result.items()):
        if idx == 3:
            result[key] = value.split(" - ")
        elif idx == 8:
            result[key] = value.split(" ")
        elif idx == 7:
            digits_list = ["".join(filter(str.isdigit, part)) for part in value.split(" ") if any(char.isdigit() for char in part)]
            result[key] = {
                "Fist": digits_list[0] if len(digits_list) > 0 else None,
                "Pickaxe": digits_list[1] if len(digits_list) > 1 else None,
                "Restore": digits_list[2] if len(digits_list) > 2 else None
            }
    
    result["Sprite"] = {
        "Item": html_content.select_one('div.card-header img')['src'],
        "Tree": html_content.select_one('th:-soup-contains("Grow Time") + td img')['src'],
        "Seed": html_content.select_one('td.seedColor img')['src']
    }
