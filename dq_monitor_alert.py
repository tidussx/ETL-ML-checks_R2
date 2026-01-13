import os
import pandas as pd
from sqlalchemy import create_engine
import requests

def run_dq_audit():
    # Fetch connection string from GitHub Secrets environment
    db_url = os.getenv('DB_CONNECTION_STRING')
    if not db_url:
        raise ValueError("No DB_CONNECTION_STRING found in environment variables")

    engine = create_engine(db_url)
    
    # Use the SQL query we wrote earlier
    query = """
    SELECT u.user_id, 'Inconsistency' as issue_type
    FROM Platform_Core.user_accounts u
    LEFT JOIN Identity_Vault.verification_status k ON u.user_id = k.user_id
    WHERE k.verification_status IS NULL;
    """
    
    try:
        df_issues = pd.read_sql_query(query, engine)
        if not df_issues.empty:
            send_slack_alert(df_issues)
    except Exception as e:
        print(f"Error connecting to database: {e}")

def send_slack_alert(data):
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    message = {
        "text": f"RING_RING *Data Governance Alert*: Found {len(data)} synchronization mismatches across KYC/KYB databases."
    }
    requests.post(webhook_url, json=message)

if __name__ == "__main__":
    run_dq_audit()
