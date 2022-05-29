from app.config import URL_WEB, TELEGRAM_URL, BOT_TOKEN
from app.menu import *
import requests
import json
import ast


def validate_request(data):
    if data is None:
        return "No data", 200
    headers = {"Content-type": "application/json"}
    message_url = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/sendMessage"
    if "callback_query" in data:
        user_id = data["callback_query"]["from"]["id"]
        rdata = data["callback_query"]["data"]
        url = URL_WEB + "/share-api/"
        chat_data = {"chat_id": user_id, "text": "Menu"}
        if "BuyStocksMenu" in rdata:
            url += "BuyStocksMenu"
            chat_data["text"] = "To buy stocks input next message: Buy name_of_stock amount. Example: Buy MTC 3. Same with sell."
            request_data = requests.get(url).content
            json_response = json.loads(request_data)
            dictionary_response = dict(ast.literal_eval(json_response))
            chat_data.update(dictionary_response)
            chat_data = json.dumps(chat_data)
            requests.post(message_url, headers=headers, data=chat_data)
        elif "ReviewData" in rdata:
            url += "BuyShareMenu"
            chat_data["text"] = "To send review about stocks input next message: Review: message. Example: Review: normal stock. Stock: MTC"
            chat_data = json.dumps(chat_data)
            requests.post(message_url, headers=headers, data=chat_data)
        elif "BackMenu" in rdata:
            url += "BackMenu"
            chat_data["text"] = "MainMenu"
            request_data = requests.get(url).content
            json_response = json.loads(request_data)
            dictionary_response = dict(ast.literal_eval(json_response))
            chat_data.update(dictionary_response)
            chat_data = json.dumps(chat_data)
            requests.post(message_url, headers=headers, data=chat_data)
        elif "DeleteUser" in rdata:
            url += f"{user_id}"
            requests.delete(url)
            chat_data["text"] = "User was deleted! If you want to start new game, just write /start"
            requests.post(message_url, headers=headers, data=chat_data)
        elif "UpdateShares" in rdata:
            requests.put(url=url)
        elif "AdminMenu" in rdata:
            url = URL_WEB + "/share-api/" + rdata
            send_data = json.dumps(data)
            request_data = requests.post(url, headers=headers, data=send_data).content
            json_response = json.loads(request_data)
            dictionary_response = dict(ast.literal_eval(json_response))
            chat_data.update(admin_menu())
            chat_data = json.dumps(chat_data)
            requests.post(message_url, data=chat_data, headers=headers)
        elif "InfoMenu" in rdata or "BalanceMenu" in rdata or "ReviewData" in rdata or "AdminInfo" in rdata\
                or "ChangeBalance" in rdata:
            url = URL_WEB + "/share-api/" + rdata
            send_data = json.dumps(data)
            request_data = requests.post(url, headers=headers, data=send_data).content
            string_response = json.loads(request_data)
            chat_data["text"] = string_response
            requests.post(message_url, data=chat_data)
    elif "message" in data:
        if data["message"]["text"] == "/start":
            url = URL_WEB + "/share-api/"
            send_data = json.dumps(data)
            request_data = requests.post(url, headers=headers, data=send_data).content
            json_response = json.loads(request_data)
            dictionary_response = dict(ast.literal_eval(json_response))
            user_id = data["message"]["from"]["id"]
            chat_data = {"chat_id": user_id, "text": "Bot initialized!"}
            chat_data.update(dictionary_response)
            chat_data = json.dumps(chat_data)
            requests.post(message_url, headers=headers, data=chat_data)
        elif "Buy" in data["message"]["text"] or "Review" in data["message"]["text"] or "Sell" in data["message"]["text"]:
            url = URL_WEB + "/share-api/"
            send_data = json.dumps(data)
            request_data = requests.post(url, headers=headers, data=send_data).content
            json_response = json.loads(request_data)
            user_id = data["message"]["from"]["id"]
            chat_data = {"chat_id": user_id, "text": json_response}
            chat_data = json.dumps(chat_data)
            requests.post(message_url, headers=headers, data=chat_data)
    else:
        return "Use buttons to communicate with bot!", 200
