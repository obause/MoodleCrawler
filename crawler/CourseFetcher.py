import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .CrawledCourse import CrawledCourse

class CourseFetcher:
    def get_courses(self, name):
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": "E:\\Daten\\Crawler", #Download-Speicherort
            "download.prompt_for_download": False,              #Speicherfenster deaktivieren
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })
        driver = webdriver.Chrome(options=chrome_options,
                                  executable_path="E:\Programmieren\Python\PycharmProjects\MoodleCrawler\chromedriver.exe")
        #Login auf der Startseite
        url = "https://moodle.hs-hannover.de/login"
        driver.get(url)

        elements = driver.find_elements_by_css_selector("#username")
        username = elements[0]
        elements = driver.find_elements_by_css_selector("#password")
        password = elements[0]
        elements = driver.find_elements_by_css_selector("#loginbtn")
        submit = elements[0]

        username.clear()
        user_name = "hk7-bdq-u1"
        username.send_keys(user_name)
        password.clear()
        password.send_keys("Ruamzuzla9078#")
        submit.click()

        #Kurs auswählen
        for course in driver.find_elements_by_css_selector(".coursebox"):
            print(course.text)
            if course.text == name:
                course.click()
                break

        #Alle Einträge, die als Resource gekennzeichnet sind herunterladen f
        for resource in driver.find_elements_by_css_selector(".modtype_resource"):
            link = resource.find_element_by_css_selector(".aalink")
            link.click()

        time.sleep(2)





