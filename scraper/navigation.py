from scraper.driver import Driver
from selenium.webdriver.common.by import By
import json
from time import sleep
import random
import pyotp


class Navigation:
    """This class implements all Navigation through the site"""

    def __init__(self):

        self.login_url = "https://www.upwork.com/ab/account-security/login"
        self.driver = Driver().driver()
        self.landing_url = "https://www.upwork.com/nx/find-work/best-matches"
        self.contact_info_url = "https://www.upwork.com/freelancers/settings/contactInfo"

    def delay(self):
        sleep(random.randint(6, 10))

    def login(self):

        if not self.isLogged():

            # 3 attempts to login
            for _ in range(3):
                print("login attempted")
                self.driver.get(self.login_url)

                with open('.credentials.json') as json_file:
                    data = json.load(json_file)

                try:
                    self.delay()
                    # Login using email
                    self.driver.find_element(By.ID, "login_username").send_keys(data['login'])
                    self.delay()
                    self.driver.find_element(By.XPATH, """//*[@button-role="continue"]""").click()
                    self.delay()

                    # Input password section
                    self.driver.find_element(By.ID, "login_password").send_keys(data['password'])
                    self.delay()
                    self.driver.find_element(By.XPATH, """//*[@button-role="continue"]""").click()
                    self.delay()

                    #  We disabled this block for bobbybackupy account to use authenticator secret key
                    # # Input secret answer section
                    # self.driver.find_element(By.ID, "login_answer").send_keys(data['secret_answer'])
                    # self.delay()
                    # self.driver.find_element(By.XPATH, """//*[@button-role="continue"]""").click()
                    # self.delay()

                    # Input authenticator secret key

                    totp = pyotp.TOTP(data['auth_secret_key'])
                    self.delay()
                    print("Current OTP:", totp.now())
                    self.delay()
                    current_otp = totp.now()
                    self.delay()
                    self.driver.find_element(By.ID, "deviceAuthOtp_otp").send_keys(current_otp)
                    self.delay()
                    self.driver.find_element(By.XPATH, """//*[@button-role="continue"]""").click()
                    self.delay()

                    print('Account Login')

                    break

                except Exception as e:
                    print(e)
                    continue

        else:
            pass

    def isLogged(self):

        try:
            self.driver.find_element(By.XPATH,
                                     """//*[@id="layout"]/div[2]/div/div[7]/div[3]/div/fe-profile-completeness/div/div[1]/div[2]/h4""")
            return True
        except:
            return False

    def get_html(self, url):

        if self.driver.current_url != url:
            self.driver.get(url)
            sleep(2)

        return self.driver.page_source

    def get_xhr(self, url):

        self.driver.get(f'{url}')

        obj = json.loads(self.driver.find_element(By.TAG_NAME, 'pre').text)

        return obj

    def get_main_portal(self):

        entry_portal_html = self.get_html(url=self.landing_url)

        return entry_portal_html
