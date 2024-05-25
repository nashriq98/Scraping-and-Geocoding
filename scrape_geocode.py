import requests
from bs4 import BeautifulSoup
import pymysql
from geopy.geocoders import Nominatim

# Function to scrape data from a single page
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    outlets = []

    # Extract information from each elementor-widget-container
    for container in soup.find_all('div', class_='elementor-widget-container'):
        title_element = container.find('span', class_='entry-title')
        address_element = container.find('p')

        # Check if both title and address elements are found before accessing their text attributes
        if title_element and address_element:
            title = title_element.text.strip()
            address = address_element.text.strip()

            # Check if the name is included in the address and remove it
            if title.lower() in address.lower():
                address = address.replace(title, '', 1).strip()

            outlets.append({'name': title, 'address': address})

    return outlets

# Function to scrape data from all pages
def scrape_all_pages(base_url):
    all_outlets = []

    # Set an initial page number
    page_number = 1

    while True:
        url = f"{base_url}/page/{page_number}"
        response = requests.get(url)

        if response.status_code == 200:
            # If the page exists, scrape its content
            outlets = scrape_page(url)

            if not outlets:
                # If no outlets found on the page, stop scraping
                break

            all_outlets.extend(outlets)
            page_number += 1
        else:
            # If the page doesn't exist, stop scraping
            break

    return all_outlets

# Function to get latitude and longitude based on the address using OpenStreetMap
def get_lat_lon(address):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(address)
    
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Function to insert data into the MySQL database
def insert_into_database(outlets):
    # Connect to MySQL server
    conn = pymysql.connect(
        host='your_host',
        port='your_port',
        user='your_user',
        password='your_password',
        database='your_database',
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = conn.cursor()

    # Create a table to store outlets if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS outlets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            address TEXT,
            latitude DECIMAL(10, 8),
            longitude DECIMAL(11, 8)
        )
    ''')

    # Insert or update each outlet in the database
    for outlet in outlets:
        # Check if the name already exists in the database
        cursor.execute('''
            SELECT id FROM outlets WHERE name = %s
        ''', (outlet['name'],))

        existing_record = cursor.fetchone()

        if existing_record:
            # If the name exists, update the address, latitude, and longitude
            cursor.execute('''
                UPDATE outlets
                SET address = %s, latitude = %s, longitude = %s
                WHERE id = %s
            ''', (outlet['address'], outlet.get('latitude'), outlet.get('longitude'), existing_record['id']))
        else:
            # If the name doesn't exist, insert a new record
            latitude, longitude = get_lat_lon(outlet['address'])
            cursor.execute('''
                INSERT INTO outlets (name, address, latitude, longitude)
                VALUES (%s, %s, %s, %s)
            ''', (outlet['name'], outlet['address'], latitude, longitude))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    base_url = "https://zuscoffee.com/category/store/melaka"

    # Scrape all pages and get outlets data
    all_outlets = scrape_all_pages(base_url)

    # Insert scraped data into the MySQL database
    insert_into_database(all_outlets)

    print("Scraping and database insertion completed.")
