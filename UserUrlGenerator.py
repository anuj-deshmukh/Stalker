import requests
from bs4 import BeautifulSoup


class UserUrlGenerator:
    name = str()
    handle_codeforces = str()
    profile_url_codeforces = str()
    activity_url_codeforces = str()
    handle_codechef = str()
    profile_url_codechef = str()
    activity_url_codechef = str()

    def __init__(self, name, handle_cf, handle_cc) -> None:
        self.name = name
        self.handle_codeforces = handle_cf
        self.profile_url_codeforces = 'https://codeforces.com/profile/' + self.handle_codeforces
        self.activity_url_codeforces = 'https://codeforces.com/submissions/' + self.handle_codeforces

        self.handle_codechef = handle_cc
        self.profile_url_codechef = 'https://www.codechef.com/users/' + self.handle_codechef
        self.activity_url_codechef = 'https://www.codechef.com/recent/user?page=undefined&user_handle=' + self.handle_codechef

    def fetch_soup_codeforces(self) -> BeautifulSoup():
        print(self.name, 'fetch_soup_codeforces()')
        try:
            req = requests.get(self.activity_url_codeforces)
            html = req.content
            soup = BeautifulSoup(html, 'lxml')
            return soup
        except Exception as ex:
            print(ex)

    def fetch_soup_codechef(self) -> BeautifulSoup():
        print(self.name, 'fetch_soup_codechef()')
        try:
            header = {
                'x-requested-with':
                'XMLHttpRequest',
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
            }
            req = requests.get(self.activity_url_codechef, headers=header)
            html = req.content
            soup = BeautifulSoup(html, 'lxml')
            return soup
        except Exception as ex:
            print(ex)