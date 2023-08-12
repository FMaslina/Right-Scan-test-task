import json
from datetime import datetime
from ru.travelfood.simple_ui import SimpleSQLProvider as sqlClass


def init_on_start(hashMap, _files=None, _data=None):
    hashMap.put("SQLConnectDatabase", "test1.DB")
    hashMap.put("SQLExec",
                json.dumps({"query": "create table IF NOT EXISTS Bird(id integer primary key autoincrement, name text,"
                                     " feather_color text, image text)", "params": ""}))


def get_all_birds(hash_map, _files=None, _data=None):
    cards = {"customcards": {
        "options": {
            "search_enabled": True,
            "save_position": True
        },

        "layout": {
            "type": "LinearLayout",
            "orientation": "vertical",
            "height": "match_parent",
            "width": "match_parent",
            "weight": "0",
            "Elements": [
                {
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [
                        {
                            "type": "Picture",
                            "show_by_condition": "",
                            "Value": "@pic1",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "8",
                            "TextColor": "#DB7093",
                            "TextBold": True,
                            "TextItalic": False,
                            "BackgroundColor": "",
                            "width": "400",
                            "height": "match_parent",
                            "weight": "1"
                        },
                        {
                            "type": "LinearLayout",
                            "orientation": "vertical",
                            "height": "wrap_content",
                            "width": "match_parent",
                            "weight": "1",
                            "Elements": [
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@name",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "TextSize": "30",
                                    "Variable": "",
                                },
                                {
                                    "type": "TextView",
                                    "show_by_condition": "",
                                    "Value": "@feather_color",
                                    "NoRefresh": False,
                                    "document_type": "",
                                    "mask": "",
                                    "TextSize": "30",
                                    "StrokeWidth": "10",
                                    "Variable": ""
                                }
                            ]
                        },
                        {
                            "type": "Button",
                            "height": "match_parent",
                            "width": "wrap_content",
                            "weight": "0",
                            "Value": "Подробнее",
                            "Variable": "btn_detail"
                        }
                    ]
                },
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "@descr",
                    "NoRefresh": False,
                    "document_type": "",
                    "mask": "",
                    "Variable": "",
                    "TextSize": "-1",
                    "TextColor": "#6F9393",
                    "TextBold": False,
                    "TextItalic": True,
                    "BackgroundColor": "",
                    "width": "wrap_content",
                    "height": "wrap_content",
                    "weight": 0
                }
            ]
        }

    }
    }

    cards["customcards"]["cardsdata"] = []
    sql = sqlClass()
    res = sql.SQLQuery("select * from Bird", "")
    records = json.loads(res)
    for record in records:
        card_data = {
            "key": str(record['id']),
            "descr": f"ID {record['id']}",
            "name": str(record['name']),
            "feather_color": str(record['feather_color']),
            "pic1": str(record['image'])
        }

        cards["customcards"]["cardsdata"].append(card_data)

    hash_map.put("cards", json.dumps(cards, ensure_ascii=False).encode('utf8').decode())

    return hash_map


def open_other_screens(hash_map, _files=None, _data=None):
    if hash_map.get("listener") == "create_btn":
        hash_map.put("ShowScreen", "Добавление птиц")
    elif hash_map.get("listener") == "delete_btn":
        hash_map.put("ShowScreen", "Удаление птиц")
    elif hash_map.get("listener") == "LayoutAction":
        hash_map.put("ShowScreen", "Птица")
    elif hash_map.get("listener") == "back":
        hash_map.put("ShowScreen", "Список птиц")
    return hash_map


def add_bird(hash_map, _files=None, _data=None):
    name = hash_map.get('name')
    feather_color = hash_map.get("feather_color")
    image = hash_map.get("picture")
    if hash_map.get("listener") == "btn":
        sql = sqlClass()
        sql.SQLExec("insert into Bird(name,feather_color, image) values(?, ?, ?)", f"{name}, {feather_color}, {image}")
        hash_map.put("toast", f'Птица "{name}" успешно добавлена в список')
        hash_map.put("ShowScreen", "Список птиц")
    return hash_map


def delete_bird(hash_map, _files=None, _data=None):
    sql = sqlClass()
    if hash_map.get("listener") == "btn":
        sql.SQLExec("delete from Bird where id=?", hash_map.get('id'))
        hash_map.put("toast", f'Птица "{hash_map.get("id")}" успешно удалена из списка')
    elif hash_map.get("listener") == "btn_all":
        hash_map.put("SQLExec",
                     json.dumps(
                         {"query": "delete from Bird ", "params": ""}))
        hash_map.put("toast", "Все птицы удалены")
    hash_map.put("ShowScreen", "Список птиц")
    return hash_map


def get_bird_card(hash_map, _files=None, _data=None):
    card_data = json.loads(hash_map.get("card_data"))
    hash_map.put("image", card_data["pic1"])
    hash_map.put("name", card_data["name"])
    hash_map.put("feather_color", card_data["feather_color"])
    return hash_map
