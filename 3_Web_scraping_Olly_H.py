"""Tvým úkolem bude vytvořit scraper výsledků voleb z roku 2017, který vytáhne data přímo z webu.
Napiš takový skript, který vybere jakýkoliv územní celek z tohoto odkazu Např. X u Benešov odkazuje sem . Z tohoto odkazu chcete vyscrapovat výsledky hlasování pro všechny obce (resp. pomocí X ve sloupci Výběr okrsku).
Jak postupovat
Na svém počítači si vytvoříte vlastní virtuální prostředí (speciálně pro tento úkol)
Do nově vytvořeného prostředí si přes IDE (nebo příkazový řádek) nainstalujete potřebné knihovny třetích stran
Vygenerujete soubor requirements.txt, který obsahuje soupis všech knihoven a jejich verzí (nevypisovat ručně!)
Výsledný soubor budete spouštět pomocí 2 argumentů (ne pomocí funkce input). První argument obsahuje odkaz, který územní celek chcete scrapovat (př. územní celek Prostějov ), druhý argument obsahuje jméno výstupního souboru (př. vysledky_prostejov.csv)
Pokud uživatel nezadá oba argumenty (ať už nesprávné pořadí, nebo argument, který neobsahuje správný odkaz), program jej upozorní a nepokračuje.
Následně dopište README.md soubor, který uživatele seznámíte se svým projektem. Jak nainstalovat potřebné knihovny ze souboru requirements.txt, jak spustit váš soubor, příp. doplnit ukázku, kde demonstrujete váš kód na konkrétním odkaze s konkrétním výpisem.
Projekt bude obsahovat
Soubor s programem (.py), který pro správný běh potřebuje 2 argumenty při spuštění
Soubor se seznamem knihoven a verzí (requirements.txt)
Stručnou dokumentaci (popis, instalace knihoven, ukázka) (README.md)
Soubor s uloženým výstupem (.csv)
Výstup bude obsahovat
Ve výstupu (soubor .csv) každý řádek obsahuje informace pro konkrétní obec. Tedy podobu:
kód obce
název obce
voliči v seznamu
vydané obálky
platné hlasy
kandidující strany
"""

import sys  # Importování modulu sys pro práci s argumenty příkazové řádky
import requests as r  # Importování modulu requests jako r pro získání webového obsahu
from bs4 import BeautifulSoup  # Importování modulu BeautifulSoup pro analýzu HTML
import pandas as pd  # Importování modulu pandas pro manipulaci s daty
from typing import List  # Importování typu List pro typovou kontrolu
import csv  # Importování modulu csv pro práci s CSV soubory

# Předání argumentů proměnným a kontrola vstupu
arg1 = (sys.argv[1])
arg2 = (sys.argv[2])
if len(sys.argv) != 3 or arg2.split('.')[1] != 'csv' or r.get(arg1).status_code != 200:
    raise ValueError('Zadejte parametr URL a název CSV. Nepřekračujte nebo nevyměňujte parametry.')
else:
    # Získání obsahu z HTML na základě argumentu
    response = r.get(arg1)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Získání kódů měst z HTML
    numbers = soup.select('td.cislo')
    numbers_city = [number.find('a').text for number in numbers]
    # Získání URL pro podrobnosti o každém městě
    hrefs = soup.select('td.cislo')
    hrefs_city = [href.find('a')['href'] for href in hrefs]
    # Získání měst z HTML
    titles = soup.select('td.overflow_name')
    titles_city = []
    for title in titles:
        city = [ele.text.strip() for ele in title]
        titles_city.append([ele for ele in title if ele])

    # Vytvoření prázdných seznamů pro další použití
    df = []
    votes_by_party = []
    # Procházení každého města, kódu města a odkazu na detail pro každé město
    for href, title, number in zip(hrefs_city, titles_city, numbers_city):
        # Získání obsahu z webu pro každé město
        response2 = r.get(f"https://volby.cz/pls/ps2017nss/{href}")
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        # Získání informací o počtu voličů, obálek, platných hlasů a politických stranách
        electors = soup2.select('td.cislo')[3].text
        envelopes = soup2.select('td.cislo')[4].text
        valid_votes = soup2.select('td.cislo')[7].text

        parties = soup2.select('td.overflow_name')
        parties_city = []
        for party in parties:
            party_pol = [ele.text.strip() for ele in party]
            parties_city.append([ele for ele in party if ele])
        l = (int(len(parties_city))) * 3 + 10
        # Získání všech hlasů v detailu města
        for i in list(range(10, l, 3)):
            votes_by_party.append(soup2.select('td.cislo')[i].text)

        # Předání informací do slovníku
        df_detail = {
            'Number': number,
            'City': title,
            'Electors': electors,
            'Envelopes': envelopes,
            'Valid votes': valid_votes
        }
        df.append(df_detail)
        # Převedení slovníku na dataframe
        df_1 = pd.DataFrame(df)

    # Výběr unikátních politických stran
    parties_unique = soup2.select('td.overflow_name')
    parties_city_unique = []
    for party_un in parties_unique:
        party_pol = [ele.text.strip() for ele in party_un]
        parties_city_unique.append([ele for ele in party_un if ele])
    w = pd.DataFrame(parties_city_unique)

    # Vytvoření slovníku pro politické strany
    dict_temp = dict.fromkeys(list(range(0, len(w))))
    print(dict_temp)
    n = 0

    # Předání všech hlasů podle stran do sloupců slovníku
    for i in list(range(0, len(titles_city))):
        c = len(w)
        dict_temp[i] = votes_by_party[n:n + c]
        n += c
        df_temp = pd.DataFrame(dict_temp)
        # Převod sloupců na řádky
        df_temp = df_temp.T

    # Změna názvů sloupců na politické strany
    df_1 = df_1.join(df_temp)
    for i in range(0, len(parties_city)):
        df_1 = df_1.rename(columns={
            i: w.iloc[i][0]
        })

    # Uložení do CSV
    df_1.to_csv(arg2, index=False, encoding='utf-8')
    print(df_1)
