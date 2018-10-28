import requests


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.api_file_url = "https://api.telegram.org/file/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        try:
            result_json = resp.json()['result']
            return result_json
        except KeyError:
            return None

    def send_message(self, chat_id, text):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        resp = requests.post(self.api_url + method, params)
        return resp.json()

    def send_photo(self, chat_id, photo_path, caption=''):
        method = 'sendPhoto'
        params = {'chat_id': chat_id, 'caption': caption}
        files = {'photo': open(photo_path, 'rb')}
        resp = requests.post(self.api_url + method, params, files=files)
        return resp.json()


    def get_file(self, file_id):
        method = 'getFile'
        params = {'file_id': file_id}
        resp = requests.post(self.api_url + method, params)
        return resp.json()

    def download(self, file_path, name):
        resp = requests.get(self.api_file_url + file_path)
        with open(name, 'wb') as f:
            f.write(resp.content)
        return resp.status_code


    def get_last_update(self):
        get_result = self.get_updates()
        if get_result is not None and len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update
