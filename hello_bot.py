import requests


class HelloBot:
    def __init__(self, name):
        self.name = name

    def print_hello_message(self):
        print(f"Hello {self.name}!")

    @staticmethod
    def is_url_reachable(url):
        response = requests.get(url)
        return response.ok
