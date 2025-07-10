#!/usr/bin/env python3
"""
Test script to verify database connection and table access
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def test_connection():
    """Test database connection"""
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        print("🔌 Testing database connection...")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Test basic connection
            result = conn.execute(text("SELECT 1 as test"))
            print("✅ Database connection successful!")
            
            # Test table access
            table_name = 'Transpek Industry Limited$TPT_IM Purch_ Req_ Header$114fe92f-996b-45f1-94bb-c0d5b6ba317e'
            result = conn.execute(text(f"SELECT COUNT(*) FROM [{table_name}]"))
            count = result.fetchone()
            count = count[0] if count else 0
            print(f"✅ Table access successful! Found {count} records")
            
            # Test column access
            result = conn.execute(text(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = :table_name 
                AND column_name IN ('Status', 'email_sent', 'approver_email')
            """), {'table_name': table_name})
            
            columns = [row[0] for row in result.fetchall()]
            print(f"✅ Required columns found: {', '.join(columns)}")
            
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("1. Install ODBC Driver 17 for SQL Server")
        print("2. Check your .env file has correct DATABASE_URL")
        print("3. Ensure SQL Server is running")
        return False

if __name__ == "__main__":
    test_connection() 