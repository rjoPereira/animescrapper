#author Ricardo Pereira
from time import sleep

import selenium
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import text

path = './chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument('log-level=3')
drive = webdriver.Chrome(executable_path=path, options=options)

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

def setup_links():
    counter = 1
    for genre in genres:
        links[counter] = f"https://myanimelist.net/anime.php?cat=0&q=&type=0&score=6&status=0&p=0&r=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c[0]=a&c[1]=b&c[2]=c&c[3]=f&gx=0&genre[0]={genres[genre]}&o=3&w=1"
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
    accept_button = WebDriverWait(drive, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]')))
    accept_button.click()
    ok_button = WebDriverWait(drive, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gdpr-modal-bottom"]/div/div/div[2]/button')))
    ok_button.click()


def anime_titles():
    counter = 1
    current_page = 1
    print("Please wait a moment I'm collecting your animes ٩(◕‿◕｡)۶...")
    while True:
        titles = drive.find_elements_by_class_name('hoverinfo_trigger')
        for title in titles:
            if title.text != '':
                animes.append(title.text)
        try:
            next_page = drive.find_element_by_xpath(f'//*[@id="content"]/div[6]/div/div/span/a[{counter}]').get_attribute('href')
            drive.get(next_page)
            current_page += 1
            if current_page < 5:
                counter += 1
            elif current_page == 40:
                counter += 1
        except selenium.common.exceptions.NoSuchElementException:
            break

def open_anime_search(anime_name):
    anime_options = webdriver.ChromeOptions()
    anime_options.add_argument('log-level=3')
    anime_driver = webdriver.Chrome(executable_path='chromedriver.exe', options=anime_options)
    anime_driver.get(f'https://www.anitube.biz/?s={anime_name}')

def random_anime():
    anime = random.choice(animes)
    answer = input(f"Do you want to watch {anime}?[Y/N] ").lower()
    while answer != 'y' and answer != 'n':
        print('Invalid answer (╥﹏╥)')
        answer = input(f"Do you want to watch {anime}?[Y/N] ").lower()
    if answer == 'y':
        open_anime_search(anime)
        answer = input(f"Were you able to watch {anime}?[Y/N] ").lower()
        while answer != 'y' and answer != 'n':
            print('Invalid answer (╥﹏╥)')
            answer = input(f"Do you want to find {anime}?[Y/N] ").lower()
        if answer == 'y':
            print('Nice ٩(◕‿◕｡)۶')
        else:
            print('Oh crap lemme try again... (╥﹏╥)')
            random_anime()
    else:
        random_anime(anime)


def top10():
    for position in range(0, 10):
        print(f'{position+1}) {animes[position]}')


def top100():
    for position in range(0, 100):
        print(f'{position+1}) {animes[position]}')

def choose_type_of_search():
    try:
        type = input(text.SEARCH_MODE + "\n> ")
    except:
        print('No such option (╥﹏╥)')
        choose_type_of_search()
    search_types[int(type)]()


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
    print('Press Ctrl-C to quit...')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Bye Bye!!!! ٩(◕‿◕｡)۶')


if __name__ == '__main__':
    main()
