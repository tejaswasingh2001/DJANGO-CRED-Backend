from scrape import scrape_jobs
from db_collection import get_collection
def run():
    print("Scrapping jobs...")
    scraped_jobs = scrape_jobs()
    print("Jobs scrapped!");
    
    #mongodb collection
    collection = get_collection()

    print("Adding data to database...")

    collection.insert_many(scraped_jobs)

    print("Added jobs to the database!")

run()