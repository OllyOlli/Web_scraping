# Election Scraper

Tento projekt slouží k extrahování výsledků z parlamentních voleb 2017.

Odkaz zde - https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103

## Instalace knihoven

Knihovny, které jsou použity v kódu jsou uložené v souboru ```requirements.txt```. 
Pro instalaci doporučuji použít nové virtuální prostředí a nainstalovaným manažerem spustit následovné:

$ pip3 -- version                       # overim verzi manazera
$ pip3 install -r requirements.txt      # nainstalujeme knihovny


## Souštění projektu

Spuštění souboru ```main.py``` v rámci příkazového řádku požaduje dva povinné argumenty.

python .\election_scraper.py <argument_1> <argument_2>

argument_1 = URL link to webpage.  
argument_2 = name of the CSV file to save collected data. 

Následně se vám stáhnou výsledky, jako soubor s příponou ```.csv```.


## Ukázka projektu

Výsledky hlasování pro okres XXX:

1. argument: ```https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8101``` 
2. argument: ```vysledky_bruntal.csv```

Spouštění programu:

```python main.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8101' vysledky_bruntal.csv```

Stahuji data z URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3203 .
Ukladam data do souboru...
Ukončuji Web Scraper.

## Data uložena do výsledného souboru:

Cislo obce,Nazev obec,Volici v seznamu,Vydane obalky,Volebni ucast v %,Odevzdane obalky,Platne hlasy,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Radostné Česko,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,Česká pirátská strana,OBČANÉ 2011-SPRAVEDL. PRO LIDI,Referendum o Evropské unii,TOP 09,ANO 2011,SPR-Republ.str.Čsl. M.Sládka,Křesť.demokr.unie-Čs.str.lid.,Česká strana národně sociální,REALISTÉ,SPORTOVCI,Dělnic.str.sociální spravedl.,Svob.a př.dem.-T.Okamura (SPD),Strana Práv Občanů,-
558851,Dýšina,1349,860,"63,75",858,853,114,0,0,48,0,52,41,10,5,16,1,2,119,0,3,45,269,5,34,0,3,2,1,80,3,-
558966,Chrást,1429,1002,"70,12",1002,999,151,1,1,51,1,31,63,8,4,15,1,2,111,1,1,45,354,1,24,0,11,5,2,114,1,-

