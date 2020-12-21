from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from crawler.CrawledCourse import CrawledCourse
from config import download_directory, executable_path, moodle_home, username, password

class CourseFetcher:
    def get_courses(self):
        print("Starte Chrome-Instanz...")
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": download_directory, #Download-Speicherort
            "download.prompt_for_download": False,              #Speicherfenster deaktivieren
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })
        driver = webdriver.Chrome(options=chrome_options, executable_path=executable_path)
        #Login auf der Startseite
        print("Einloggen...")
        url = moodle_home
        driver.get(url)

        elements = driver.find_elements_by_css_selector("#username")
        username_field = elements[0]
        elements = driver.find_elements_by_css_selector("#password")
        password_field = elements[0]
        elements = driver.find_elements_by_css_selector("#loginbtn")
        submit = elements[0]

        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        submit.click()

        #Kursliste ausgeben
        print("Kurse sammeln...")
        courses = []
        count = 0
        for course in driver.find_elements_by_css_selector(".coursebox"):
            if course.text != "":
                title = course.text
                url = course.find_element_by_css_selector("a").get_attribute("href")
                item = CrawledCourse(title, url)
                courses.append(item)
                print(str(count) +": " + course.text.strip())
                #print(course.find_element_by_css_selector("a").get_attribute("href"))
                count += 1

        course_number = int(input("Kursnummer auswählen: "))

        #Ausgewählten Kurs aufrufen
        print("Kurs aufrufen...")
        driver.get(courses[course_number].url)

        folders = []
        for folder in driver.find_elements_by_css_selector(".modtype_folder"):
            link = folder.find_element_by_css_selector(".aalink").get_attribute("href")
            folders.append(link)

        if len(folders) >= 1:
            download_folders = input(("Ordner gefunden! Alle Ordner einzeln als zip herunterladen? (Ja/Nein): "))

        #Alle Einträge, die als Resource gekennzeichnet sind herunterladen
        print("Lade Dateien herunter...")
        for resource in driver.find_elements_by_css_selector(".modtype_resource"):
            link = resource.find_element_by_css_selector(".aalink")
            link.click()

        #Ordner herunterladen
        if download_folders == "Ja" or download_folders == "ja":
            print("Lade Ordner herunter...")
            for link in folders:
                driver.get(link)
                driver.find_element_by_css_selector(".btn-secondary").click()

        input("Alle Dateien heruntergeladen. Beliebeige Taste drücken zum beenden.")





