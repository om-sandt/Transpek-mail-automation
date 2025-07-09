#!/usr/bin/env python3
"""
Database Setup Script for Approval Workflow System

This script helps you set up the PostgreSQL database for the approval workflow system.
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from models import db, ApprovalRequest, JobWorkReport, IMPurchaseRequisition

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

def create_tables(database_url):
    """Create database tables"""
    try:
        engine = create_engine(database_url)
        
        # Create tables
        db.metadata.create_all(engine)
        print("✅ Database tables created successfully!")
        
        # Verify table creation
        with engine.connect() as conn:
            tables_to_check = ['approval_requests', 'job_work_report', 'im_purchase_requisition']
            for table_name in tables_to_check:
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = :table_name
                """), {'table_name': table_name})
                if result.fetchone():
                    print(f"✅ {table_name} table verified!")
                else:
                    print(f"❌ {table_name} table creation verification failed!")
                    return False
                
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return False

def insert_sample_data(database_url):
    """Insert sample data for testing"""
    try:
        engine = create_engine(database_url)
        
        # Sample approval requests
        sample_requests = [
            {
                'data': 'Request for new software license purchase\n\nSoftware: Adobe Creative Suite\nQuantity: 5 licenses\nCost: $2,500\nDepartment: Marketing\n\nThis purchase is needed for the upcoming campaign design work.',
                'approver_email': 'manager@company.com',
                'status': 'Pending'
            },
            {
                'data': 'Travel request for conference attendance\n\nConference: TechCrunch Disrupt 2024\nLocation: San Francisco, CA\nDates: March 15-17, 2024\nEstimated Cost: $3,200\n\nThis conference will provide valuable insights into emerging technologies.',
                'approver_email': 'hr@company.com',
                'status': 'Pending'
            },
            {
                'data': 'Hardware upgrade request\n\nEquipment: Dell XPS 15 Laptop\nSpecifications: 32GB RAM, 1TB SSD, RTX 4070\nQuantity: 1\nCost: $2,800\n\nCurrent laptop is 5 years old and no longer meets performance requirements.',
                'approver_email': 'it@company.com',
                'status': 'Approved',
                'reason': 'Approved - Hardware is outdated and affecting productivity'
            }
        ]
        
        with engine.connect() as conn:
            for request_data in sample_requests:
                conn.execute(text("""
                    INSERT INTO approval_requests (data, approver_email, status, reason)
                    VALUES (:data, :approver_email, :status, :reason)
                """), request_data)
            conn.commit()
            
        print("✅ Sample data inserted successfully!")
        return True
    except Exception as e:
        print(f"❌ Error inserting sample data: {str(e)}")
        return False

def add_email_sent_columns():
    """Add email_sent column to existing tables if it doesn't exist"""
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is required")
    
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # Check if email_sent column exists in job_work_report
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'job_work_report' 
                AND column_name = 'email_sent'
            """))
            
            if not result.fetchone():
                print("Adding email_sent column to job_work_report table...")
                conn.execute(text("ALTER TABLE job_work_report ADD COLUMN email_sent BOOLEAN DEFAULT FALSE"))
            
            # Check if email_sent column exists in im_purchase_requisition
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'im_purchase_requisition' 
                AND column_name = 'email_sent'
            """))
            
            if not result.fetchone():
                print("Adding email_sent column to im_purchase_requisition table...")
                conn.execute(text("ALTER TABLE im_purchase_requisition ADD COLUMN email_sent BOOLEAN DEFAULT FALSE"))
            
            # Check if email_sent column exists in approval_requests
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'approval_requests' 
                AND column_name = 'email_sent'
            """))
            
            if not result.fetchone():
                print("Adding email_sent column to approval_requests table...")
                conn.execute(text("ALTER TABLE approval_requests ADD COLUMN email_sent BOOLEAN DEFAULT FALSE"))
            
            conn.commit()
            print("Email tracking columns added successfully!")
            
        except Exception as e:
            print(f"Error adding email_sent columns: {str(e)}")
            conn.rollback()

def main():
    """Main setup function"""
    print("🚀 Approval Workflow Database Setup")
    print("=" * 50)
    
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
        print("- Ensure PostgreSQL is running")
        print("- Verify database exists: CREATE DATABASE approval_workflow;")
        print("- Check username/password in DATABASE_URL")
        print("- Ensure user has CREATE privileges")
        sys.exit(1)
    
    # Step 2: Create tables
    print("\nStep 2: Creating database tables...")
    if not create_tables(database_url):
        print("\n💡 Troubleshooting tips:")
        print("- Ensure user has CREATE TABLE privileges")
        print("- Check if tables already exist")
        sys.exit(1)
    
    # Step 3: Insert sample data (optional)
    print("\nStep 3: Insert sample data...")
    response = input("Would you like to insert sample data for testing? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        if insert_sample_data(database_url):
            print("📝 Sample data includes:")
            print("  - Software license request (Pending)")
            print("  - Travel request (Pending)")
            print("  - Hardware upgrade (Approved)")
        else:
            print("⚠️  Sample data insertion failed, but setup is complete.")
    
    # Add email_sent columns
    add_email_sent_columns()
    
    print("\n🎉 Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the Flask application: python app.py")
    print("2. Start the email processor: python send_emails.py")
    print("3. Access the web interface at: http://localhost:5000")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main() 