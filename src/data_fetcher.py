import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


class CRMEnergyScraper:

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.url = (
            "https://en.wikipedia.org/wiki/List_of_countries_by_lithium_production"
        )

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def clean_text(self, text):
        """Removes source citations (e.g. [1]) and extra whitespaces."""
        if not text:
            return ""
        cleaned = re.sub(r"\[.*?\]", "", text)
        return cleaned.strip()

    def parse_numeric(self, text):
        """Cleans character noise from numbers (commas, dashes, spaces) and converts to int."""
        if not text:
            return 0
        cleaned = (
            text.replace("—", "0")
            .replace(",", "")
            .replace(" ", "")
            .replace("-", "0")
            .strip()
        )
        try:
            return int(cleaned) if cleaned else 0
        except ValueError:
            return 0

    def scrape_lithium_data(self):
        """Scrapes global lithium production, reserves, and resources from Wikipedia."""
        print(f"🕵️ Fetching live comprehensive data from: {self.url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to retrieve data: {e}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # FIX 1: Find the specific table that contains our target headers
        table = None
        for candidate_table in soup.find_all("table", {"class": "wikitable"}):
            table_text = candidate_table.text.lower()
            if "reserves" in table_text and "resources" in table_text:
                table = candidate_table
                break

        if not table:
            print("❌ Could not find the correct data table on the page.")
            return None

        extracted_data = []

        # Iterate through table rows, skipping the header row
        for row in table.find_all("tr")[1:]:
            cols = row.find_all(["td", "th"])

            # FIX 2: Count from the back to support rows without a rank (like 'Other countries')
            if len(cols) >= 4:
                country = self.clean_text(cols[-4].text)

                # Skip summary rows
                if "world" in country.lower() or "total" in country.lower():
                    continue

                production = self.parse_numeric(self.clean_text(cols[-3].text))
                reserves = self.parse_numeric(self.clean_text(cols[-2].text))
                resources = self.parse_numeric(self.clean_text(cols[-1].text))

                extracted_data.append(
                    {
                        "country": country,
                        "production_tonnes": production,
                        "reserves_tonnes": reserves,
                        "resources_tonnes": resources,
                    }
                )

        # FIX 3: Explicitly define columns so Pandas never throws a KeyError if empty
        df = pd.DataFrame(
            extracted_data,
            columns=[
                "country",
                "production_tonnes",
                "reserves_tonnes",
                "resources_tonnes",
            ],
        )

        if df.empty:
            print("⚠️ Warning: No data was extracted from the table.")
            return df

        # Sort by resources descending
        df = df.sort_values(by="resources_tonnes", ascending=False)

        # Save to CSV
        output_path = os.path.join(self.data_dir, "lithium_comprehensive.csv")
        df.to_csv(output_path, index=False)

        print(f"✅ Successfully scraped {len(df)} countries with full metrics.")
        print(f"🎯 Complete dataset saved to: {output_path}")

        return df


if __name__ == "__main__":
    scraper = CRMEnergyScraper()
    data = scraper.scrape_lithium_data()
    if data is not None and not data.empty:
        print("\n📊 Preview of the strategic dataset:")
        print(data.head(10))
