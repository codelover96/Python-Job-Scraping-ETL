#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()

is_local_environment = True  # set to false before deploy to GCP

cwd = os.getcwd()
keys_dir = os.path.join(cwd, "assets/keys")

bigquery_service_account = str(os.path.join(keys_dir, os.environ["GCP_BIG_Q_SERVICE_ACCOUNT_KEY"]))

PROJECT_ID = os.environ["PROJECT_ID"]
DATASET_ID = os.environ["BQ_DATASET_ID"]
TABLE_NAME = os.environ["BQ_TABLE_NAME"]
BIG_QUERY_REGION = os.environ["BQ_REGION"]

# Web Scraping Configuration
JOB_BOARD_URL = os.environ["JOB_POSTINGS_URL"]
PAGE_LOAD_DELAY = 2  # Seconds to wait for page to load
