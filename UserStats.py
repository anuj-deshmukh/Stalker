import re
from bs4 import BeautifulSoup
import requests
import urllib.request, urllib.parse, urllib.error
from UserUrlGenerator import UserUrlGenerator


class UserStats(UserUrlGenerator):
    rating_codeforces = int()
    rating_max_codeforces = int()
    problems_codeforces = int()
    verdicts_codeforces = dict()
    accuracy_codeforces = int()
    problem_type_codeforces = dict()

    rating_codechef = int()
    rating_max_codechef = int()
    full_problems_codechef = int()
    partial_problems_codechef = int()
    verdicts_codechef = dict()
    accuracy_codechef = int()

    def __init__(self, name, handle_cf, handle_cc) -> None:
        super().__init__(name, handle_cf, handle_cc)
        self.fetch_stats_codeforces()
        self.fetch_stats_codechef()

    def fetch_stats_codeforces(self) -> None:
        req = requests.get(self.profile_url_codeforces)
        html = req.content
        soup = BeautifulSoup(html, 'lxml')

        # rating
        # <span style="font-weight:bold;" class="user-cyan">1533</span>
        try:
            self.rating_codeforces = soup.find(
                'span',
                style="font-weight:bold;",
                class_=re.compile("^user.*")).string.strip()
            self.rating_codeforces = int(self.rating_codeforces)
        except:
            self.rating_codeforces = 0
        print('Codeforces Rating:', self.rating_codeforces)

        # rating_max
        # <span class="smaller"> (max.
        #  <span style="font-weight:bold;" class="user-cyan">specialist, </span>
        #  <span style="font-weight:bold;" class="user-cyan">1586</span>)</span>
        try:
            self.rating_max_codeforces = soup.find_all(
                'span',
                style="font-weight:bold;",
                class_=re.compile("^user.*"))[-1].string.strip()
        except:
            self.rating_max_codeforces = 0
        print('Codeforces max:', self.rating_max_codeforces)

        #  problems solved
        # <div class="_UserActivityFrame_counterValue">818 problems</div>
        self.problems_codeforces = int(
            soup.find('div', class_="_UserActivityFrame_counterValue").string.
            strip().split()[0])
        print('Codeforces Problems:', self.problems_codeforces)

        page_url = self.activity_url_codeforces + '/page/1'
        req = requests.get(page_url)
        html = req.content
        soup = BeautifulSoup(html, 'lxml')
        # <span class="page-index" pageIndex="2"><a href="/submissions/tilwanil818/page/2">2</a></span>
        try:
            page_count = int(
                soup.find_all('span', class_="page-index")[-1]['pageindex'])
        except:
            page_count = 1
        print('Pages:', page_count)

        for page in range(1, page_count + 1):
            print('Page', page)
            page_url = self.activity_url_codeforces + f'/page/{page}'
            req = requests.get(page_url)
            html = req.content
            soup = BeautifulSoup(html, 'lxml')

            # verdicts
            # <span class="submissionVerdictWrapper" submissionid="173929438"
            # submissionverdict="OK" contesttype="ICPC" partymemberids=";1712487;">
            # <span class="verdict-accepted">Accepted</span></span>

            verdicts = soup.find_all('span', class_="submissionVerdictWrapper")
            for v in verdicts:
                verd = v['submissionverdict']
                self.verdicts_codeforces[verd] = self.verdicts_codeforces.get(
                    verd, 0) + 1

            # problem_type
            # <a href="/contest/1550/problem/C">
            #     C - Manhattan Subarrays
            # </a>
            problems = soup.find_all(
                'a', href=re.compile('/contest/[0-9]+/problem/'))
            problem = set()
            for p in problems:
                problem.add(p.string.strip())
            for prob in problem:
                self.problem_type_codeforces[
                    prob[0]] = self.problem_type_codeforces.get(prob[0], 0) + 1

        accpeted_ratio = (self.verdicts_codeforces.get('OK', 0) /
                          sum(self.verdicts_codeforces.values()))
        self.accuracy_codeforces = round(accpeted_ratio * 100, 2)

        print(f'Accuracy: {self.accuracy_codeforces}%')
        print(self.verdicts_codeforces, sep='\n')
        print(self.problem_type_codeforces)

    def fetch_stats_codechef(self) -> None:
        header = {
            'x-requested-with':
            'XMLHttpRequest',
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        }
        req = requests.get(self.profile_url_codechef, headers=header)
        html = req.content
        soup = BeautifulSoup(html, 'lxml')

        # rating
        # <div class="rating-number">3023</div>
        self.rating_codechef = soup.find(
            'div', class_="rating-number").string.strip()
        print('Codechef Rating:', self.rating_codechef)

        # rating_max
        # <small>(Highest Rating 3083)</small>
        rating_max = soup.find(
            'small', text=re.compile("(Highest Rating.*)")).string.split()[-1]
        self.rating_max_codechef = rating_max[:len(rating_max) - 1]
        print('Codechef Rating Max:', self.rating_max_codechef)
