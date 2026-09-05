import json
import os

import requests
from colorama import Fore, Style, init
from dotenv import load_dotenv

load_dotenv()

init(autoreset=True)

API_TOKEN = os.getenv("RESTCOUNTRIES_API_KEY", "rc_live_demo")
BASE_URL = "https://api.restcountries.com/countries/v5"


def _get_country_data(country: str) -> dict | None:
    url = f"{BASE_URL}?q={country}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as exc:
        print(exc)
        return None

    if response.status_code != 200:
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")
        return None

    payload = response.json()
    objects = payload.get("data", {}).get("objects", [])
    if not objects:
        print(f"Страна '{country}' не найдена")
        return None

    if "_demo" in payload.get("data", {}):
        print(
            Fore.YELLOW
            + "(!) Внимание: ответ получен по демо-ключу, данные могут быть примером, "
            "а не реальной страной.\n"
        )
    return objects[0]


def _print_field(label: str, value) -> None:
    color = Fore.CYAN
    print(f"{color}{label}: {Style.RESET_ALL}{Fore.WHITE}{value}")


def print_country_info(country: str) -> None:
    data = _get_country_data(country)
    if data is None:
        return

    print()
    print(Fore.GREEN + "=" * 60)
    print(Fore.GREEN + Style.BRIGHT + f"   🌍 {data['names']['common']}")
    print(Fore.GREEN + "=" * 60)

    names = data["names"]
    _print_field("Официальное название", names.get("official", "—"))

    codes = data.get("codes", {})
    _print_field("Код страны (alpha-2)", codes.get("alpha_2", "—"))

    capitals = data.get("capitals", [])
    cap_names = ", ".join(c.get("name", "—") for c in capitals) if capitals else "—"
    _print_field("Столица", cap_names)

    _print_field("Регион", data.get("region", "—"))
    _print_field("Субрегион", data.get("subregion", "—"))

    area = data.get("area", {})
    _print_field("Площадь (км²)", f"{area.get('kilometers', '—'):,}")

    _print_field("Население", f"{data.get('population', '—'):,}")

    timezones = ", ".join(data.get("timezones", [])) or "—"
    _print_field("Часовые пояса", timezones)

    tlds = ", ".join(data.get("tlds", [])) or "—"
    _print_field("Доменные зоны", tlds)

    languages = data.get("languages", [])
    lang_names = ", ".join(l.get("name", "—") for l in languages) or "—"
    _print_field("Языки", lang_names)

    currencies = data.get("currencies", [])
    cur_names = ", ".join(
        f"{c.get('name', '—')} ({c.get('code', '—')})" for c in currencies
    ) or "—"
    _print_field("Валюта", cur_names)

    flag_svg = data.get("flag", {}).get("url_svg")
    if flag_svg:
        _print_field("Флаг (SVG)", flag_svg)

    print(Fore.GREEN + "=" * 60)
    print()


def main() -> None:
    try:
        country = input("Введите название страны: ").strip()
        if not country:
            print(Fore.RED + "Вы ничего не ввели.")
            return
        print_country_info(country)
    except requests.exceptions.RequestException as exc:
        print(Fore.RED + f"Ошибка запроса: {exc}")
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        print(Fore.RED + f"Ошибка обработки данных: {exc}")


if __name__ == "__main__":
    main()
