# File: notion_integration.py
from notion_client import Client
import pandas as pd
import time
from config import NOTION_API_KEY, NOTION_DATABASE_ID

def sync_to_notion(csv_path, notion_token=NOTION_API_KEY, database_id=NOTION_DATABASE_ID):
    # Initialize Notion client
    notion = Client(auth=notion_token)
    
    # Read scraped data
    df = pd.read_csv(csv_path)
    
    # Sync each job
    for _, row in df.iterrows():
        try:
            notion.pages.create(
                parent={"database_id": database_id},
                properties={
                    "Title": {"title": [{"text": {"content": row["Title"]}}]},
                    "Company": {"rich_text": [{"text": {"content": row["Company"]}}]},
                    "Status": {"select": {"name": "Not Applied"}},
                    "URL": {"url": row.get("Link", "")}  # Added URL field
                }
            )
            print(f"Added {row['Title']} at {row['Company']} to Notion")
            time.sleep(0.5)  # Rate limit protection
            
        except Exception as e:
            print(f"❌ Failed to add {row['Title']}: {str(e)}")
            time.sleep(60)  # Wait longer after errors

# Usage with config.py values (no hardcoded credentials)
if __name__ == "__main__":
    sync_to_notion(csv_path="linkedin_jobs.csv")