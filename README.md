# Scraper volebních výsledků

Tento skript je navržen pro získávání volebních výsledků pro jednotlivé obce z oficiální české volební stránky [volby.cz](https://www.volby.cz). Skript načítá data jako počet registrovaných voličů, přijaté obálky, platné hlasy a hlasy pro jednotlivé strany v různých obcích a ukládá je do CSV souboru.

---

## 📌 Funkce

- Scrape dat z webu volby.cz
- Získání údajů o jednotlivých obcích:
  - registrovaní voliči
  - přijaté obálky
  - platné hlasy
- Získání počtu hlasů pro jednotlivé strany
- Uložení výsledků do CSV souboru s UTF-8 BOM (kompatibilní s MS Excel)
- Snadná konfigurace pro zvolený region pomocí URL

---

## ✅ Požadavky

- Python 3.7 nebo novější
- Potřebné knihovny uvedeny v `requirements.txt`

---

## 📦 Instalace knihoven

**1. Vytvořte a aktivujte virtuální prostředí (doporučeno):**

### Windows
```bash
python -m venv venv
venv\Scripts\activate
````

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

**2. Nainstalujte knihovny:**

```bash
pip install -r requirements.txt
```


## 🚀 Jak používat

1. Stáhněte nebo naklonujte repozitář
2. Spusťte skript s následující syntaxí:

```bash
python main.py <URL_regionu> <vystupni_soubor.csv>
```

### Příklad:

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "results_prostejov.csv"
```

---

## 🧾 Argumenty

* `<URL>`: URL stránky regionu z volby.cz (např. začínající `https://www.volby.cz/pls/ps2017nss/`)
* `<output.csv>`: Název výstupního CSV souboru

---

## 📊 Výstupní formát CSV

| code   | location | registered | envelopes | valid | party\_1\_name | party\_1\_votes | party\_2\_name | party\_2\_votes | ... |
| ------ | -------- | ---------- | --------- | ----- | -------------- | --------------- | -------------- | --------------- | --- |
| 123456 | Obec 1   | 10000      | 9000      | 8800  | Strana A       | 4000            | Strana B       | 3000            | ... |
| 123457 | Obec 2   | 15000      | 13000     | 12000 | Strana A       | 7000            | Strana B       | 5000            | ... |

**Popis sloupců:**

* `code`: Kód obce
* `location`: Název obce
* `registered`: Počet registrovaných voličů
* `envelopes`: Počet přijatých obálek
* `valid`: Počet platných hlasů
* `party_x_name`: Název politické strany
* `party_x_votes`: Počet hlasů pro danou stranu

---

## 🧠 Přehled funkcí ve skriptu

* `save_csv(filename, dataframe)`: Uložení dat do CSV souboru s UTF-8 BOM
* `load_page_content(url)`: Načte HTML z URL a zpracuje pomocí BeautifulSoup
* `extract_city_list(html_soup)`: Získá seznam obcí (kód, název, URL)
* `get_cell_value(header_id, html_soup)`: Získá hodnotu z tabulky podle ID
* `extract_city_results(city_url)`: Získá podrobnosti pro jednotlivou obec
* `main(region_url, output_filename)`: Koordinuje celý proces scrapování a ukládání

---

## ⚠️ Ošetření chyb

Skript zahrnuje ošetření běžných chyb:

* Chybné nebo nedostupné HTTP požadavky
* Neexistující nebo špatně formátovaná data
* Neplatné vstupní argumenty (např. chybějící URL nebo výstupní CSV soubor)

---

## 📝 Poznámky

* Skript používá omezení rychlosti (`time.sleep(0.5)`) pro šetrnost vůči serveru a hlavičku (simuluje skutečný OS a prohlížeč - bez tohoto nastavení server občas neodpověděl)
* Pokud pro obec nejsou dostupná data, skript ji přeskočí
* Výstupní CSV lze otevřít v Excelu nebo jiném tabulkovém editoru

---
