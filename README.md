# Real-Time Customer Behavior Analysis Platform

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Services](#running-the-services)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Data Ingestion](#data-ingestion)
  - [Data Processing](#data-processing)
  - [Dashboard](#dashboard)
- [Logging and Monitoring](#logging-and-monitoring)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

The **Real-Time Customer Behavior Analysis Platform** is a comprehensive data engineering project designed to simulate, process, and visualize customer behavior data in real-time. This platform showcases modern data engineering practices, utilizing containerization, 
streaming data processing, and interactive dashboards.

## Features

- **Data Ingestion**: Simulates customer behavior events and streams them to Kafka.
- **Data Processing**: Consumes data from Kafka, processes it, and stores it in MongoDB.
- **Real-Time Dashboard**: Visualizes customer behavior data in real-time using Streamlit.
- **Robust Logging**: Implements detailed logging for monitoring and debugging.
- **Containerization**: Uses Docker Compose to orchestrate services like Kafka, Zookeeper, MongoDB, and Spark.

## Technologies Used

- **Programming Language**: Python 3.11+
- **Containerization**: Docker, Docker Compose
- **Messaging**: Kafka, Zookeeper
- **Data Processing**: Spark (Master and Worker)
- **Database**: MongoDB
- **Dashboard**: Streamlit
- **Dependency Management**: Poetry
- **Logging**: Loguru, Python Logging
- **Version Control**: Git

## Setup Instructions

### Prerequisites

- **macOS** operating system.
- **Terminal** access.
- **Homebrew** installed.
- **Docker** and **Docker Compose** installed.
- **Python 3.11+** installed.
- **Poetry** installed.
- **Git** initialized in the project.

### Installation

1. **Clone the Repository**:

Usage
Follow these steps to set up and run the project on your local machine.

1. Clone the Repository:

bash
Copy code
git clone git@github.com:yourusername/real_time_customer_behavior_analysis.git
cd real_time_customer_behavior_analysis
2. Set Up Docker Services:

Navigate to the docker directory and start all services:

bash
Copy code
cd docker
docker-compose up -d
This will start the following services:

MongoDB: for storing customer behavior events.
Zookeeper: for managing Kafka.
Kafka: for streaming customer behavior events.
Spark: for data processing.
3. Install Dependencies:

For each project component, navigate to the corresponding directory and install the dependencies.

Data Ingestion (Simulates customer behavior and sends events to Kafka):
bash
Copy code
cd data_ingestion
poetry install
Data Processing (Consumes customer behavior events from Kafka and stores them in MongoDB):
bash
Copy code
cd ../data_processing
poetry install
Dashboard (Visualizes customer behavior data in real-time):
bash
Copy code
cd ../dashboard
poetry install
4. Run Data Ingestion:

To start the data ingestion service, navigate to the data_ingestion folder and run the following command:

bash
Copy code
cd data_ingestion
poetry shell
python producer.py
Press Ctrl + C to stop the process.

5. Run Data Processing:

Open another terminal window, and start the data processing service:

bash
Copy code
cd data_processing
poetry shell
python consumer.py
This will consume the events from Kafka, process them, and store them in MongoDB. Press Ctrl + C to stop the process.

6. Run the Dashboard:

Open a third terminal window and run the Streamlit dashboard to visualize the data:

bash
Copy code
cd dashboard
poetry shell
streamlit run app.py
This will start the Streamlit dashboard. You can access it in your browser at:

http://localhost:8501
Project Structure

bash
Copy code
real_time_customer_behavior_analysis/
├── data_ingestion/
│   ├── producer.py
│   ├── .env
│   ├── pyproject.toml
│   └── poetry.lock
├── data_processing/
│   ├── consumer.py
│   ├── setup_db.py
│   ├── .env
│   ├── pyproject.toml
│   └── poetry.lock
├── dashboard/
│   ├── app.py
│   ├── .env
│   ├── pyproject.toml
│   └── poetry.lock
├── docker/
│   └── docker-compose.yml
├── .gitignore
└── README.md
Usage

Data Ingestion
Purpose: Simulates customer behavior events and streams them to Kafka.
Running:
bash
Copy code
cd data_ingestion
poetry shell
python producer.py
Data Processing
Purpose: Consumes events from Kafka, processes them, and stores them in MongoDB.
Running:
bash
Copy code
cd data_processing
poetry shell
python consumer.py
Dashboard
Purpose: Visualizes customer behavior data in real-time.
Running:
bash
Copy code
cd dashboard
poetry shell
streamlit run app.py
Logging and Monitoring

Data Ingestion Logs: Located in data_ingestion/producer.log.

Data Processing Logs: Located in data_processing/consumer.log and data_processing/setup_db.log.

Dashboard Logs: Displayed in the terminal running Streamlit.

Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

License

MIT License

Contact

WILFRIED ADAMS FONKOU DINESSO
Email: fonkouadams01@outlook.com

