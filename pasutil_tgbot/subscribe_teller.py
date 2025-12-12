import telebot

def check_user_subscription(bot_instance: telebot.TeleBot, channel_username: str, user_id: int) -> bool:
    try:
        member = bot_instance.get_chat_member(channel_username, user_id)
        return member.status in ("member", "administrator", "creator")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error")
        return False 
    except Exception as e:
        print(f"No name error")
        return False
