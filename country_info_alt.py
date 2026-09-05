import requests
from colorama import Fore, Style, init

init(autoreset=True)

BASE_URL = "https://countries.dev"


def _get_country_data(country: str) -> dict:
    url = f"{BASE_URL}/name/{country}"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    if isinstance(data, list) and data:
        return data[0]
    if isinstance(data, dict):
        return data
    raise ValueError(f"Страна '{country}' не найдена")


def _print_field(label: str, value) -> None:
    print(f"{Fore.CYAN}{label}: {Style.RESET_ALL}{Fore.WHITE}{value}")


def print_country_info_alt(country: str) -> None:
    data = _get_country_data(country)

    print()
    print(Fore.GREEN + "=" * 60)
    print(Fore.GREEN + Style.BRIGHT + f"   🌍 {data.get('name', '—')} {data.get('flag', '')}")
    print(Fore.GREEN + "=" * 60)

    _print_field("Официальное название", data.get("nativeName", "—"))
    _print_field("Код страны (alpha-2)", data.get("alpha2Code", "—"))
    _print_field("Код страны (alpha-3)", data.get("alpha3Code", "—"))
    _print_field("Столица", data.get("capital", "—"))
    _print_field("Регион", data.get("region", "—"))
    _print_field("Субрегион", data.get("subregion", "—"))
    _print_field("Площадь (км²)", f"{data.get('area', '—'):,}")
    _print_field("Население", f"{data.get('population', '—'):,}")
    _print_field("Плотность населения", data.get("populationDensity", "—"))

    timezones = ", ".join(data.get("timezones", [])) or "—"
    _print_field("Часовые пояса", timezones)

    tlds = ", ".join(data.get("topLevelDomain", [])) or "—"
    _print_field("Доменные зоны", tlds)

    languages = data.get("languages", [])
    lang_names = ", ".join(l.get("name", "—") for l in languages) or "—"
    _print_field("Языки", lang_names)

    currencies = data.get("currencies", [])
    cur_names = ", ".join(
        f"{c.get('name', '—')} ({c.get('code', '—')})" for c in currencies
    ) or "—"
    _print_field("Валюта", cur_names)

    flags = data.get("flags", {})
    if flags.get("svg"):
        _print_field("Флаг (SVG)", flags["svg"])
    if flags.get("png"):
        _print_field("Флаг (PNG)", flags["png"])

    print(Fore.GREEN + "=" * 60)
    print()


def main() -> None:
    try:
        country = input("Введите название страны: ").strip()
        if not country:
            print(Fore.RED + "Вы ничего не ввели.")
            return
        print_country_info_alt(country)
    except requests.exceptions.RequestException as exc:
        print(Fore.RED + f"Ошибка запроса: {exc}")
    except (ValueError, KeyError) as exc:
        print(Fore.RED + f"Ошибка обработки данных: {exc}")


if __name__ == "__main__":
    main()
