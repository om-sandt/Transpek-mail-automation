#!/usr/bin/env python3
"""
Database Setup Script for Transpek IM Purchase Requisition System

This script helps you set up the MS SQL Server database for the IM purchase requisition system.
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from models import db, IMPurchaseRequisition
import re

def check_database_connection(database_url):
    """Test database connection"""
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def check_table_exists(database_url):
    """Check if the IM purchase requisition table exists"""
    try:
        engine = create_engine(database_url)
        table_name = 'Transpek Industry Limited$TPT_IM Purch_ Req_ Header$114fe92f-996b-45f1-94bb-c0d5b6ba317e'
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = :table_name
            """), {'table_name': table_name})
            
            if result.fetchone():
                print(f"✅ Table {table_name} exists!")
                return True
            else:
                print(f"❌ Table {table_name} does not exist!")
                return False
                
    except Exception as e:
        print(f"❌ Error checking table: {str(e)}")
        return False

def add_status_and_email_columns(database_url):
    """Add Status and email_sent columns to existing table"""
    try:
        engine = create_engine(database_url)
        table_name = 'Transpek Industry Limited$TPT_IM Purch_ Req_ Header$114fe92f-996b-45f1-94bb-c0d5b6ba317e'
        
        with engine.connect() as conn:
            # Check if Status column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = :table_name 
                AND column_name = 'Status'
            """), {'table_name': table_name})
            
            if not result.fetchone():
                print("Adding Status column...")
                conn.execute(text(f"ALTER TABLE [{table_name}] ADD Status INT DEFAULT 0"))
                print("✅ Status column added!")
            else:
                print("✅ Status column already exists!")
            
            # Check if email_sent column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = :table_name 
                AND column_name = 'email_sent'
            """), {'table_name': table_name})
            
            if not result.fetchone():
                print("Adding email_sent column...")
                conn.execute(text(f"ALTER TABLE [{table_name}] ADD email_sent BIT DEFAULT 0"))
                print("✅ email_sent column added!")
            else:
                print("✅ email_sent column already exists!")
            
            # Check if approver_email column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = :table_name 
                AND column_name = 'approver_email'
            """), {'table_name': table_name})
            
            if not result.fetchone():
                print("Adding approver_email column...")
                conn.execute(text(f"ALTER TABLE [{table_name}] ADD approver_email NVARCHAR(255)"))
                print("✅ approver_email column added!")
            else:
                print("✅ approver_email column already exists!")
            
            conn.commit()
            print("✅ All required columns added successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error adding columns: {str(e)}")
        return False

def validate_approver_emails(database_url):
    """Validate approver emails in the database"""
    try:
        engine = create_engine(database_url)
        table_name = 'Transpek Industry Limited$TPT_IM Purch_ Req_ Header$114fe92f-996b-45f1-94bb-c0d5b6ba317e'
        
        with engine.connect() as conn:
            # Get all records with approver_email
            result = conn.execute(text(f"""
                SELECT timestamp, approver_email 
                FROM [{table_name}]
                WHERE approver_email IS NOT NULL AND approver_email != ''
            """))
            
            records = result.fetchall()
            valid_emails = []
            invalid_emails = []
            
            # Email validation regex
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            
            for record in records:
                timestamp, email = record
                if email and email_pattern.match(email):
                    valid_emails.append((timestamp, email))
                else:
                    invalid_emails.append((timestamp, email))
            
            print(f"✅ Found {len(valid_emails)} valid approver emails")
            if invalid_emails:
                print(f"⚠️  Found {len(invalid_emails)} invalid approver emails:")
                for timestamp, email in invalid_emails[:5]:  # Show first 5
                    print(f"   - Record {timestamp}: {email}")
                if len(invalid_emails) > 5:
                    print(f"   ... and {len(invalid_emails) - 5} more")
            
            return valid_emails, invalid_emails
            
    except Exception as e:
        print(f"❌ Error validating emails: {str(e)}")
        return [], []

def update_invalid_emails(database_url, invalid_emails):
    """Update invalid emails with a default email"""
    if not invalid_emails:
        return True
        
    try:
        engine = create_engine(database_url)
        table_name = 'Transpek Industry Limited$TPT_IM Purch_ Req_ Header$114fe92f-996b-45f1-94bb-c0d5b6ba317e'
        default_email = 'approver@transpek.com'
        
        with engine.connect() as conn:
            for timestamp, _ in invalid_emails:
                conn.execute(text(f"""
                    UPDATE [{table_name}]
                    SET approver_email = :default_email
                    WHERE timestamp = :timestamp
                """), {'default_email': default_email, 'timestamp': timestamp})
            
            conn.commit()
            print(f"✅ Updated {len(invalid_emails)} invalid emails to {default_email}")
            return True
            
    except Exception as e:
        print(f"❌ Error updating invalid emails: {str(e)}")
        return False

def show_database_stats(database_url):
    """Show database statistics"""
    try:
        engine = create_engine(database_url)
        table_name = 'Transpek Industry Limited$TPT_IM Purch_ Req_ Header$114fe92f-996b-45f1-94bb-c0d5b6ba317e'
        
        with engine.connect() as conn:
            # Total records
            result = conn.execute(text(f"SELECT COUNT(*) FROM [{table_name}]"))
            total_records = result.fetchone()
            total_records = total_records[0] if total_records else 0
            
            # Pending records (Status = 0)
            result = conn.execute(text(f"SELECT COUNT(*) FROM [{table_name}] WHERE Status = 0"))
            pending_records = result.fetchone()
            pending_records = pending_records[0] if pending_records else 0
            
            # Records with valid emails
            result = conn.execute(text(f"""
                SELECT COUNT(*) FROM [{table_name}] 
                WHERE approver_email IS NOT NULL 
                AND approver_email != '' 
                AND approver_email LIKE '%@%.%'
            """))
            valid_email_records = result.fetchone()
            valid_email_records = valid_email_records[0] if valid_email_records else 0
            
            print(f"\n📊 Database Statistics:")
            print(f"   Total Records: {total_records}")
            print(f"   Pending Records: {pending_records}")
            print(f"   Records with Valid Emails: {valid_email_records}")
            
    except Exception as e:
        print(f"❌ Error getting database stats: {str(e)}")

def main():
    """Main setup function"""
    print("🚀 Transpek IM Purchase Requisition Database Setup")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables!")
        print("Please create a .env file with your database configuration.")
        print("See env_example.txt for reference.")
        sys.exit(1)
    
    print(f"📊 Database URL: {database_url.split('@')[1] if '@' in database_url else 'Local database'}")
    print()
    
    # Step 1: Test connection
    print("Step 1: Testing database connection...")
    if not check_database_connection(database_url):
        print("\n💡 Troubleshooting tips:")
        print("- Ensure MS SQL Server is running")
        print("- Verify database exists")
        print("- Check username/password in DATABASE_URL")
        print("- Install ODBC Driver 17 for SQL Server")
        print("- Download from: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
        sys.exit(1)
    
    # Step 2: Check if table exists
    print("\nStep 2: Checking if table exists...")
    if not check_table_exists(database_url):
        print("\n💡 The table does not exist. Please ensure your database contains the required table.")
        sys.exit(1)
    
    # Step 3: Add required columns
    print("\nStep 3: Adding required columns...")
    if not add_status_and_email_columns(database_url):
        print("\n💡 Error adding columns. Please check database permissions.")
        sys.exit(1)
    
    # Step 4: Validate approver emails
    print("\nStep 4: Validating approver emails...")
    valid_emails, invalid_emails = validate_approver_emails(database_url)
    
    # Step 5: Update invalid emails if any
    if invalid_emails:
        print("\nStep 5: Updating invalid emails...")
        response = input("Would you like to update invalid emails to a default email? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            update_invalid_emails(database_url, invalid_emails)
    
    # Step 6: Show database statistics
    print("\nStep 6: Database statistics...")
    show_database_stats(database_url)
    
    print("\n🎉 Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the Flask application: python app.py")
    print("2. Start the email processor: python send_emails.py")
    print("3. Access the web interface at: http://localhost:5000")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main() 