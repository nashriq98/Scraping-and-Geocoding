# Outlet Map Project

This project consists of three main components: web scraping and geocoding, a Flask API, and a simple Leaflet-based frontend map.

## Components

1. **Scraping and Geocoding (Python Script)**:
    - The script `scrape_geocode.py` is responsible for scraping outlet data from a website and geocoding the addresses using OpenStreetMap.

2. **Flask API (Python Script)**:
    - The script `api.py` utilizes Flask to create a RESTful API that serves the outlet data stored in a MySQL database.

3. **Frontend (HTML/JavaScript)**:
    - The HTML file `outlet_map.html` contains a Leaflet map that fetches outlet data from the Flask API and displays markers on the map.

## Setup and Installation

### Prerequisites

1. **Python and Dependencies**:
    - Make sure you have Python installed. If not, download and install it from [python.org](https://www.python.org/downloads/).
    - Install the required Python packages using the following command:
        ```bash
        pip install -r requirements.txt
        ```

2. **MySQL Database**:
    - Install and set up a MySQL server. Update the MySQL connection details in `scrape_geocode.py`.

### Running the Web Scraping and Geocoding

1. **Scraping and Geocoding**:
    - Run the scraping script using the following command:
        ```bash
        python scrape_geocode.py
        ```

## Additional Notes

- The scraping and geocoding functionality is complete.
- Development for the Flask API and the frontend is ongoing.

## Author

Muhammad Amirul Nashriq Bin Aziz
