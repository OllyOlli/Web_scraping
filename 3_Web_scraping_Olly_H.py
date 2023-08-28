"""Závěrečný projekt prověří tvé znalosti nejenom z posledních lekcí, ale z celého kurzu. Tvým úkolem bude vytvořit scraper výsledků voleb z roku 2017, který vytáhne data přímo z webu.
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


import sys
import requests as r
from bs4 import BeautifulSoup
import pandas as pd
from typing import List
import csv

#passing arguments to variables and checking the entry
arg1 = (sys.argv[1])
arg2 = (sys.argv[2])
if len(sys.argv) != 3 or arg2.split('.')[1] != 'csv' or r.get(arg1).status_code != 200:
    raise ValueError('Enter the parameter url and the title of csv. Do not exceed or exchange the parameters.')
else:
    #getting content from html based on argv
    response = r.get(arg1)
    soup = BeautifulSoup(response.text, 'html.parser')
    #getting the codes of cities from html
    numbers = soup.select('td.cislo')
    numbers_city = [number.find('a').text for number in numbers]
    #getting the url for detailed info for each city
    hrefs = soup.select('td.cislo')
    hrefs_city = [href.find('a')['href'] for href in hrefs]
    #getting the cities from html
    titles = soup.select('td.overflow_name')
    titles_city = []
    for title in titles:
        city = [ele.text.strip() for ele in title]
        titles_city.append([ele for ele in title if ele])

    #creating empty lists for further use
    df = []
    votes_by_party = []
    #iterating trought every city, code of city and link to detail of url for each city
    for href, title, number in zip(hrefs_city, titles_city, numbers_city):
        #getting content from the web for each city
        response2 = r.get(f"https://volby.cz/pls/ps2017nss/{href}")
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        #picking up information about number of electors, envelopes, valid votes and political party
        electors = soup2.select('td.cislo')[3].text
        envelopes = soup2.select('td.cislo')[4].text
        valid_votes = soup2.select('td.cislo')[7].text

        parties = soup2.select('td.overflow_name')
        parties_city = []
        for party in parties:
            party_pol = [ele.text.strip() for ele in party]
            parties_city.append([ele for ele in party if ele])
        l =(int(len(parties_city)))*3+10
        #picking up all of the votes in the city detail
        for i in list(range(10, l, 3)):
            votes_by_party.append(soup2.select('td.cislo')[i].text)

        #passing the information to dictionary
        df_detail = {
            'Number': number,
            'City': title,
            'Electors': electors,
            'Envelopes': envelopes,
            'Valid votes': valid_votes
        }
        df.append(df_detail)
        #converting the dictionary into dataframe
        df_1 = pd.DataFrame(df)

    #selecting unique political parties
    parties_unique = soup2.select('td.overflow_name')
    parties_city_unique = []
    for party_un in parties_unique:
        party_pol = [ele.text.strip() for ele in party_un]
        parties_city_unique.append([ele for ele in party_un if ele])
    w = pd.DataFrame(parties_city_unique)


    #creating a dictionary for political parties
    dict_temp = dict.fromkeys(list(range(0,len(w))))
    print(dict_temp)
    n = 0

    #passing all the votes by parti to the dictionary columns
    for i in list(range(0, len(titles_city))):
        c = len(w)
        dict_temp[i] = votes_by_party[n:n+c]
        n += c
        df_temp = pd.DataFrame(dict_temp)
        #transform columns vs rows
        df_temp = df_temp.T

    #changing the column names to political parties
    df_1 = df_1.join(df_temp)
    for i in range(0, len(parties_city)):
        df_1 = df_1.rename(columns={
            i: w.iloc[i][0]
       })

    #save to csv
    df_1.to_csv(arg2, index=False, encoding='utf-8')
    print(df_1)