"""Example insert script"""
from datetime import datetime
from db_utils import insert_im_purchase_req, setup_database
import traceback

def main():
    """Main function"""
    print("Testing database connection...")
    if not setup_database():
        print("Database connection failed!")
        return

    print("Inserting test record...")
    
    # Test data matching SQL example exactly
    data = {
        "$systemCreatedAt": "2024-09-20T12:09:03.320Z",
        "$systemCreatedBy": "F8A07143-F39D-4035-A527-A3487D0DB295",
        "$systemId": "EAF6E11F-4977-EF11-BB91-F794BA0508DC",
        "$systemModifiedAt": "2025-06-05T12:02:41.557Z",
        "$systemModifiedBy": "A7505281-FAE6-4315-9133-32876391A677",
        "Approved By": "",
        "Approved By Account Dept_": 0,
        "Approved Date": "1753-01-01T00:00:00.000Z",
        "Approved Time": "1753-01-01T00:00:00.000Z",
        "Assigned User ID": "TIL\\TRIPEARLTECH4",
        "Capital Item Premises": 0,
        "Comment": 0,
        "Dimension Set ID": 33044,
        "Document Date": "2024-09-20T00:00:00.000Z",
        "Document Type": 0,
        "Due Date": "2024-09-22T00:00:00.000Z",
        "Employee Department": "",
        "Employee Name": "ATUL GOVINDJIBHAI SHROFF",
        "Employee No_": "10001",
        "Expected Receipt Date": "2024-09-20T00:00:00.000Z",
        "Gen_ Bus_ Posting Group": "",
        "Indent Type": 0,
        "Indenting Department": "BOILER DEPT.",
        "Job Card Date": "1753-01-01T00:00:00.000Z",
        "Job Card No_": "",
        "Job Task No_": "",
        "Last Posting No_": "",
        "Location Code": "",
        "No_": "MG4145",
        "No_ Series": "",
        "Posted": 0,
        "Posting Date": "2024-09-20T00:00:00.000Z",
        "Posting Description": "Purchase Requisition MG4145",
        "Posting No_": "",
        "Posting No_ Series": "",
        "Purchase Type": 6,
        "Reason Code": "",
        "Request Date": "2024-09-20T00:00:00.000Z",
        "Responsibility Center": "",
        "Shortcut Dimension 1 Code": "",
        "Shortcut Dimension 2 Code": "05",
        "Shortcut Dimension 2 Value": "BOILER DEPT.",
        "Shortcut Dimension 3 Code": "",
        "Shortcut Dimension 6 Code": "",
        "Status": 0,
        "Type of Jobwork": 0,
        "Your Reference": "",
        "approver_mailid": None,
        "email_send": None,
        "status": None,
        "timestamp": bytes.fromhex("00000000433780fd")
    }
    
    try:
        result = insert_im_purchase_req(data)
        if result:
            print("✅ Test record inserted successfully!")
        else:
            print("❌ Failed to insert test record")
    except Exception as e:
        print(f"❌ Error inserting test record: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
