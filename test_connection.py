#!/usr/bin/env python3
"""
Test script to verify database connection and table access
"""

import os
import sqlalchemy
from sqlalchemy import text
from dotenv import load_dotenv
import smtplib
from db_utils import get_purchase_requests, PURCHASE_REQ_TABLE

# Load environment variables
load_dotenv()

def test_connection():
    """Test database connection and query functionality"""
    print("🔌 Testing database connection...")
    try:
        # Create engine
        engine = sqlalchemy.create_engine(os.getenv("DATABASE_URL"))
        
        # Test connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
            # Try to query the specific table
            try:
                with engine.connect() as new_connection:
                    result = new_connection.execute(
                        text(f"SELECT COUNT(*) FROM {PURCHASE_REQ_TABLE}")
                    )
                    count = result.scalar()
                    print(f"✅ Table query successful! Found {count} purchase requisitions.")
                    
                    # Get sample records
                    sample_query = text(f"SELECT TOP 5 * FROM {PURCHASE_REQ_TABLE}")
                    sample = new_connection.execute(sample_query).fetchall()
                    
                    print("\nSample records:")
                    for row in sample:
                        print(f"Document: {row['No_']} | Employee: {row['Employee Name']} | Status: {row['Status']}")
                    
                    # Test email lookup
                    approver_emails = []
                    for row in sample:
                        if row.get('approver_mailid'):
                            approver_emails.append(f"{row['No_']}: {row['approver_mailid']}")
                    
                    if approver_emails:
                        print("\nFound approver emails:")
                        for email in approver_emails:
                            print(f"  - {email}")
                    else:
                        print("\nNo approver emails found in sample data.")
            except Exception as e:
                print(f"❌ Table query failed: {e}")
                
            # Test email configuration
            test_email_config()
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Install ODBC Driver 18 for SQL Server")
        print("2. Check your .env file has correct DATABASE_URL")
        print("3. Ensure SQL Server is running")

def test_email_config():
    """Test SMTP email configuration"""
    print("\n📧 Testing email configuration...")
    
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if not all([smtp_server, smtp_port, smtp_username, smtp_password]):
        print("❌ SMTP settings not properly configured in .env file")
        print("   Check your .env file for SMTP_* variables")
        return
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            print(f"✅ Successfully connected to SMTP server: {smtp_server}")
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        print("   Please check your SMTP credentials and server settings")

if __name__ == "__main__":
    test_connection()