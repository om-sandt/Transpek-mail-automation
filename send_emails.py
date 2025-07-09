import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pdf_generator import generate_approval_pdf

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
if not SMTP_USERNAME:
    raise ValueError("SMTP_USERNAME environment variable is required")
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
if not SMTP_PASSWORD:
    raise ValueError("SMTP_PASSWORD environment variable is required")

# Flask app URL (for approval/rejection links)
FLASK_APP_URL = os.getenv('FLASK_APP_URL', 'http://localhost:5000')

# Table configuration for monitoring
TABLE_CONFIG = {
    'approval_requests': {
        'table_name': 'approval_requests',
        'id_column': 'id',
        'data_column': 'data',
        'email_column': 'approver_email',
        'status_column': 'status',
        'pending_value': 'Pending',
        'subject_type': 'Approval Request',
        'route_prefix': 'legacy'
    },
    'job_work_report': {
        'table_name': 'job_work_report',
        'id_column': 'id',
        'data_column': '"OBJECTIVE_OF_JOB_CARD"',
        'email_column': 'approver_email',
        'status_column': '"Approved"',
        'pending_value': 0,
        'subject_type': 'Job Work Report',
        'route_prefix': 'job-work'
    },
    'im_purchase_requisition': {
        'table_name': 'im_purchase_requisition',
        'id_column': 'id',
        'data_column': '"Posting_Description"',
        'email_column': 'approver_email',
        'status_column': '"Status"',
        'pending_value': 0,
        'subject_type': 'IM Purchase Requisition',
        'route_prefix': 'im-purchase'
    }
}

def get_pending_requests():
    """Query database for pending approval requests from all configured tables"""
    engine = create_engine(DATABASE_URL)
    pending = []
    
    with engine.connect() as conn:
        for table_key, config in TABLE_CONFIG.items():
            try:
                # Build dynamic query based on configuration - only get requests where email_sent is False
                query = f"""
                    SELECT {config['id_column']}, {config['data_column']}, 
                           {config['email_column']}, '{table_key}' as source
                    FROM {config['table_name']}
                    WHERE {config['status_column']} = :pending_value 
                    AND (email_sent IS NULL OR email_sent = FALSE)
                """
                
                result = conn.execute(text(query), {'pending_value': config['pending_value']})
                table_pending = result.fetchall()
                pending.extend(table_pending)
                
                if table_pending:
                    print(f"Found {len(table_pending)} pending requests in {config['table_name']}")
                    
            except Exception as e:
                print(f"Error querying {config['table_name']}: {str(e)}")
                continue
    
    return pending

def send_approval_email(request_id, data, approver_email, source='legacy'):
    """Send approval email with PDF attachment and action buttons"""
    
    # Get table configuration
    table_config = TABLE_CONFIG.get(source, TABLE_CONFIG['approval_requests'])
    
    # Fetch actual record data for PDF generation
    engine = create_engine(DATABASE_URL)
    record_data = None
    
    with engine.connect() as conn:
        try:
            # Fetch the complete record
            query = f"""
                SELECT * FROM {table_config['table_name']}
                WHERE {table_config['id_column']} = :request_id
            """
            result = conn.execute(text(query), {'request_id': request_id})
            record = result.fetchone()
            
            if record:
                # Convert to dictionary
                columns = result.keys()
                record_data = dict(zip(columns, record))
                
        except Exception as e:
            print(f"Error fetching record data: {str(e)}")
    
    # Generate PDF with actual data
    try:
        pdf_content = generate_approval_pdf(data, request_id, source, record_data)
    except Exception as e:
        print(f"Error generating PDF for request #{request_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Create email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'{table_config["subject_type"]} #{request_id} - Action Required'
    msg['From'] = SMTP_USERNAME
    msg['To'] = approver_email
    
    # Build approval/rejection URLs based on table configuration
    approve_url = f"{FLASK_APP_URL}/quick-approve-{table_config['route_prefix']}?id={request_id}"
    reject_url = f"{FLASK_APP_URL}/quick-reject-{table_config['route_prefix']}?id={request_id}"
    
    # HTML email body with approval/rejection buttons
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; }}
            .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
            .content {{ padding: 20px; }}
            .buttons {{ text-align: center; margin: 20px 0; }}
            .btn {{ display: inline-block; padding: 12px 24px; margin: 0 10px; 
                    text-decoration: none; border-radius: 5px; font-weight: bold; }}
            .btn-approve {{ background-color: #28a745; color: white; }}
            .btn-reject {{ background-color: #dc3545; color: white; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; 
                      font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>{table_config["subject_type"]} #{request_id}</h2>
                <p>A new {table_config["subject_type"].lower()} requires your attention.</p>
            </div>
            
            <div class="content">
                <h3>Request Details:</h3>
                <p><strong>Request ID:</strong> {request_id}</p>
                <p><strong>Data:</strong></p>
                <pre style="background-color: #f8f9fa; padding: 10px; border-radius: 3px; white-space: pre-wrap;">{data[:500]}{'...' if len(data) > 500 else ''}</pre>
                
                <div class="buttons">
                    <a href="{approve_url}" class="btn btn-approve">✅ Approve</a>
                    <a href="{reject_url}" class="btn btn-reject">❌ Reject</a>
                </div>
                
                <p><em>Please click one of the buttons above to approve or reject this request. 
                A PDF document with the complete request details is attached to this email.</em></p>
            </div>
            
            <div class="footer">
                <p>This is an automated message from the Approval Workflow System.</p>
                <p>If you have any questions, please contact the system administrator.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Attach HTML content
    html_part = MIMEText(html_body, 'html')
    msg.attach(html_part)
    
    # Attach PDF
    pdf_attachment = MIMEBase('application', 'pdf')
    pdf_attachment.set_payload(pdf_content)
    encoders.encode_base64(pdf_attachment)
    pdf_attachment.add_header('Content-Disposition', 'attachment', 
                             filename=f'{table_config["subject_type"].lower().replace(" ", "_")}_{request_id}.pdf')
    msg.attach(pdf_attachment)
    
    # Send email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully to {approver_email} for {table_config['subject_type']} #{request_id}")
        return True
    except Exception as e:
        print(f"Failed to send email to {approver_email} for {table_config['subject_type']} #{request_id}: {str(e)}")
        return False

def mark_email_sent(request_id, source):
    """Mark that an email has been sent for this request"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # Get table configuration
            table_config = TABLE_CONFIG.get(source, TABLE_CONFIG['approval_requests'])
            
            # Update the email_sent flag
            update_query = f"""
                UPDATE {table_config['table_name']}
                SET email_sent = TRUE
                WHERE {table_config['id_column']} = :request_id
            """
            
            conn.execute(text(update_query), {'request_id': request_id})
            conn.commit()
            print(f"Marked email as sent for {table_config['subject_type']} #{request_id}")
            
        except Exception as e:
            print(f"Error marking email as sent for request #{request_id}: {str(e)}")
            conn.rollback()

def main():
    """Main function to process pending requests and send emails"""
    print("Starting approval workflow email processor...")
    print(f"Monitoring {len(TABLE_CONFIG)} tables: {', '.join(TABLE_CONFIG.keys())}")
    
    while True:
        try:
            # Get pending requests
            pending_requests = get_pending_requests()
            
            if pending_requests:
                print(f"Found {len(pending_requests)} total pending requests")
                
                for i, request in enumerate(pending_requests):
                    try:
                        print(f"Processing request {i+1}/{len(pending_requests)}")
                        
                        if len(request) == 4:
                            request_id, data, approver_email, source = request
                        else:
                            request_id, data, approver_email = request
                            source = 'approval_requests'
                        
                        print(f"Request ID: {request_id}, Source: {source}, Email: {approver_email}")
                        
                        if send_approval_email(request_id, data, approver_email, source):
                            mark_email_sent(request_id, source)
                        else:
                            print(f"Failed to process request #{request_id}")
                            
                    except Exception as e:
                        print(f"Error processing individual request: {str(e)}")
                        print(f"Request data: {request}")
                        import traceback
                        traceback.print_exc()
                        continue
            else:
                print("No pending requests found")
            
            # Wait before next check (5 minutes)
            print("Waiting 5 minutes before next check...")
            time.sleep(300)
            
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            import traceback
            traceback.print_exc()
            print("Waiting 1 minute before retrying...")
            time.sleep(60)

if __name__ == "__main__":
    main() 