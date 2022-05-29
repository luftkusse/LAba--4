def main_menu():
    return {
        "reply_markup": {"inline_keyboard": [[{"text": "BuyStocks", "callback_data": "BuyStocksMenu"},
                                              {"text": "Info", "callback_data": "InfoMenu"}],
                                             [{"text": "Balance", "callback_data": "BalanceMenu"},
                                              {"text": "Admin", "callback_data": "AdminMenu"}]]}}


def share_menu():
    return {
        "reply_markup": {"inline_keyboard": [[{"text": "Back", "callback_data": "BackMenu"},
                                              {"text": "Review", "callback_data": "ReviewData"}]]}}


def admin_menu():
    return {
        "reply_markup": {"inline_keyboard": [[{"text": "Back", "callback_data": "BackMenu"},
                                              {"text": "Info", "callback_data": "AdminInfo"}],
                                             [{"text": "ChangeBalance", "callback_data": "ChangeBalance"},
                                              {"text": "DeleteUser", "callback_data": "DeleteUser"}],
                                             [{"text": "UpdateShares", "callback_data": "UpdateShares"}]]}}