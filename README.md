# Weather Aggregator Project

The Weather Aggregator project is a Django-based application that aggregates weather data from multiple sources and provides city-level weather information and daily weather averages. This project uses Django REST Framework for building API endpoints and Poetry for dependency management.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
- [Running the Development Server](#running-the-development-server)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Available Endpoints](#available-endpoints)

## Requirements

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/) (for dependency management)

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/weather-aggregator.git
    cd weather-aggregator
    ```

2. **Install dependencies**:
    Use Poetry to install project dependencies:
    ```bash
    poetry install
    ```

## Setup

1. **Database Configuration**:
    You don't need to do anything regarding this since it uses sqlite3

2. **Apply Migrations**:
    Run migrations to set up the database schema:
    ```bash
    python3 manage.py migrate
    ```

3. **Create a Superuser** (optional):
    If you need access to Django's admin panel, create a superuser account:
    ```bash
    python3 manage.py createsuperuser
    ```

## Running the Development Server

To start the Django development server, run:

```bash
python manage.py runserver
```

## Running tests

To run unit tests on this server, run:

```bash
python manage.py test
```

## Project Structure

weather-aggregator/
│

├── general/                   # General utilities, views for normalized data endpoints

├── weather_master_x/          # App for Weather Master X data

├── bulgarian_meteo_pro/       # App for Bulgarian Meteo Pro data

├── stations/                  # App handling station data and authorization classes

├── manage.py                  # Django management script

├── README.md                  # Project documentation

└── pyproject.toml             # Poetry configuration file with dependencies


## Available Endpoints 

For a list of all the available endpoints visit '/api/docs/'
