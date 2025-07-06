"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Vladena Ceplechova
email: VladenaC@seznam.cz
"""
from io import StringIO
import re
import sys
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


def save_csv(filename, dataframe):
    """
    Save a DataFrame as a CSV file with UTF-8 BOM encoding (compatible with Excel).
    """
    dataframe.to_csv(filename, index=False, sep=";", encoding="utf-8-sig")
    print(f"✅ Data saved as CSV to: {filename}")


def load_page_content(url):
    """
    Load HTML content from the provided URL and parse it with BeautifulSoup and pandas.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to load URL: {url}\n   → {e}")
        return None, None

    html_soup = BeautifulSoup(response.text, features="html.parser")
    tables = pd.read_html(StringIO(response.text), header=0)
    return html_soup, tables


def extract_city_list(html_soup):
    """
    Extract a list of municipalities from the parsed region page.
    """
    city_data = []
    for row in html_soup.find_all("tr"):
        code_cell = row.find("td", class_="cislo")
        name_cell = row.find("td", class_="overflow_name")
        link_tag = code_cell.find("a") if code_cell else None

        if code_cell and name_cell and link_tag and link_tag.get("href"):
            city_data.append((
                code_cell.get_text(strip=True),
                name_cell.get_text(strip=True),
                f"https://www.volby.cz/pls/ps2017nss/{link_tag['href']}"
            ))
    return city_data


def get_cell_value(header_id, html_soup):
    """
    Extract text value from a table cell based on a given header ID.
    """
    cell = html_soup.find("td", {"headers": header_id})
    return cell.get_text(strip=True) if cell else None


def parse_int(value):
    if not value:
        return None
    cleaned = re.sub(r"\s+", "", value)  # odstraní všechny mezery, včetně \xa0
    try:
        return int(cleaned)
    except ValueError:
        return None


def extract_city_results(city_url):
    """
    Extract voting results for a specific municipality.
    """
    html_soup, _ = load_page_content(city_url)

    if not html_soup:
        return None

    data = {
        "registered": parse_int(get_cell_value("sa2", html_soup)),
        "envelopes": parse_int(get_cell_value("sa3", html_soup)),
        "valid": parse_int(get_cell_value("sa6", html_soup))
    }

    if None in data.values():
        return None

    for row in html_soup.find_all("tr"):
        party_name = row.find("td", {"headers": "t1sa1 t1sb2"})
        party_votes = row.find("td", {"headers": "t1sa2 t1sb3"})

        if party_name and party_votes:
            name = party_name.get_text(strip=True)
            votes = parse_int(party_votes.get_text(strip=True))
            data[name] = votes

    return pd.DataFrame([data])


def main(region_url, output_filename):
    """
    Main function that coordinates the scraping and export of election results.
    """
    print("🔄 Loading list of municipalities...")
    soup, _ = load_page_content(region_url)

    if not soup:
        print("❌ Failed to load region page.")
        return None

    cities = extract_city_list(soup)
    print(f"✅ Found municipalities: {len(cities)}")

    all_city_results = []

    for code, name, url in cities:
        print(f"➡️ Processing: {code} - {name}")
        city_df = extract_city_results(url)

        if city_df is not None:
            city_df.insert(0, "location", name)
            city_df.insert(0, "code", code)
            all_city_results.append(city_df)
        else:
            print(f"⚠️  Skipped due to error: {code} - {name}")

        time.sleep(0.5)

    if all_city_results:
        final_df = pd.concat(all_city_results, ignore_index=True)
        save_csv(output_filename, final_df)
    else:
        print("❌ No data was processed.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❌ Error: Please provide 2 arguments – the URL and the output CSV filename.")
        print("▶️ Usage: python main.py <URL> <output.csv>")
        sys.exit(1)

    region_url = sys.argv[1]
    output_file = sys.argv[2]

    if not re.match(r"^https://www\.volby\.cz/pls/ps2017nss/", region_url):
        print("❌ Invalid URL. It must start with: https://www.volby.cz/pls/ps2017nss/")
        sys.exit(1)

    if not output_file.lower().endswith(".csv"):
        print("❌ Output filename must end with .csv")
        sys.exit(1)

    main(region_url, output_file)

