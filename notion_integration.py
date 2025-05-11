# File: notion_integration.py
from notion_client import Client
import pandas as pd

def sync_to_notion(csv_path, notion_token, database_id):
    # Initialize Notion client
    notion = Client(auth=notion_token)
    
    # Read scraped data
    df = pd.read_csv(csv_path)
    
    # Sync each job
    for _, row in df.iterrows():
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Title": {"title": [{"text": {"content": row["Title"]}}],
                "Company": {"rich_text": [{"text": {"content": row["Company"]}}],
                "Status": {"select": {"name": "Not Applied"}}
            }
        )

# Usage
sync_to_notion(
    csv_path="linkedin_jobs.csv",
    notion_token="your_notion_integration_token",
    database_id="your_database_id"
)