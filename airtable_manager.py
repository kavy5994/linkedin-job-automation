import os
from pyairtable import Api


class AirtableManager:
    def __init__(self):
        self.api = Api(os.getenv("AIRTABLE_API_KEY"))
        self.base = self.api.base(os.getenv("AIRTABLE_BASE_ID"))
        self.table = self.base.table(os.getenv("AIRTABLE_TABLE_NAME"))
    
    def add_job(self, job_data):
        self.table.create(job_data)
    
    def get_unapplied_jobs(self):
        return self.table.all(formula="NOT({Status} = 'Applied')")