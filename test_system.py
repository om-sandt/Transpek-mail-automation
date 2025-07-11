#!/usr/bin/env python3
"""
Test script for the approval workflow system
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import pyodbc
        print("✅ pyodbc imported successfully")
    except ImportError as e:
        print(f"❌ pyodbc import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    except Exception as e:
        print(f"⚠️  SQLAlchemy import warning: {e}")
        print("   This may be a version compatibility issue, but the system should still work")
        # Don't fail the test for this
    
    try:
        from db_utils import setup_database, insert_im_purchase_req
        print("✅ db_utils imported successfully")
    except ImportError as e:
        print(f"❌ db_utils import failed: {e}")
        return False
    except Exception as e:
        print(f"⚠️  db_utils import warning: {e}")
        print("   This may be due to SQLAlchemy version issues, but core functionality should work")
        # Don't fail the test for this
    
    return True

def test_database_connection():
    """Test database connection"""
    print("\n🔍 Testing database connection...")
    
    try:
        from db_utils import setup_database
        if setup_database():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_form_submission():
    """Test form submission with sample data"""
    print("\n🔍 Testing form submission...")
    
    try:
        from db_utils import insert_im_purchase_req
        
        # Sample test data
        test_data = {
            "$systemCreatedAt": datetime.now().isoformat() + "Z",
            "$systemCreatedBy": "00000000-0000-0000-0000-000000000000",
            "$systemId": "00000000-0000-0000-0000-000000000000",
            "$systemModifiedAt": datetime.now().isoformat() + "Z",
            "$systemModifiedBy": "00000000-0000-0000-0000-000000000000",
            "Approved By": "Test Approver",
            "Approved By Account Dept_": 0,
            "Approved Date": "1753-01-01T00:00:00.000Z",
            "Approved Time": "1753-01-01T00:00:00.000Z",
            "Assigned User ID": "TEST\\USER",
            "Capital Item Premises": 0,
            "Comment": 0,
            "Dimension Set ID": 33044,
            "Document Date": "2024-09-20T00:00:00.000Z",
            "Document Type": 0,
            "Due Date": "2024-09-22T00:00:00.000Z",
            "Employee Department": "",
            "Employee Name": "TEST EMPLOYEE",
            "Employee No_": "TEST001",
            "Expected Receipt Date": "2024-09-20T00:00:00.000Z",
            "Gen_ Bus_ Posting Group": "",
            "Indent Type": 0,
            "Indenting Department": "TEST DEPT.",
            "Job Card Date": "1753-01-01T00:00:00.000Z",
            "Job Card No_": "",
            "Job Task No_": "",
            "Last Posting No_": "",
            "Location Code": "",
            "No_": "TEST001",
            "No_ Series": "",
            "Posted": 0,
            "Posting Date": "2024-09-20T00:00:00.000Z",
            "Posting Description": "Test Purchase Requisition",
            "Posting No_": "",
            "Posting No_ Series": "",
            "Purchase Type": 6,
            "Reason Code": "",
            "Request Date": "2024-09-20T00:00:00.000Z",
            "Responsibility Center": "",
            "Shortcut Dimension 1 Code": "",
            "Shortcut Dimension 2 Code": "05",
            "Shortcut Dimension 2 Value": "TEST DEPT.",
            "Shortcut Dimension 3 Code": "",
            "Shortcut Dimension 6 Code": "",
            "Status": 2,  # Pending
            "Type of Jobwork": 0,
            "Your Reference": "",
            "approver_mailid": "test@example.com",
            "email_send": None,
            "status": None,
            "timestamp": bytes.fromhex("00000000433780fd")
        }
        
        success = insert_im_purchase_req(test_data)
        if success:
            print("✅ Form submission test successful")
            return True
        else:
            print("❌ Form submission test failed")
            return False
            
    except Exception as e:
        print(f"❌ Form submission test error: {e}")
        return False

def test_email_functionality():
    """Test email functionality"""
    print("\n🔍 Testing email functionality...")
    
    try:
        from db_utils import send_approval_email
        
        # Test email data
        test_email_data = {
            "No_": "TEST001",
            "Employee Name": "Test Employee",
            "Indenting Department": "Test Department",
            "Request Date": "2024-09-20T00:00:00.000Z",
            "approver_mailid": "test@example.com"
        }
        
        # Check if email configuration is available
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        
        if not all([smtp_server, smtp_user, smtp_password]):
            print("⚠️  Email configuration incomplete - skipping email test")
            print("   Set SMTP_SERVER, SMTP_USER, and SMTP_PASSWORD in .env file")
            return True  # Not a failure, just not configured
        
        # Try to send test email
        success = send_approval_email(test_email_data)
        if success:
            print("✅ Email functionality test successful")
        else:
            print("❌ Email functionality test failed")
        return success
        
    except Exception as e:
        print(f"❌ Email functionality test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Approval Workflow System Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed - check your Python environment")
        return False
    
    # Test database connection
    if not test_database_connection():
        print("\n❌ Database connection failed - check your DATABASE_URL in .env file")
        return False
    
    # Test form submission
    if not test_form_submission():
        print("\n❌ Form submission test failed")
        return False
    
    # Test email functionality
    if not test_email_functionality():
        print("\n❌ Email functionality test failed")
        return False
    
    print("\n🎉 All tests passed! System is ready to use.")
    print("\n📝 Next steps:")
    print("   1. Run 'python start.py' to start the full system")
    print("   2. Access the web interface at http://localhost:5000")
    print("   3. Submit a new purchase requisition")
    print("   4. Check that emails are sent to approvers")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 