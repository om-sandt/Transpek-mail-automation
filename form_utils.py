"""Form processing utilities"""
from datetime import datetime
import uuid
from db_utils import insert_im_purchase_req, convert_to_type

def process_form_data(form_data):
    """Process form data for database insertion"""
    now = datetime.now()
    doc_no = f"MG{now.strftime('%H%M%S')}"  # Changed to match format MG4145
    
    processed_data = {
        "Document Type": 0,
        "No_": doc_no,
        "Employee No_": form_data.get('employee_no', ''),
        "Employee Name": form_data.get('employee_name', ''),
        "Your Reference": '',
        "Request Date": now,
        "Posting Date": now,
        "Expected Receipt Date": now,
        "Posting Description": f"Purchase Requisition {doc_no}",
        "Due Date": now,  # Changed to use the new doc_no format
        "Location Code": '',
        "Comment": 0,
        "Status": 0,
        "Purchase Type": 6,
        "Indenting Department": form_data.get('department', 'BOILER DEPT.'),
        "Assigned User ID": 'TIL\\TRIPEARLTECH4',
        "email_send": None,
        "approver_mailid": form_data.get('approver_email', ''),
        "$systemCreatedAt": datetime.utcnow(),
        "$systemCreatedBy": str(uuid.uuid4()),
        "$systemId": str(uuid.uuid4()),
        "$systemModifiedAt": datetime.utcnow(),
        "$systemModifiedBy": str(uuid.uuid4()),
        "timestamp": int(now.timestamp()).to_bytes(8, 'big')  # Convert to binary timestamp
    }
    
    return processed_data

def submit_purchase_requisition(form_data):
    """Submit purchase requisition"""
    try:
        data = process_form_data(form_data)
        result = insert_im_purchase_req(data)
        return True, f"Successfully submitted: {data['No_']}", data['No_']
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return False, f"Error submitting purchase requisition: {str(e)}\n{error_details}", None
    """
    # Convert data from form to proper database format
    processed_data = {}
    
    # Field mappings exactly matching database schema
    field_mappings = {
        'timestamp': ('timestamp', None),
        'Document Type': ('int', None),
        'No_': ('nvarchar', 20),
        'Employee No_': ('nvarchar', 20),
        'Employee Name': ('nvarchar', 50),
        'Your Reference': ('nvarchar', 30),
        'Request Date': ('datetime', None),
        'Posting Date': ('datetime', None),
        'Expected Receipt Date': ('datetime', None),
        'Posting Description': ('nvarchar', 50),
        'Due Date': ('datetime', None),
        'Location Code': ('nvarchar', 10),
        'Shortcut Dimension 1 Code': ('nvarchar', 20),
        'Shortcut Dimension 2 Code': ('nvarchar', 20),
        'Shortcut Dimension 2 Value': ('nvarchar', 100),
        'Comment': ('tinyint', None),
        'Posting No_': ('nvarchar', 20),
        'Last Posting No_': ('nvarchar', 20),
        'Reason Code': ('nvarchar', 10),
        'Gen_ Bus_ Posting Group': ('nvarchar', 10),
        'Document Date': ('datetime', None),
        'No_ Series': ('nvarchar', 10),
        'Posting No_ Series': ('nvarchar', 10),
        'Status': ('int', None),
        'Dimension Set ID': ('int', None),
        'Responsibility Center': ('nvarchar', 10),
        'Assigned User ID': ('nvarchar', 50),
        'Posted': ('tinyint', None),
        'Purchase Type': ('int', None),
        'Indenting Department': ('nvarchar', 100),
        'Employee Department': ('nvarchar', 10),
        'Type of Jobwork': ('int', None),
        'Capital Item Premises': ('int', None),
        'Shortcut Dimension 3 Code': ('nvarchar', 20),
        'Shortcut Dimension 6 Code': ('nvarchar', 20),
        'Indent Type': ('int', None),
        'Approved By': ('nvarchar', 250),
        'Approved Date': ('datetime', None),
        'Approved Time': ('datetime', None),
        'Job Card No_': ('nvarchar', 20),
        'Job Card Date': ('datetime', None),
        'Job Task No_': ('nvarchar', 20),
        'Approved By Account Dept_': ('tinyint', None)
    }

    # Process form fields and convert to correct types
    for db_field, (data_type, max_length) in field_mappings.items():
        form_field = db_field.lower().replace(' ', '_').replace('_', '')
        if form_field in form_data:
            processed_data[db_field] = convert_to_type(form_data[form_field], data_type, max_length)

    # Add system fields
    now = datetime.datetime.now()
    processed_data.update({
        '$systemId': str(uuid.uuid4()),
        '$systemCreatedAt': now,
        '$systemCreatedBy': form_data.get('user_id', 'SYSTEM'),
        '$systemModifiedAt': now,
        '$systemModifiedBy': form_data.get('user_id', 'SYSTEM'),
        'approver_mailid': form_data.get('approver_email', ''),
        'status': str(form_data.get('status', '2')),  # 2 = Pending
        'email_send': '0'
    })

    print(f"Processed data with correct column names: {processed_data.keys()}")
    return processed_data

def submit_purchase_requisition(form_data):
    """
    Submit a purchase requisition from form data
    
    Args:
        form_data: Dictionary of form data
        
    Returns:
        Tuple of (success, message, requisition_no)
    """
    try:
        # Process form data
        data = process_form_data(form_data)
        
        # Insert into database
        insert_im_purchase_req(data)
        
        return True, f"Successfully submitted purchase requisition: {data['No_']}", data["No_"]
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return False, f"Error submitting purchase requisition: {str(e)}\n{error_details}", None
        error_details = traceback.format_exc()
        return False, f"Error submitting purchase requisition: {str(e)}\n{error_details}", None
