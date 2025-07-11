"""Database utilities"""
import os
import pyodbc
import smtplib
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import text, create_engine
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

# Table name constants
PURCHASE_REQ_TABLE = "[dbo].[Transpek Industry Limited$TPT_IM Purch_ Req_ Header$114fe92f-996b-45f1-94bb-c0d5b6ba317e]"
EMAIL_TRACKING_TABLE = "[dbo].[email_tracking]"

def get_engine():
    """Get database engine"""
    conn_str = os.getenv("DATABASE_URL")
    if not conn_str:
        raise ValueError("DATABASE_URL not set in environment")
    return create_engine(conn_str)

def insert_im_purchase_req(data):
    """Insert a purchase requisition using the exact SQL format provided"""
    try:
        conn_str = os.getenv("DATABASE_URL")
        if not conn_str:
            raise ValueError("DATABASE_URL not set in environment")

        # Use the exact SQL insert command format
        sql = f"""INSERT INTO {PURCHASE_REQ_TABLE} (
            [$systemCreatedAt], [$systemCreatedBy], [$systemId], [$systemModifiedAt], [$systemModifiedBy], 
            [Approved By], [Approved By Account Dept_], [Approved Date], [Approved Time], [Assigned User ID], 
            [Capital Item Premises], [Comment], [Dimension Set ID], [Document Date], [Document Type], 
            [Due Date], [Employee Department], [Employee Name], [Employee No_], [Expected Receipt Date], 
            [Gen_ Bus_ Posting Group], [Indent Type], [Indenting Department], [Job Card Date], [Job Card No_], 
            [Job Task No_], [Last Posting No_], [Location Code], [No_], [No_ Series], [Posted], 
            [Posting Date], [Posting Description], [Posting No_], [Posting No_ Series], [Purchase Type], 
            [Reason Code], [Request Date], [Responsibility Center], [Shortcut Dimension 1 Code], 
            [Shortcut Dimension 2 Code], [Shortcut Dimension 2 Value], [Shortcut Dimension 3 Code], 
            [Shortcut Dimension 6 Code], [Status], [Type of Jobwork], [Your Reference], 
            [approver_mailid], [email_send], [status], [timestamp]
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        # Prepare values in the exact order as the SQL columns
        values = [
            data.get("$systemCreatedAt"),
            data.get("$systemCreatedBy"),
            data.get("$systemId"),
            data.get("$systemModifiedAt"),
            data.get("$systemModifiedBy"),
            data.get("Approved By"),
            data.get("Approved By Account Dept_"),
            data.get("Approved Date"),
            data.get("Approved Time"),
            data.get("Assigned User ID"),
            data.get("Capital Item Premises"),
            data.get("Comment"),
            data.get("Dimension Set ID"),
            data.get("Document Date"),
            data.get("Document Type"),
            data.get("Due Date"),
            data.get("Employee Department"),
            data.get("Employee Name"),
            data.get("Employee No_"),
            data.get("Expected Receipt Date"),
            data.get("Gen_ Bus_ Posting Group"),
            data.get("Indent Type"),
            data.get("Indenting Department"),
            data.get("Job Card Date"),
            data.get("Job Card No_"),
            data.get("Job Task No_"),
            data.get("Last Posting No_"),
            data.get("Location Code"),
            data.get("No_"),
            data.get("No_ Series"),
            data.get("Posted"),
            data.get("Posting Date"),
            data.get("Posting Description"),
            data.get("Posting No_"),
            data.get("Posting No_ Series"),
            data.get("Purchase Type"),
            data.get("Reason Code"),
            data.get("Request Date"),
            data.get("Responsibility Center"),
            data.get("Shortcut Dimension 1 Code"),
            data.get("Shortcut Dimension 2 Code"),
            data.get("Shortcut Dimension 2 Value"),
            data.get("Shortcut Dimension 3 Code"),
            data.get("Shortcut Dimension 6 Code"),
            data.get("Status"),
            data.get("Type of Jobwork"),
            data.get("Your Reference"),
            data.get("approver_mailid"),
            data.get("email_send"),
            data.get("status"),
            data.get("timestamp")
        ]
        
        # Insert data
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()
            print(f"Successfully inserted record with No_: {data.get('No_', 'Unknown')}")
            return True
            
    except Exception as e:
        print(f"Error inserting record: {e}")
        raise

def setup_database():
    """Test database connection"""
    try:
        conn_str = os.getenv("DATABASE_URL")
        if not conn_str:
            raise ValueError("DATABASE_URL not set in environment")
            
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def convert_to_type(value, data_type, max_length=None):
    """Convert value to the correct data type"""
    if value is None:
        return None
        
    try:
        if data_type == 'int':
            return int(value)
        elif data_type == 'tinyint':
            return min(max(int(value), 0), 255)
        elif data_type == 'nvarchar':
            return str(value)[:max_length] if max_length else str(value)
        elif data_type == 'datetime':
            if isinstance(value, datetime):
                return value
            return datetime.fromisoformat(value) if isinstance(value, str) else datetime.now()
        elif data_type == 'text':
            return str(value)
        elif data_type == 'uniqueidentifier':
            return str(value)
        elif data_type == 'timestamp':
            return datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            return str(value)
    except Exception as e:
        print(f"Warning: Could not convert {value} to {data_type}: {e}")
        return None

def create_email_tracking_table():
    """Create the email tracking table if it doesn't exist"""
    try:
        engine = get_engine()
        with engine.connect() as connection:
            # Check if table exists
            check_query = text("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = :table_name
            """)
            table_name = EMAIL_TRACKING_TABLE.replace('[', '').replace(']', '')
            count = connection.execute(check_query, {"table_name": table_name}).scalar()
            
            if count == 0:
                # Create the table
                query = text("""
                CREATE TABLE """ + EMAIL_TRACKING_TABLE + """ (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    document_no NVARCHAR(50),
                    status NVARCHAR(50),
                    email_sent NVARCHAR(10),
                    email_sent_date DATETIME,
                    recipient_email NVARCHAR(255),
                    email_subject NVARCHAR(255),
                    email_body NTEXT,
                    created_date DATETIME DEFAULT GETDATE()
                )
                """)
                connection.execute(query)
                connection.commit()
    except Exception as e:
        print(f"Warning: Could not create email tracking table: {e}")

def track_email(document_no, recipient_email, email_sent=0):
    """
    Track email sending status in a separate table
    
    Args:
        document_no: The document number
        recipient_email: Email address of the recipient
        email_sent: Whether the email was sent (0/1)
    """
    try:
        # First, check if email tracking table exists
        create_email_tracking_table()
        
        # Then insert/update tracking record
        engine = get_engine()
        with engine.connect() as connection:
            # Check if record exists
            check_query = text("SELECT COUNT(*) FROM " + EMAIL_TRACKING_TABLE + " WHERE document_no = :doc_no")
            count = connection.execute(check_query, {"doc_no": document_no}).scalar()
            
            if count and count > 0:
                # Update existing record
                query = text("""
                UPDATE """ + EMAIL_TRACKING_TABLE + """ 
                SET email_sent = :email_sent, recipient_email = :recipient, 
                    email_sent_date = CASE WHEN :email_sent = '1' THEN GETDATE() ELSE NULL END
                WHERE document_no = :doc_no
                """)
                connection.execute(query, {
                    "email_sent": str(email_sent), 
                    "recipient": recipient_email, 
                    "doc_no": document_no
                })
            else:
                # Insert new record
                query = text("""
                INSERT INTO """ + EMAIL_TRACKING_TABLE + """ 
                (document_no, recipient_email, email_sent, created_date, email_sent_date)
                VALUES (:doc_no, :recipient, :email_sent, GETDATE(), CASE WHEN :email_sent = '1' THEN GETDATE() ELSE NULL END)
                """)
                connection.execute(query, {
                    "doc_no": document_no, 
                    "recipient": recipient_email, 
                    "email_sent": str(email_sent)
                })
                
            connection.commit()
    except Exception as e:
        print(f"Warning: Could not track email status: {e}")

def get_purchase_requests(status=None, email_sent=None):
    """
    Get purchase requests with optional filters
    
    Args:
        status: Filter by status (0=Draft, 1=Approved, 2=Pending)
        email_sent: Filter by email sent status (None=All, True=Sent, False=Not Sent)
        
    Returns:
        List of purchase request records
    """
    query = f"SELECT * FROM {PURCHASE_REQ_TABLE}"
    params = {}
    conditions = []
    
    if status is not None:
        conditions.append("[Status] = :status")
        params["status"] = str(status)
        
    # Add where clause if conditions exist
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    # Execute query
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute(text(query), params).fetchall()
        
    return result

def get_status_text(status_code):
    """Convert status code to text"""
    status_map = {
        0: "Draft",
        1: "Approved", 
        2: "Pending",
        3: "Rejected"
    }
    return status_map.get(status_code, f"Unknown ({status_code})")

def send_approval_email(purchase_req):
    """Send approval email for a purchase requisition"""
    try:
        # Email configuration
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        
        if not all([smtp_server, smtp_user, smtp_password]):
            print("Email configuration incomplete")
            return False
            
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = purchase_req.get('approver_mailid', '')
        msg['Subject'] = f"Purchase Requisition {purchase_req.get('No_', '')} - Approval Required"
        
        # Email body
        body = f"""
        Dear Approver,
        
        A new purchase requisition requires your approval:
        
        Document No: {purchase_req.get('No_', '')}
        Employee: {purchase_req.get('Employee Name', '')}
        Department: {purchase_req.get('Indenting Department', '')}
        Request Date: {purchase_req.get('Request Date', '')}
        
        Please review and approve/reject this request.
        
        Best regards,
        Transpek System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            
        # Track email
        track_email(purchase_req.get('No_', ''), purchase_req.get('approver_mailid', ''), 1)
        
        print(f"Approval email sent for document {purchase_req.get('No_', '')}")
        return True
        
    except Exception as e:
        print(f"Error sending approval email: {e}")
        return False

def send_pending_approval_emails():
    """Send emails for all pending approval requests"""
    try:
        # Get pending requests
        pending_requests = get_purchase_requests(status=2)
        
        for req in pending_requests:
            if req.get('approver_mailid'):
                send_approval_email(req)
                
        print(f"Processed {len(pending_requests)} pending approval requests")
        
    except Exception as e:
        print(f"Error processing pending approval emails: {e}")

def get_email_tracking_data():
    """Get email tracking data"""
    try:
        engine = get_engine()
        with engine.connect() as connection:
            query = text(f"SELECT * FROM {EMAIL_TRACKING_TABLE}")
            result = connection.execute(query).fetchall()
            return result
    except Exception as e:
        print(f"Error getting email tracking data: {e}")
        return []

def get_table_schema(table_name):
    """Get the schema of a table"""
    try:
        # Clean table name
        clean_table_name = table_name.replace('[', '').replace(']', '')
        if '.' in clean_table_name:
            parts = clean_table_name.split('.')
            schema_name = parts[0]
            pure_table_name = parts[1]
        else:
            # If no schema specified, use dbo
            schema_name = 'dbo'
            pure_table_name = clean_table_name
        
        # Query to get column information
        query = text("""
        SELECT 
            c.name AS column_name, 
            t.name AS data_type,
            c.max_length,
            c.precision,
            c.scale,
            c.is_nullable
        FROM sys.columns c
        JOIN sys.types t ON c.user_type_id = t.user_type_id
        JOIN sys.tables tbl ON c.object_id = tbl.object_id
        JOIN sys.schemas s ON tbl.schema_id = s.schema_id
        WHERE tbl.name = :table_name
        ORDER BY c.column_id
        """)
        
        engine = get_engine()
        with engine.connect() as connection:
            result = connection.execute(query, {"table_name": pure_table_name}).fetchall()
            
            if not result:
                # Try alternate approach using INFORMATION_SCHEMA
                alt_query = text("""
                SELECT 
                    COLUMN_NAME as column_name,
                    DATA_TYPE as data_type,
                    CHARACTER_MAXIMUM_LENGTH as max_length,
                    NUMERIC_PRECISION as precision,
                    NUMERIC_SCALE as scale,
                    CASE WHEN IS_NULLABLE = 'YES' THEN 1 ELSE 0 END as is_nullable
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = :table_name
                ORDER BY ORDINAL_POSITION
                """)
                result = connection.execute(alt_query, {"table_name": pure_table_name}).fetchall()
            
            return result
    except Exception as e:
        print(f"Error getting table schema: {e}")
        return []

def print_table_schema(table_name):
    """Print the schema of a table in a readable format"""
    schema_info = get_table_schema(table_name)
    
    if not schema_info:
        print(f"Could not retrieve schema for table {table_name}")
        return
    
    print(f"\nTable: {table_name}")
    print("=" * (len(table_name) + 7))
    print(f"{'Column Name':<30} {'Data Type':<15} {'Length':<8} {'Nullable':<8}")
    print("-" * 65)
    
    for col in schema_info:
        data_type = col['data_type']
        if col['max_length'] and col['max_length'] > 0:
            if data_type in ('nvarchar', 'nchar', 'varchar', 'char'):
                # For nvarchar, the length is stored in bytes, so divide by 2
                length = col['max_length']
                if data_type.startswith('n'):  # Unicode types
                    length = length // 2
                type_info = f"{data_type}({length})"
            else:
                type_info = f"{data_type}({col['max_length']})"
        elif col['precision'] is not None and col['scale'] is not None:
            type_info = f"{data_type}({col['precision']},{col['scale']})"
        else:
            type_info = data_type
            
        nullable = "YES" if col['is_nullable'] else "NO"
        print(f"{col['column_name']:<30} {type_info:<15} {str(col['max_length']):<8} {nullable:<8}")
