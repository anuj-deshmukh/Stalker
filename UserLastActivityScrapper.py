import requests
import re
from UserUrlGenerator import UserUrlGenerator
from bs4 import BeautifulSoup


class UserLastActivityScrapper(UserUrlGenerator):
    last_submissionid_codeforces = str()
    last_problem_codeforces = str()
    last_submissionid_codechef = str()
    last_problem_codechef = str()

    def __init__(self, name, handle_cf, handle_cc) -> None:
        super().__init__(name, handle_cf, handle_cc)

        self.fetch_last_codeforces()
        self.fetch_last_codechef()
        # put all of this info in db

    def fetch_last_codeforces(self) -> None:
        print(self.name, 'fetch_last_codeforces()')
        soup_cf = self.fetch_soup_codeforces()
        try:
            # <a class="view-source" title="Source" href="/contest/1038/submission/159141124" submissionId="159141124">159141124</a>
            self.last_submissionid_codeforces = soup_cf.find(
                'a', class_="view-source", title="Source").string
            if len(self.last_submissionid_codeforces) == 0:
                raise Exception
        except:
            # <span class="submissionVerdictWrapper" submissionId="159141124"
            # submissionVerdict="OK" contestType="CF" partyMemberIds=";1712487;">
            # <span class='verdict-accepted'>Accepted</span></span><!---->
            self.last_submissionid_codeforces = soup_cf.find(
                'span', class_="submissionVerdictWrapper")['submissionid']

        # <a href="/contest/1038/problem/A">
        #         A - Equality
        #     </a>
        self.last_problem_codeforces = soup_cf.find(
            'a', href=re.compile('/contest/[0-9]+/problem/.*')).string.strip()

    def fetch_last_codechef(self) -> str():
        print(self.name, 'fetch_last_codechef()')
        soup_cc = self.fetch_soup_codechef()

        # <a  class = 'centered' href='\/viewsolution\/65960119' target='_blank'>View<\/a>
        self.last_submissionid_codechef = soup_cc.find(
            'a', href=re.compile('.*/viewsolution.*/[0-9]+'))['href'][16:]

        # <a href='\/problems\/SST' title='' target='_blank'>SST<\/a>
        self.last_problem_codechef = soup_cc.find(
            'a', href=re.compile('.+problem.+'))['href'][12:]
