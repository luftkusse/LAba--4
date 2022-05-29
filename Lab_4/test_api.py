import pytest
from unittest.mock import ANY, MagicMock, patch
import json
from flask import request
from app.database_crud import RestApi
from app.menu import *

def test_get_invalid():
    r = RestApi()
    s,c = r.get([None])
    assert s == "Menu not found or message was invalid"
    assert c == 404 

def test_get_menu():
    r = RestApi()
    s,c = r.get(['Menu'])
    assert s == "Bad request. You must send Menu type"
    assert c == 400 

def test_get_buy_stocks_menu():
    r = RestApi()
    s,c = r.get(['BuyStocksMenu'])

    data = share_menu()
    data = json.dumps(data)

    assert s == data
    assert c == 200 

def test_get_back_menu():
    r = RestApi()
    s,c = r.get(['BackMenu'])

    data = main_menu()
    data = json.dumps(data)

    assert s == data
    assert c == 200 

@patch('app.models.Share')
def test_put(mock_module):
    all_by_mock = mock_module.query.all
    r = RestApi()
    assert 200 == r.put(None)

from app.models import Share
@patch('app.models.Share')
def test_put_shares(mock_module):
    obj = Share()
    obj.share_name = "AAPL"
    all_by_mock = mock_module.query.all
    all_by_mock.return_value = [obj] 
    r = RestApi()
    assert 200 == r.put(None)

@patch('app.models.User')
@patch('app.models.UserAndShare')
@patch('app.models.Requests')
def test_delete(user_module, UserAndShare_module, Requests_module):
    user_get_mock = user_module.query.get
    user_filter_by_mock = user_module.query.filter_by
    UserAndShare_filter_by_mock = UserAndShare_module.query.filter_by
    Requests_module_by_mock = Requests_module.query.filter_by

    r = RestApi()
    s,c = r.delete(1)
    assert s == "User was deleted, if he exist"
    assert c == 200 









