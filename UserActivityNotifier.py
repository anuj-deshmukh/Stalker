import requests
import re
from UserLastActivityScrapper import UserLastActivityScrapper
from bs4 import BeautifulSoup
from plyer import notification


class UserActivityNotifier(UserLastActivityScrapper):

    def __init__(self, name, handle_cf, handle_cc) -> None:
        super().__init__(name, handle_cf, handle_cc)

        self.new_submissionid_codeforces = self.last_submissionid_codeforces
        self.new_submissionid_codechef = self.last_submissionid_codechef

    def notify(self, handle, problem):
        print(self.name, 'notify()')
        notification.notify(
            title=handle + ' has submitted a problem',
            message=problem,
            app_name='Stalker',
            app_icon='D:\\Academics\\Projects\\Stalker\\icon.ico',
            timeout=5)

    def check_new_codeforces(self):
        print(self.name, 'check_new_codeforces()')
        soup_cf = self.fetch_soup_codeforces()

        try:
            # <a class="view-source" title="Source" href="/contest/1038/submission/159141124" submissionId="159141124">159141124</a>
            new_submissionid_codeforces = soup_cf.find('a',
                                                       class_="view-source",
                                                       title="Source").string
            if len(new_submissionid_codeforces) == 0:
                raise Exception
        except:
            # <span class="submissionVerdictWrapper" submissionId="159141124"
            # submissionVerdict="OK" contestType="CF" partyMemberIds=";1712487;">
            # <span class='verdict-accepted'>Accepted</span></span><!---->
            new_submissionid_codeforces = soup_cf.find(
                'span', class_="submissionVerdictWrapper")['submissionid']

        # <a href="/contest/1038/problem/A">
        #         A - Equality
        #     </a>
        new_problem_codeforces = soup_cf.find(
            'a', href=re.compile('/contest/[0-9]+/problem/.*')).string.strip()

        if new_submissionid_codeforces != self.last_submissionid_codeforces:
            self.last_submissionid_codeforces = new_submissionid_codeforces
            self.last_problem_codeforces = new_problem_codeforces
            self.notify(self.handle_codeforces, new_problem_codeforces)

    def check_new_codechef(self) -> str():
        print(self.name, 'check_new_codechef()')
        soup_cc = self.fetch_soup_codechef()

        # <a  class = 'centered' href='\/viewsolution\/65960119' target='_blank'>View<\/a>
        new_submissionid_codechef = soup_cc.find(
            'a', href=re.compile('.*/viewsolution.*/[0-9]+'))['href'][16:]

        # <a href='\/problems\/SST' title='' target='_blank'>SST<\/a>
        new_problem_codechef = soup_cc.find(
            'a', href=re.compile('.+problem.+'))['href'][12:]

        if new_submissionid_codechef != self.last_submissionid_codechef:
            self.last_submissionid_codechef = new_submissionid_codechef
            self.last_problem_codechef = new_problem_codechef
            self.notify(self.handle_codechef, new_problem_codechef)
