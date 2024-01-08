from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re

def convert_salary(salary):
    matches = re.findall(r'\$([\d,]+)(?:\s*-\s*\$([\d,]+))?\s*(a\s*(year|month|hour))?', salary)
    salary_mean=0
    if matches:
        # Extract lower and upper bounds
        lower_bound = float(matches[0][0].replace(',', ''))
        upper_bound = float(matches[0][1].replace(',', '')) if matches[0][1] else lower_bound

        # Check if frequency is specified and adjust mean calculation accordingly
        frequency = matches[0][3]
        if frequency == 'month':
            # If salary is per month, multiply by 12 to get annual salary
            lower_bound *= 12
            upper_bound *= 12
        elif frequency == 'hour':
            # If salary is per hour, multiply by average work hours per week and weeks per year
            lower_bound *= 40 * 52  # Assuming 40 hours per week and 52 weeks per year
            upper_bound *= 40 * 52

        # Calculate mean
        salary_mean = (lower_bound + upper_bound) / 2
    
    return salary_mean

def scrape_jobs():
    driver = webdriver.Chrome()

    driver.get(f'https://www.indeed.com/jobs?q=Python+Developer')
    next_page = 2
    jobs = []

    while next_page < 9:
        time.sleep(10)
        job_listings_container = driver.find_element(By.ID, 'mosaic-provider-jobcards')
        job_listings_ul = job_listings_container.find_element(By.TAG_NAME, 'ul')
        job_listings = job_listings_ul.find_elements(By.XPATH, "./child::*")
        for job in job_listings:
            elemid = job.find_elements(By.XPATH, "./child::*")[0].get_attribute('id')
            curr_job = job.find_elements(By.XPATH, "./child::*")[0]
            if elemid == '':
                job_title = curr_job.find_element(By.CSS_SELECTOR, 'h2.jobTitle').text
                job_company = curr_job.find_element(By.XPATH, ".//span[@data-testid='company-name']").text
                job_location = curr_job.find_element(By.XPATH, ".//div[@data-testid='text-location']").text
                job_salary = 0
                try:
                    job_salary = convert_salary(curr_job.find_element(By.CSS_SELECTOR, "div.salary-snippet-container").text)
                except NoSuchElementException:
                    job_salary = 0
                # job_description = job.find_element(By.CSS_SELECTOR, 'div.summary').text

                jobs.append({
                    'job_title': job_title,
                    'job_company': job_company,
                    'job_location': job_location,
                    'job_salary': job_salary,
                    # 'job_description': job_description
                })
        # next page
        try:
            next_page_btn = driver.find_element(By.XPATH, f"//a[@data-testid='pagination-page-{next_page}']")
            next_page+=1
            next_page_btn.click()
        except NoSuchElementException:
            break

    # driver.quit()
    return jobs