# author Ricardo Pereira

from sys import platform
import random
import pip
from os import name, system

try:
    import selenium
except ModuleNotFoundError:
    pip.main(['install', 'selenium'])
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import text

if platform == 'win32':
    path = './chromedriver.exe'
elif platform == 'linux' or platform == 'linux2':
    path = './chromedriver_l'
else:
    path = './chromedriver_m'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument('log-level=3')
anime_options = webdriver.ChromeOptions()
anime_options.add_argument('log-level=3')
try:
    drive = webdriver.Chrome(executable_path=path, options=options)
except selenium.common.exceptions.SessionNotCreatedException:
    print("Please, update your Google Chrome first...")
else:
    anime_driver = webdriver.Chrome(executable_path='chromedriver.exe', options=anime_options)

    genres = {
        "action": 1,
        "adventure": 2,
        "comedy": 4,
        "dementia": 5,
        "demons": 6,
        "drama": 8,
        "ecchi": 9,
        "fantasy": 10,
        "horror": 14,
        "josei": 43,
        "kids": 15,
        "mecha": 18,
        "music": 19,
        "mystery": 7,
        "psychological": 40,
        "romance": 22,
        "sci-fi": 24,
        "seinen": 42,
        "shoujo": 25,
        "shounen": 27,
        "slice of life": 36,
        "sports": 30
    }

    links = {}
    animes = []


    def clear():
        if name == "nt":
            system('cls')
        else:
            system('clear')


    def setup_links():
        counter = 1
        for genre in genres:
            links[
                counter] = f"https://myanimelist.net/anime.php?cat=0&q=&type=0&score=6&status=0&p=0&r=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c[0]=a&c[1]=b&c[2]=c&c[3]=f&gx=0&genre[0]={genres[genre]}&o=3&w=1"
            counter += 1


    def start():
        print(text.START + "\n\nChoose the genre: ")
        counter = 1
        for genre in genres:
            print(f'{counter}) {genre}')
            counter += 1


    def choose_genre():
        chosen_genre = input("\nChoose your genre: ")
        try:
            link = links[int(chosen_genre)]
        except:
            print("No such genre!!! (╥﹏╥)")
            choose_genre()
        else:
            drive.get(link)


    def accept_cookies():
        accept_button = WebDriverWait(drive, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]')))
        accept_button.click()
        ok_button = WebDriverWait(drive, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="gdpr-modal-bottom"]/div/div/div[2]/button')))
        ok_button.click()


    def anime_titles():
        counter = 1
        current_page = 1
        current_score = 2
        print("Please wait a moment I'm collecting your animes ٩(◕‿◕｡)۶...")
        while True:
            titles = drive.find_elements_by_class_name('hoverinfo_trigger')
            for title in titles:
                if title.text != '':
                    score = drive.find_element_by_xpath(
                        f'//*[@id="content"]/div[6]/table/tbody/tr[{current_score}]/td[5]')
                    animes.append(f'{title.text}    {score.text}')
                    current_score += 1
            current_score = 2
            try:
                next_page = drive.find_element_by_xpath(
                    f'//*[@id="content"]/div[6]/div/div/span/a[{counter}]').get_attribute('href')
                drive.get(next_page)
                current_page += 1
                if current_page < 5:
                    counter += 1
                elif current_page == 40:
                    counter += 1
            except selenium.common.exceptions.NoSuchElementException:
                break


    def repeat_search():
        animes.clear()
        clear()
        start()
        choose_genre()
        anime_titles()
        choose_type_of_search()
        response = y_n_verification('Do you still want to do anything?[Y/N] ')
        if response:
            repeat_search()
        else:
            print('Bye Bye!!! ٩(◕‿◕｡)۶')
            clear()


    def open_anime_search(anime_name):
        anime_driver.get(f'https://www.anitube.biz/?s={anime_name.split("    ")[0]}')


    def y_n_verification(message):
        answer = input(message)
        while answer != 'y' and answer != 'n':
            print('Invalid answer (╥﹏╥)')
            answer = input(message).lower()
        if answer == 'y':
            return True
        else:
            return False


    def random_anime():
        anime = random.choice(animes)
        answer1 = y_n_verification(f"Do you want to watch {anime}?[Y/N]")
        if not answer1:
            print('Oh crap lemme try again... (╥﹏╥)')
            random_anime()
        else:
            open_anime_search(anime)
            answer2 = y_n_verification(f"Were you able to watch {anime}?[Y/N] ")
            if answer2:
                print('Nice ٩(◕‿◕｡)۶')
            else:
                print('Oh crap lemme try again... (╥﹏╥)')
                random_anime()


    def top10():
        for position in range(0, 10):
            print(f'{position + 1}) {animes[position]}')


    def top100():
        for position in range(0, 100):
            print(f'{position + 1}) {animes[position]}')


    def choose_type_of_search():
        clear()
        try:
            type = input(text.SEARCH_MODE + "\n> ")
            search_types[int(type)]()
        except:
            print('No such option (╥﹏╥)')
            choose_type_of_search()


    search_types = {
        1: random_anime,
        2: top10,
        3: top100
    }


    def main():
        setup_links()
        start()
        choose_genre()
        accept_cookies()
        anime_titles()
        choose_type_of_search()
        response = y_n_verification('Do you still want to do anything?[Y/N] ')
        if response:
            repeat_search()
        else:
            print('Bye Bye!!! ٩(◕‿◕｡)۶')
            clear()


    if __name__ == '__main__':
        main()
