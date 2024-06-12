#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from google.cloud import bigquery
import google.cloud.exceptions
from flask import Flask
import settings

app = Flask(__name__)

# Check if running inside Docker
if os.getenv('DOCKER_ENV') == 'true':
    from pyvirtualdisplay import Display

    display = Display(visible=0)
    display.start()


def set_environment():
    """Set up the environment variable for Google Cloud authentication."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.bigquery_service_account


def init_webdriver():
    """Initialize and return a Chrome WebDriver optimized for running in a Docker container."""
    # Setup Chrome options for headless operation
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless Chrome
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model, crucial for Docker
    chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    chrome_options.add_argument('--disable-gpu')  # disable gpu hardware acceleration
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-infobars')

    # Optional: Use ChromeDriverManager to handle driver automatically
    service = Service(ChromeDriverManager().install())

    # Initialize a new browser instance with specified options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


def scrape_job_postings(driver):
    """Scrape job postings from a fake job board and return them as a list of dictionaries."""
    driver.get(settings.JOB_BOARD_URL)
    time.sleep(settings.PAGE_LOAD_DELAY)

    jobs = []
    job_cards = driver.find_elements(By.CLASS_NAME, "card-content")

    for card in job_cards:
        title = card.find_element(By.CLASS_NAME, "title").text
        company = card.find_element(By.CLASS_NAME, "company").text
        location = card.find_element(By.CLASS_NAME, "location").text
        date_posted = card.find_element(By.TAG_NAME, "time").text

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "date_posted": date_posted
        })

    return jobs


def upload_df_to_bigquery(dataframe: pd.DataFrame, project_id: str, dataset_id: str, table_name: str):
    """Uploads a pandas DataFrame to a BigQuery table. If the provided dataset_id does not exist, it creates it.

     Args:
         dataframe (pd.DataFrame): The pandas DataFrame to upload.
         project_id (str): Your GCP project ID.
         dataset_id (str): The ID of the BigQuery dataset where the table will be created.
         table_name (str): The name of the BigQuery table to create.

     Returns:
         None
     """
    # Construct a BigQuery client object
    client = bigquery.Client()
    dataset_id = f"{project_id}.{dataset_id}"

    # Construct a full Dataset object and then post it to BQ API.
    # we autodetect the database schema, and that's why schema declaration is missing from Dataset Constructor
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = settings.BIG_QUERY_REGION
    try:
        dataset = client.create_dataset(dataset, timeout=30)
        print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
    except google.cloud.exceptions.Conflict as e:
        print(e)

    table_id = f"{dataset_id}.{table_name}"

    # Modify job_config for partitioning and truncating
    # autodetect dataset schema
    j_config = bigquery.LoadJobConfig(
        autodetect=True,
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED'
    )

    # Make and API request to store data into BQ
    try:
        j = client.load_table_from_dataframe(dataframe, table_id, job_config=j_config)
        j.result()  # wait for the job to complete
        print(f"Data uploaded successfully to {table_id}")
    except ValueError as e:
        print(dataframe.dtypes)
        print(table_id)
        raise e
    except TypeError as e:
        print(dataframe.dtypes)
        print(table_id)
        raise e


@app.route('/')
def main():
    """Initializes necessary scraping variables, scrapes and converts job data, then uploads them to BigQuery.

    :return:
        string:
    """
    set_environment()
    driver = init_webdriver()
    return_message = ''
    try:
        jobs = scrape_job_postings(driver)
        jobs_df = pd.DataFrame(jobs)
        # Convert the date_posted column from string to date data type
        jobs_df['date_posted'] = pd.to_datetime(jobs_df['date_posted'], errors='coerce', format='%Y-%m-%d')
        upload_df_to_bigquery(jobs_df, project_id=settings.PROJECT_ID, dataset_id=settings.DATASET_ID,
                              table_name=settings.TABLE_NAME)
        return_message = '200, Success'
    except Exception as e:
        return_message = str(e)
    finally:
        driver.quit()
        print("WebDriver session has been closed")
        return return_message


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
