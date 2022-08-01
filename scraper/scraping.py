from typing import List
from bs4 import BeautifulSoup

from models.work import Work
from scraper.navigation import Navigation
import json
from time import time
from models.profile import Profile
import os


class Scraping:
    """This class implements reading data from html"""

    navigation = Navigation()
    navigation.login()

    print('API is Ready')

    def main_portal_reader(self):
        soup = BeautifulSoup(self.navigation.get_main_portal(), 'lxml')
        job_feed = soup.find('div', {'data-test': 'job-tile-list'})

        works: List[Work] = []

        for sec in job_feed.findAll('section'):
            title = sec.find('h4', {'class': 'job-tile-title'}).find('a').getText()
            url = f"https://upwork.com{sec.find('h4', {'class': 'job-tile-title'}).find('a')['href']}"
            description = sec.find('span', {'data-test': 'job-description-text'}).getText()
            tags = [tag.getText() for tag in
                    sec.find('div', {"class", "up-skill-wrapper"}).findAll('a', {'data-test': 'attr-item'})]
            location = sec.find('small', {"data-test": "client-country"}).find('strong').getText()
            client_spendings = sec.find('small', {"data-test": "client-spendings"}).find('strong').getText()
            payment_status = sec.find('small', {"data-test": "payment-verification-status"}).find('strong').getText()
            rating = sec.find('div', {"class": "up-rating-background"}).find("span", {"class": "sr-only"}).getText()
            job_type = sec.find('strong', {'data-test': 'job-type'}).getText()
            tier = sec.find('span', {"data-test": "contractor-tier"}).getText()
            date = sec.find('span', {'data-test': 'posted-on'}).getText()

            work = Work(
                title=title,
                url=url,
                description=description,
                tags=tags,
                location=location,
                client_spendings=client_spendings,
                payment_status=payment_status,
                rating=rating,
                job_type=job_type,
                tier=tier,
                date=date
            )

            works.append(work)

        return works

    def save_to_json(self, obj, path: str):
        _, userId = self.get_profile_ids()

        file = f"output/{userId}-{path}-{int(time())}.json"

        os.makedirs(os.path.dirname(file), exist_ok=True)

        with open(file, 'w') as json_file:
            json.dump(obj, json_file, default=str)

        print(f'{str} saved to output file')

    def get_profile_ids(self):
        profile_info = self.navigation.get_xhr(
            'https://www.upwork.com/freelancers/api/v1/profile/me/fwh')
        cipherId = profile_info['identity']['ciphertext']
        userId = profile_info['identity']['userId']

        return cipherId, userId

    def get_profile_obj(self):
        cipherId, _ = self.get_profile_ids()

        url_api_profile = f'https://www.upwork.com/freelancers/api/v1/freelancer/profile/{cipherId}/details?viewMode=1'

        profile_obj = self.navigation.get_xhr(url=url_api_profile)

        return profile_obj

    def get_portal_content(self):
        works = self.main_portal_reader()
        works_obj = {'works': [work.dict() for work in works]}

        self.save_to_json(works_obj, path='jobfeed')

        return works_obj

    def get_profile_contact_info(self):
        contact_obj = self.navigation.get_xhr(
            'https://www.upwork.com/freelancers/settings/api/v1/contactInfo')

        return contact_obj

    def get_profile_content(self):
        profile_obj = self.get_profile_obj()
        contact_obj = self.get_profile_contact_info()

        address_data = {
            'line1': contact_obj['freelancer']['address']['street'],
            'line2': contact_obj['freelancer']['address']['additionalInfo'],
            'city': contact_obj['freelancer']['address']['city'],
            'state': contact_obj['freelancer']['address']['state'],
            'postal_code': contact_obj['freelancer']['address']['zip'],
            'country': contact_obj['freelancer']['address']['country']
        }

        profile_data = {
            'id': profile_obj['profile']['identity']['uid'],
            'account': contact_obj['freelancer']['nid'],
            'employer': profile_obj['profile']['employmentHistory'][0]['companyName'],
            'created_at': profile_obj['profile']['stats']['memberSince'],
            'first_name': contact_obj['freelancer']['firstName'],
            'last_name': contact_obj['freelancer']['lastName'],
            'full_name': profile_obj['profile']['profile']['name'],
            'email': contact_obj['freelancer']['email']['address'],
            'phone_number': contact_obj['freelancer']['phone'],
            'picture_url': profile_obj['profile']['profile']['portrait']['portrait'],
            'address': address_data,
        }

        profile = Profile(**profile_data)

        self.save_to_json(profile.dict(), path='profile')

        return profile.dict()
