import requests

class TelegramManager:
    def __init__(self, token, chatId):
        self.token = token
        self.chatId = chatId

    def notify(self, message):
        if not self.token or not self.chatId:
            print("Telegram config missing.")
            return
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {
            'chat_id': self.chatId,
            'text': message
        }
        try:
            resp = requests.post(url, data=data)
            if resp.status_code != 200:
                print(f"Telegram error: {resp.text}")
        except Exception as e:
            print(f"Telegram exception: {e}")
