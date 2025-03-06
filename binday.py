#!/usr/bin/env python
import requests
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

# Unique Property Reference Number (UPRN)
UPRN = os.getenv("UPRN")
if not UPRN:
    raise ValueError("UPRN environment variable not set")

# Session URL for authentication
SESSION_URL = os.getenv("SESSION_URL")
if not SESSION_URL:
    raise ValueError("SESSION_URL environment variable not set")

# API URL to fetch bin collection details
API_URL = os.getenv("API_URL")
if not API_URL:
    raise ValueError("API_URL environment variable not set")

# Referer URL
REFERER = os.getenv("REFERER")
if not REFERER:
    raise ValueError("REFERER environment variable not set")

# Headers to mimic a browser request
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": REFERER,
}

# Map bin names to more user-friendly names
BIN_NAME_CONVERSION = {
    "140L Food & Garden (Green Lid)": "Green Bin",
    "180L Metal Glass & Plastic (Blue Lid)": "Blue Bin",
    "180L Paper & Card (Red Lid)": "Red Bin",
    "180L Refuse (Grey Lid)": "Black Bin"
}
# Create a session to maintain cookies
session = requests.Session()


def get_bin_collection_data():
    try:
        # Get session authentication data
        auth_response = session.get(SESSION_URL, headers=HEADERS)
        auth_response.raise_for_status()
        session_data = auth_response.json()

        # Extract session ID
        sid = session_data.get("auth-session")
        if not sid:
            raise ValueError("Failed to retrieve session ID")

        # Request bin collection data
        params = {
            "id": "64d9feda3a507",
            "_": str(int(time.time() * 1000)),  # Unix timestamp
            "sid": sid,
        }

        data = {"formValues": {"Section 1": {"uprnCore": {"value": UPRN}}}}

        response = session.post(
            API_URL, json=data, headers=HEADERS, params=params)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching bin collection data: {e}")
        return None


def parse_bin_collection_data(raw_data):
    if not raw_data or "data" not in raw_data:
        logging.error("No valid data received.")
        return None

    xml_data = raw_data["data"]
    root = ET.fromstring(xml_data)

    bins = []
    for row in root.findall(".//Row"):
        bin_type = row.find(".//result[@column='AssetTypeName']").text
        bin_type_converted = BIN_NAME_CONVERSION.get(bin_type)
        next_collection = row.find(".//result[@column='NextInstance']").text

        # Convert next_collection to a datetime object
        next_collection_date = datetime.strptime(next_collection, "%Y-%m-%d")

        # Check if next_collection_date is within 7 days
        if next_collection_date <= datetime.now() + timedelta(days=7):
            bins.append({"Bin Type": bin_type_converted,
                        "Next Collection": next_collection_date})
    return bins


if __name__ == "__main__":
    raw_data = get_bin_collection_data()
    if raw_data:
        bin_schedule = parse_bin_collection_data(raw_data)
        if bin_schedule:
            next_collection_date = bin_schedule[0]["Next Collection"].strftime(
                "%A, %d %B %Y")
            print(f"Next bin collection on {next_collection_date}:")
            for bin_info in bin_schedule:
                print(f" - {bin_info['Bin Type']}")
    else:
        logging.error("Failed to retrieve bin collection data.")
