# Automated Web Scraper for Python Job Listings on Google Cloud Platform

## Project Overview
This repository showcases an automated web scraper developed to extract Python job listings, demonstrating the setup of a complete data pipeline on Google Cloud Platform (GCP).

## Project Architecture
![Project Architecture](https://github.com/codelover96/Python-Job-Scraping-ETL/blob/master/assets/images/project-structure.png)

## Skills Demonstrated
- **Web Scraping**: Uses Selenium for automated extraction of job listing data.
- **Cloud Automation**: Implements Cloud Run and Cloud Scheduler for deploying and scheduling the scraper.
- **Data Management**: Utilizes BigQuery for efficient data storage and management.

## Technologies Used
- Python3, Selenium
- Google Cloud Platform: Cloud Run, Cloud Scheduler, BigQuery

## Project Files
- `main.py`: Main script for scraping job listings.
- `app.py`: Flask application for deploying the scraper as a web service.
- `settings.py`: Configuration settings for API keys and database connections.
- `requirements.txt`: Lists all Python dependencies.
- `Dockerfile`: Docker configuration for building the application.
- `example.env`: Stores environmental variable such as Google Service Account Keys and BigQuery variables
- `.dockerignore`: Specifies which folders and files to ignore when building the docker image

## Setup and Installation
### Prerequisites
- A Google Cloud Platform account. [Start your free trial here](https://cloud.google.com/free).
- Basic knowledge of Python and Selenium for web scraping.

### Configuration and Deployment
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/python-job-scraper.git
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Local Environment Variables**
   - Create a `.env` file with the contents of the provided `example.env`
   - Configure variables, specific for your project
   - ***Important:*** Store you Big Query Service Account key inside `assets/keys` 
   
4. **Test the main.py locally to ensure the scraper functions correctly.**
   -  Run main.py locally to validate that the web scraper works as expected

5. **Deploy on Google Cloud.**
   - Use the provided Dockerfile to build the Docker Image of the Flask application (app.py).
   - Deploy the containerized Flask application on Cloud Run (detailed instructions provided by [DataProjects.io](https://dataprojects.io) in the project material).
   ![Cloud Run Example](https://github.com/codelover96/Python-Job-Scraping-ETL/blob/master/assets/images/cloud-run.JPG)
   - Set up Cloud Scheduler to automate the scraping process (detailed instructions provided by [DataProjects.io](https://dataprojects.io) in the project material).
   ![Cloud Run Example](https://github.com/codelover96/Python-Job-Scraping-ETL/blob/master/assets/images/cloud-scheduler.JPG)

### Running the Project
   - Ensure all settings in settings.py are correctly configured, deploy the scraper to Google Cloud Run, and manage the scraping schedule with Cloud Scheduler.
   - Preview of the created Big Query Dataset and Table
   ![Cloud Run Example](https://github.com/codelover96/Python-Job-Scraping-ETL/blob/master/assets/images/big-query-table-preview.JPG)

Contributions to this project are welcome! Please fork this repository and submit a pull request with your proposed changes.

## Scraped Data
As there are privacy and legal issues from scraping live job data, this project used fake job posting generated from [Fake Jobs](https://github.com/realpython/fake-jobs) initially.
With some JavaScript magic I was able to generate more fake jobs with Python relative roles, just for visualization purposes. These new job postings will help me, make better a better report with Looker Studio. 
You can find the newly created job postings in [this](https://codelover96.github.io/fake-jobs) GitHub page. If you would like to see the JavaScript code, head to my GitHub repo [here](https://github.com/codelover96/fake-jobs)


## Acknowledgments
This project is provided by [DataProjects.io](https://dataprojects.io), a platform that helps data professionals build a portfolio of real-world, end-to-end projects on the cloud.

## License
This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](Mozilla-Public-License-2.0.txt) file for details.