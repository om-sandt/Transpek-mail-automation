"""Email processor for approval notifications"""
import os
import time
import pyodbc
from datetime import datetime
from dotenv import load_dotenv
from db_utils import PURCHASE_REQ_TABLE, send_approval_email, track_email

load_dotenv()

def process_pending_emails():
    """Send emails for pending approvals"""
    try:
        conn_str = os.getenv("DATABASE_URL")
        if not conn_str:
            print("❌ DATABASE_URL not configured")
            return
            
        # Query for pending requests that haven't been emailed yet
        sql = f"""
        SELECT * FROM {PURCHASE_REQ_TABLE}
        WHERE [Status] = 2 
        AND ([email_send] IS NULL OR [email_send] = '0')
        AND [approver_mailid] IS NOT NULL
        AND [approver_mailid] != ''
        """
        
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            if not rows:
                print("No pending emails to send")
                return
                
            success = 0
            failed = 0
            
            for row in rows:
                try:
                    # Convert row to dictionary
                    columns = [column[0] for column in cursor.description]
                    data = dict(zip(columns, row))
                    
                    # Send email
                    if send_approval_email(data):
                        # Mark as sent
                        update_sql = f"""
                        UPDATE {PURCHASE_REQ_TABLE}
                        SET [email_send] = '1'
                        WHERE [No_] = ?
                        """
                        cursor.execute(update_sql, (data.get('No_', ''),))
                        conn.commit()
                        success += 1
                        print(f"✅ Email sent for document {data.get('No_', '')}")
                    else:
                        failed += 1
                        print(f"❌ Failed to send email for document {data.get('No_', '')}")
                        
                except Exception as e:
                    failed += 1
                    print(f"❌ Error processing document {data.get('No_', '')}: {e}")
                    
            if success or failed:
                print(f"📧 Email processing complete: {success} sent, {failed} failed")
                
    except Exception as e:
        print(f"❌ Error processing emails: {e}")

def main():
    """Main loop"""
    print("📧 Starting email processor...")
    print("🔍 Checking for pending approval emails...")
    
    while True:
        try:
            process_pending_emails()
            print("⏳ Waiting 60 seconds before next check...")
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n🛑 Email processor stopped by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error in email processor: {e}")
            print("⏳ Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    main()