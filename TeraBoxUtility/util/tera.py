from time import sleep

import requests
import os
from selenium.webdriver.common.by import By
import TeraBoxUtility.common.constant as Constant
from TeraBoxUtility.util import helper
from TeraBoxUtility.util.profile import ChromeProfile
import zipfile
import shutil


class TeraBox:

    def __init__(self, emails):
        self.path = Constant.env["UPLOAD_PATH"]
        email = Constant.env["EMAIL"]
        email = email.split(':')
        profile = ChromeProfile(email[0], email[1], email[2])
        self.emails = emails
        self.copy_path = email[0]
        self.driver = profile.retrieve_driver()
        self.zip_path = self.path.split(".")[0] + '.zip'
        profile.start()
        self.login()
        self.cookie = self.get_cookie()
        self.download_path = Constant.env["DOWNLOAD_PATH"]

    def download(self):
        for email in self.emails:
            self.download_zip(email)
        sleep(int(Constant.env["TIME_DOWNLOAD"]))
        for email in self.emails:
            self.unzip_in_folder(email)
            helper.delete(Constant.env["DOWNLOAD_LOCATION"] + '\\' + email + '.zip')
            self.decrypt_in_folder(email)

    def login(self):
        self.driver.get("https://www.terabox.com/")
        if 'main' not in self.driver.current_url:
            login_xpath = "/html/body/div[1]/div/div[1]/div[4]/div/div[2]/div/div[2]/div/div[1]"
            self.driver.find_element(By.XPATH, login_xpath).click()
        else:
            pass
        sleep(Constant.WAIT_RELOAD)

    def get_cookie(self):
        self.driver.get(self.driver.current_url)
        cookie = self.driver.get_cookie('ndus')
        ndus = 'ndus=' + cookie.get('value')
        return ndus

    def upload(self):
        list_dir = os.listdir(self.path)
        for data in list_dir:
            if data in self.emails:
                dir_path = self.path + '\\' + data
                if os.path.isdir(dir_path):
                    zip_path = dir_path + '.zip'
                    copy_path = dir_path + '_copy'
                    self.zip_directory(dir_path)
                    helper.delete(copy_path)
                    self.call_create_api(zip_path, data)
                    helper.delete(zip_path)
                else:
                    pass

    def pre_upload(self, zip_path):
        url_upload = 'https://c-jp.terabox.com/rest/2.0/pcs/superfile2'
        params = {
            'method': 'upload',
            'app_id': 250528,
            'path': '/abc.txt',
            'uploadid': 'N1-MTQu',
            'partseq': 0
        }
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/105.0.0.0 Safari/537.36',
        }
        files = {'file': open(zip_path, 'rb')}
        try:
            response = requests.post(url=url_upload, params=params, headers=headers, files=files)
            result = response.json()["md5"]
            return result

        except requests.exceptions.HTTPError as err:
            print(err)

    def call_create_api(self, zip_path, email):
        path = zip_path
        size = os.stat(path=path).st_size
        file_name = os.path.basename(path).split('/')[-1]
        md5 = self.pre_upload(path)
        url = 'https://www.terabox.com/api/create'
        headers = {
            'Cookie': self.cookie,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'path': email + '/' + file_name,
            'size': size,
            'block_list': '["' + md5 + '"]'
        }

        requests.post(url=url, headers=headers, data=data)

    def zip_directory(self, dir_path):
        dir_copy = self.copy_directory(dir_path=dir_path)
        with zipfile.ZipFile(dir_path + '.zip', mode='w') as zipf:
            len_dir_path = len(dir_path)
            for root, _, files in os.walk(dir_copy):
                for file in files:
                    file_path = os.path.join(root, file)
                    helper.encrypt_file(file_path=file_path)
                    zipf.write(file_path, file_path[len_dir_path:])

    @staticmethod
    def copy_directory(dir_path):
        copy_path = dir_path + '_copy'
        shutil.copytree(dir_path, copy_path)
        return copy_path

    def download_zip(self, email):
        self.driver.get('https://www.terabox.com/main?category=all&path=%2F' + email)
        self.driver.find_element(By.CLASS_NAME, "u-checkbox").click()
        self.driver.find_element(By.CSS_SELECTOR, "body > div.main-page > div.box > div.view-container-box > "
                                                  "div.nd-main-list.hasAd > div.wp-s-core-pan > div > "
                                                  "div.wp-s-core-pan__header.is-show-header > div > "
                                                  "div.wp-s-core-pan__header-tool-bar--action > div > div > "
                                                  "div.wp-s-agile-tool-bar__h-group > "
                                                  "div > div:nth-child(4) > button").click()
        sleep(Constant.WAIT_DOWNLOAD)
        try:
            self.driver.find_element(By.CLASS_NAME, 'left-button').click()
            sleep(Constant.WAIT_DOWNLOAD)
        except:
            pass

    def unzip_in_folder(self, email):
        path_to_download_folder = Constant.env["DOWNLOAD_LOCATION"] + '\\' + email + '.zip'
        out_path = self.download_path
        helper.unzip(path_to_download_folder, out_path)
        os.chdir(out_path)
        os.rename('_copy', email)

    def decrypt_in_folder(self, email):
        out_path = self.download_path + email
        for root, _, files in os.walk(out_path):
            for file in files:
                file_path = os.path.join(root, file)
                helper.decrypt(file_path)

