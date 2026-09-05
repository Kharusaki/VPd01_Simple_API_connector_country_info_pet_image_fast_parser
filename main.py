import os

import requests
from colorama import Fore, Style, init
from dotenv import load_dotenv

import http_client
from country_info import print_country_info
from country_info_alt import print_country_info_alt

init(autoreset=True)

load_dotenv()

API_TOKEN = os.getenv("RESTCOUNTRIES_API_KEY", "rc_live_demo")


def make_get_request(url: str) -> None:
    response = http_client.get(url)
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Body: {response.text}")


def make_dog_request() -> None:
    response = http_client.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    print(f"Случайная собака: {data.get('message')}")


def make_get_country_request(country: str) -> None:
    print_country_info(country)


FIELDS = ["name", "capital", "population"]


def make_countries_dev_field_request(country: str, fields: list[str] | None = None) -> None:
    fields = fields or FIELDS
    response = http_client.get(f"https://countries.dev/name/{country}")
    data = response.json()[0] if isinstance(response.json(), list) else response.json()
    for field in fields:
        print(f"{field}: {data.get(field)}")

MFIELDS = ["name", "flags", "region", "subregion", "demonym", "capital", "independent"]

def make_manual(country: str, fields: list[str] | None = None) -> None:
    mfields = fields or MFIELDS
    response = http_client.get(f"https://countries.dev/name/{country}")
    data = response.json()[0] if isinstance(response.json(), list) else response.json()
    for field in mfields:
        print(f"{field}: {data.get(field)}")

def main() -> None:
    while True:
        print("Выберите тип запроса:")
        print("1 - Выполнить простой GET-запрос по любому сайту")
        print("2 - Выполнить поиск случайной собаки")
        print("3 - Выполнить GET-запрос по стране (запрос по https://restcountries.com)")
        print("4 - Выполнить GET-запрос по альтернативному API для данных по странам (напр. https://countries.dev)")
        print("5 - Выполнить выборочный запрос по ключевым полям (countries.dev)")
        print("6 - Тестовый запрос human (countries.dev)")
        print("7 - Выйти")

        choice = input("Ваш выбор: ")

        if choice == "1":
            url = input("Введите URL: ")
            make_get_request(url)

        elif choice == "2":
            make_dog_request()

        elif choice == "3":
            country = input("Введите страну: ")
            print_country_info(country)

        elif choice == "4":
            country = input("Введите страну (альтернативный API): ")
            try:
                print_country_info_alt(country)
            except (requests.exceptions.RequestException, ValueError) as exc:
                print(Fore.RED + str(exc))

        elif choice == "5":
            country = input("Введите страну (выборка ключевых полей): ")
            make_countries_dev_field_request(country)

        elif choice == "6":
            country = input("Введите страну (для https://countries.dev/explore): ")
            make_manual(country)


        elif choice == "7":
            print("До свидания!")
            break

        else:
            print("Неверный выбор")
        print()


if __name__ == "__main__":
    main()