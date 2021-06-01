import json

# with open('data/farms_scrape.json', mode='w', encoding='utf-8') as json_file:
#     print('file_open')
#     # existing_data = json.load(json_file)
#     farm = '{"lat": 47.162544100000, "lon": -114.084739800000,"link": "https://www.workaway.info/en/host/227416959459","available_months": [4,5,6]}'
#     jsonified_farm = json.loads(farm)
#     # existing_data.update(jsonified_farm)
#     json.dump(jsonified_farm, json_file)

with open('data/farms_scrape.json', mode='r+', encoding='utf-8') as json_file:
    existing_data = open('data/farms_scrape.json', mode='r', encoding='utf-8').read()
    farm = {"lat": 47.162544100000, "lon": -114.084739800000,"link": "https://www.workaway.info/en/host/227416959459","available_months": [4,5,6,7]}
    farm_double_quote = str(farm).replace("'",'"')
    z = json.loads(existing_data)
    z.update(farm_double_quote)
    # z = json.loads(existing_data)
    # print(type(z))
    # z.update(farm_double_quote)
    json.dumps(z)