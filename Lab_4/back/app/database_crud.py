from flask_restful import Resource
from flask import request
import requests
import yfinance as yahooFinance
import json
import logging
import configparser

from app.menu import *


from multiprocessing import Process
config = configparser.ConfigParser()

config.read('./app/config.ini')
logging.basicConfig(level=config['LOGGING']['level'], filename=config['LOGGING']['filename'])
logger = logging.getLogger(__name__)


class RestApi(Resource):
    def get(self, id):
        p = Process(target=logger.info(f'Get method initialized'))
        if "BuyStocksMenu" in id:
            p = Process(target=logger.info("Stocks menu was returned"))
            chat_data = share_menu()
            chat_data = json.dumps(chat_data)
            return chat_data, 200

        if "Menu" in id:
            p = Process(target=logger.info("Bad request."))
            return "Bad request. You must send Menu type", 400
        if "BackMenu" in id:
            p = Process(target=logger.info("Back menu was returned"))
            chat_data = main_menu()
            chat_data = json.dumps(chat_data)
            return chat_data, 200
        else:
            p = Process(target=logger.info("Bad request."))
            return "Menu not found or message was invalid", 404

    def post(self, id=0):
        from app.models import User, Requests, UserAndShare, Share, Review, db
        chat_data = "Chat info"
        if "callback_query" in request.json:
            user_id = request.json["callback_query"]["from"]["id"]
            rdata = request.json["callback_query"]["data"]
            try:
                user = User.query.get(int(user_id))
                if "BalanceMenu" in rdata:
                    p = Process(target=logger.info("Balance was returned"))
                    balance = user.balance
                    chat_data = json.dumps(f"User test balance: {balance}$")
                    return chat_data, 200
                elif rdata == "AdminMenu" and user.id_admin == 1:
                    p = Process(target=logger.info("AdminMenu was returned. Admin is logged in."))
                    chat_data = json.dumps(admin_menu())
                    return chat_data, 200
                elif rdata == "ChangeBalance":
                    user.balance += 1000
                    db.session.add(user)
                    db.session.commit()
                    chat_data = json.dumps(f"User test balance was updated!: {user.balance}$")
                    return chat_data, 200
                elif rdata == "InfoMenu":
                    shapes = Requests.query.get(int(user_id))
                    message = f"You have {shapes.count} shapes!"
                    chat_data = json.dumps(message)
                    return chat_data, 200
                elif rdata == "ReviewData":
                    chat_data = json.dumps(f"User test balance: {balance}$")
                    return 200
                elif rdata == "AdminInfo":
                    p = Process(target=logger.info("Join request initialized"))
                    from app.models import User, Requests, UserAndShare, Share, Review, db
                    chat_data = "Chat info"
                    users = User.query.all()
                    usersshare = UserAndShare.query.all()
                    shares = Share.query.all()
                    text = "Information:   "
                    for user in users:
                        for shareuser in usersshare:
                            for share in shares:
                                if share.id == shareuser.share_id and shareuser.user_id == user.id:
                                    text += f"User: {user.username} has {share.share_name}!"
                    chat_data = json.dumps(text)
                    return chat_data, 200
            except (RuntimeError, TypeError, NameError, AttributeError):
                chat_data = json.dumps("Error occurred while processing menu operations or buy operations")
                return chat_data, 200
        elif "message" in request.json and "text" in request.json["message"]:
            if "Sell" in request.json["message"]["text"]:
                data = request.json["message"]["text"].split(" ")
                obj = yahooFinance.Ticker(data[-2])
                if obj is None:
                    chat_data = json.dumps(f"Stock name was invalid!")
                    return chat_data, 200
                price = float(obj.info['regularMarketPrice'])
                id = request.json["message"]["from"]["id"]
                user = User.query.get(int(id))
                user.balance += price * int(data[-1])
                req = Requests.query.get(int(id))
                if req is not None:
                    req.count += int(data[-1])
                    db.session.commit()
                    chat_data = json.dumps(
                        f"You have sell some Stocks! Amount:{int(data[-1])}, type: {data[-2]}. Price for one Stock: {price}")
                    return chat_data, 200
                else:
                    pass
            elif "Buy" in request.json["message"]["text"]:
                data = request.json["message"]["text"].split(" ")
                obj = yahooFinance.Ticker(data[-2])
                if obj is None:
                    chat_data = json.dumps(f"Stock name was invalid!")
                    return chat_data, 200
                share = Share(share_name=data[-2], price=float(obj.info['regularMarketPrice']))
                db.session.add(share)
                db.session.commit()
                id = request.json["message"]["from"]["id"]
                user = User.query.get(int(id))
                if share.price * int(data[-1]) <= user.balance:
                    user.balance -= share.price * int(data[-1])
                    req = Requests.query.get(int(id))
                    if req is not None:
                        req.count += int(data[-1])
                        db.session.commit()
                        user_share = UserAndShare(user_id=int(id), share_id=share.id)
                        db.session.add(user_share)
                        db.session.commit()
                        chat_data = json.dumps(f"You have bought some Stocks! Amount:{int(data[-1])}, type: {data[-2]}. Price for one Stock: {share.price}")
                        return chat_data, 200
                    else:
                        pass
                else:
                    chat_data = json.dumps(f"Not enough money")
                    return chat_data, 200
            elif "Review" in request.json["message"]["text"]:
                share_type = request.json["message"]["text"].split(":")[-1]
                shares = Share.query.all()
                index = -1
                share_type = share_type.replace(" ", "")
                for i in shares:
                    if i.share_name == share_type:
                        index = i.id
                if index != -1:
                    review = Review(text_review=request.json["message"]["text"], share_id=index)
                    chat_data = json.dumps(f"Your review was successfully send")
                    return chat_data, 200
                else:
                    chat_data = json.dumps(f"Invalid type of stock")
                    return chat_data, 200
            else:
                user_id = request.json["message"]["from"]["id"]
                p = Process(target=logger.info(f"User: {user_id} is starting application"))
                username = request.json["message"]["from"]["username"]
                myuser = User.query.get(int(user_id))
                if myuser is None and request.json["message"]["text"] == "/start":
                    myuser = User(id=int(user_id), id_admin=int(1), username=username, balance=float(1000))
                    request_my = Requests(user_id=int(user_id), count=int(0))
                    db.session.add(myuser)
                    db.session.commit()
                    db.session.add(request_my)
                    db.session.commit()
                    chat_data = main_menu()
                    chat_data = json.dumps(chat_data)
                    return chat_data, 200
                else:
                    chat_data = main_menu()
                    chat_data = json.dumps(chat_data)
                    return chat_data, 200
        chat_data = "Error request!"
        chat_data = json.dumps(chat_data)
        return chat_data, 200

    def put(self, id):
        p = Process(target=logger.info("Put method initialized"))
        from app.models import User, Requests, UserAndShare, Share, Review, db
        shares = Share.query.all()
        for share in shares:
            obj = yahooFinance.Ticker(share.share_name)
            if obj is not None:
                share.price = float(obj.info['regularMarketPrice'])
                db.session.commit()
        return 200

    def delete(self, id):
        from app.models import User, Requests, UserAndShare, Share, Review, db
        user = User.query.get(int(id))
        UserAndShare.query.filter_by(user_id=user.id).delete()
        Requests.query.filter_by(user_id=user.id).delete()
        User.query.filter_by(id=user.id).delete()
        db.session.commit()
        return "User was deleted, if he exist", 200