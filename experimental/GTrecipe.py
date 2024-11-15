import requests
from bs4 import BeautifulSoup

def get_item_title(html_result: BeautifulSoup) -> str:
    title_tag = html_result.find('span', class_="mw-headline")
    try: title_tag.small.decompose()
    except AttributeError: pass
    return title_tag.get_text(strip=True).replace(u'\xa0', u' ')

def get_item_recipe(item_name, region="en"):
    try:
        search_response = requests.get(f"https://growtopia.fandom.com/{region}/api/v1/SearchSuggestions/List?query={item_name}").json()
        try:
            item_page_response = requests.get(f"https://growtopia.fandom.com/{region}/wiki/{search_response['items'][0]['title']}")
            try:
                html_content = BeautifulSoup(item_page_response.text, "html.parser")
                required_indices = []
                result = {}

                def insert_recipe(item_name, recipe):
                    if item_name in recipe.keys():
                        recipe[item_name].append([])
                        for cell in item.select('td'):
                            cell_text = cell.get_text(' ', strip=True).replace('"', "'")
                            recipe[item_name][1].append(cell_text.replace(u'\xa0', u''))
                    else:
                        recipe[item_name] = [[]]
                        for cell in item.select('td'):
                            cell_text = cell.get_text(' ', strip=True).replace('"', "'")
                            recipe[item_name][0].append(cell_text.replace(u'\xa0', u''))

                def insert_sub_recipe(sub_item_name, recipe):
                    if sub_item_name in recipe[main_item_name].keys():
                        recipe[main_item_name][sub_item_name].append([])
                        for sub_cell in sub_item.select('td'):
                            sub_cell_text = sub_cell.get_text(' ', strip=True).replace('"', "'")
                            recipe[main_item_name][sub_item_name][1].append(sub_cell_text.replace(u'\xa0', u''))
                    else:
                        recipe[main_item_name][sub_item_name] = [[]]
                        for sub_cell in sub_item.select('td'):
                            sub_cell_text = sub_cell.get_text(' ', strip=True).replace('"', "'")
                            recipe[main_item_name][sub_item_name][0].append(sub_cell_text.replace(u'\xa0', u''))

                if not html_content.select(".wds-tab__content"):
                    ws = 0
                    count = 0
                    recipe = {}
                    for item in html_content.select(".content"):
                        if not item.select(".content"):
                            if count not in required_indices:
                                insert_recipe(item.find('th').text.strip(), recipe)
                            ws += 1
                        else:
                            main_item_name = item.find('th').text.strip()
                            recipe[main_item_name] = {}
                            for sub_item in item.select(".content"):
                                insert_sub_recipe(sub_item.find('th').text.strip(), recipe)
                                ws += 1
                                required_indices.append(ws)
                        count += 1
                    result[get_item_title(html_content)] = recipe
                    result[get_item_title(html_content)]["Title"] = search_response["items"][0]["title"]
                else:
                    for tab_content in html_content.select(".wds-tab__content"):
                        ws = 0
                        count = 0
                        recipe = {}
                        if not tab_content.select(".content"):
                            for item in html_content.select(".content"):
                                if not item.select(".content"):
                                    if count not in required_indices:
                                        insert_recipe(item.find('th').text.strip(), recipe)
                                    ws += 1
                                else:
                                    main_item_name = item.find('th').text.strip()
                                    recipe[main_item_name] = {}
                                    for sub_item in item.select(".content"):
                                        insert_sub_recipe(sub_item.find('th').text.strip(), recipe)
                                        ws += 1
                                        required_indices.append(ws)
                                count += 1
                            result[get_item_title(tab_content)] = recipe
                            result[get_item_title(tab_content)]["Title"] = search_response["items"][0]["title"]
                        else:
                            for item in tab_content.select(".content"):
                                if not item.select(".content"):
                                    if count not in required_indices:
                                        insert_recipe(item.find('th').text.strip(), recipe)
                                    ws += 1
                                else:
                                    main_item_name = item.find('th').text.strip()
                                    recipe[main_item_name] = {}
                                    for sub_item in item.select(".content"):
                                        insert_sub_recipe(sub_item.find('th').text.strip(), recipe)
                                        ws += 1
                                        required_indices.append(ws)
                                count += 1
                            result[get_item_title(tab_content)] = recipe
                            result[get_item_title(tab_content)]["Title"] = search_response["items"][0]["title"]
                try:
                    return result[search_response["items"][0]["title"]]
                except:
                    if item_name in result.keys():
                        return result[item_name]
                    else:
                        return result
            except:
                return {"Error": f"Sorry! I can't find {item_name} in Growtopia Fandom {region} Error Code 3"}
        except IndexError:
            return {"Error": f"Sorry! I can't find {item_name} in Growtopia Fandom {region} Error Code 2"}
    except:
        return {"Error": f"It looks like we can't reach fandom.com {region}! Try again later. Error Code 1"}


# Legacy
# def get_item_recipe(item_name: str) -> dict:
#     try:
#         item_found = search_item(item_name, allow_partial_match=False)[0]
#         item_page = get_raw_html(item_found["Url"])
#     except IndexError:
#         raise Exception(f"Item '{item_name}' not found")

#     recipe_contents = item_page.select("div.mw-parser-output > div.recipebox")
#     recipes = []
#     for recipe_content in recipe_contents:
#         recipe = {}
#         recipe["Title"] = recipe_content.select_one("th").get_text(strip=True)
#         rows = recipe_content.select("table tr:not(:first-of-type)")

#         for row in rows:
#             # delete all tags except <br/>
#             for tag in row.find_all():
#                 if tag.name != "br":
#                     tag.unwrap()

#             line = row.get_text(separator=" ", strip=True).replace("\n", " ").split("•")

#             # Menampilkan hasil
#             if recipe["Title"] == "Splicing" and "Items" not in recipe:
#                 seeds = line[0].rstrip("Seed").split("Seed")
#                 if len(seeds) == 2:
#                     for seed in seeds:
#                         recipe.setdefault("Items", []).append(f"{seed.strip()} Seed")

#             if line[0].strip() != "" and "description" in recipe and "Extra" not in recipe and recipe["Title"] != "Splicing":
#                 recipe["Extra"] = line[0].strip()

#             if line[0].strip() != "" and "description" not in recipe:
#                 recipe["description"] = line[0].strip()

#             if len(line) > 1:
#                 for i in range(1, len(line)):
#                     recipe.setdefault("items", []).append(line[i].rstrip(" , or").strip())

#         recipes.append(recipe)
#     print(len(recipe_contents))
#     return recipes

# pprint(get_item_recipe("Laser grid"))