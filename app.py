from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, IMPurchaseRequisition
from db_utils import insert_im_purchase_req, setup_database
from dotenv import load_dotenv
import os
from datetime import datetime
import re  # Import re for regular expressions

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

@app.route('/')
def index():
    """Home page with navigation to different sections"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        if setup_database():
            return jsonify({"status": "healthy", "database": "connected"})
        else:
            return jsonify({"status": "unhealthy", "database": "disconnected"}), 500
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/im-purchase-requisitions')
def im_purchase_requisitions():
    """List all IM purchase requisitions"""
    requisitions = IMPurchaseRequisition.query.order_by(IMPurchaseRequisition.Request_Date.desc()).all()
    return render_template('im_purchase_requisitions.html', requisitions=requisitions)

@app.route('/submit-im-purchase', methods=['GET', 'POST'])
def submit_im_purchase():
    """Submit a new IM purchase requisition"""
    if request.method == 'POST':
        try:
            # Validate required fields
            required_fields = [
                'Employee_No', 'Employee_Name', 'approver_email',
                'Posting_Description', 'Purchase_Type', 'Indenting_Department'
            ]
            for field in required_fields:
                if not request.form.get(field):
                    raise ValueError(f"Missing required field: {field}")
            
            # Prepare data for database insertion using the exact format
            data = {
                "$systemCreatedAt": datetime.now().isoformat() + "Z",
                "$systemCreatedBy": "00000000-0000-0000-0000-000000000000",
                "$systemId": "00000000-0000-0000-0000-000000000000",
                "$systemModifiedAt": datetime.now().isoformat() + "Z",
                "$systemModifiedBy": "00000000-0000-0000-0000-000000000000",
                "Approved By": request.form.get('Approved_By', ''),
                "Approved By Account Dept_": int(request.form.get('Approved_By_Account', 0)),
                "Approved Date": "1753-01-01T00:00:00.000Z",
                "Approved Time": "1753-01-01T00:00:00.000Z",
                "Assigned User ID": request.form.get('Assigned_User_ID', ''),
                "Capital Item Premises": int(request.form.get('Capital_Item_Premises', 0)),
                "Comment": int(request.form.get('Comment', 0)),
                "Dimension Set ID": int(request.form.get('Dimension_Set_ID', 0)),
                "Document Date": request.form.get('Document_Date', ''),
                "Document Type": int(request.form.get('Document_Type', 0)),
                "Due Date": request.form.get('Due_Date', ''),
                "Employee Department": request.form.get('Employee_Department', ''),
                "Employee Name": request.form.get('Employee_Name', ''),
                "Employee No_": request.form.get('Employee_No', ''),
                "Expected Receipt Date": request.form.get('Expected_Receipt_Date', ''),
                "Gen_ Bus_ Posting Group": request.form.get('Gen_Bus_Posting_Group', ''),
                "Indent Type": int(request.form.get('Indent_Type', 0)),
                "Indenting Department": request.form.get('Indenting_Department', ''),
                "Job Card Date": "1753-01-01T00:00:00.000Z",
                "Job Card No_": request.form.get('Job_Card_No', ''),
                "Job Task No_": request.form.get('Job_Task_NO', ''),
                "Last Posting No_": request.form.get('Last_Posting_No', ''),
                "Location Code": request.form.get('Location_Code', ''),
                "No_": request.form.get('No_', ''),
                "No_ Series": request.form.get('NO_Series', ''),
                "Posted": int(request.form.get('Posted', 0)),
                "Posting Date": request.form.get('Posting_Date', ''),
                "Posting Description": request.form.get('Posting_Description', ''),
                "Posting No_": request.form.get('Posting_No', ''),
                "Posting No_ Series": request.form.get('Posting_No_Series', ''),
                "Purchase Type": int(request.form.get('Purchase_Type', 0)),
                "Reason Code": request.form.get('Reason_Code', ''),
                "Request Date": request.form.get('Request_Date', ''),
                "Responsibility Center": request.form.get('Responsibility_Center', ''),
                "Shortcut Dimension 1 Code": request.form.get('Shortcut_Dimension_1', ''),
                "Shortcut Dimension 2 Code": request.form.get('Shortcut_Dimension_2', ''),
                "Shortcut Dimension 2 Value": request.form.get('Indenting_Department', ''),
                "Shortcut Dimension 3 Code": request.form.get('Shortcut_Dimension_3_Code', ''),
                "Shortcut Dimension 6 Code": request.form.get('Shortcut_Dimension_6_Code', ''),
                "Status": 2,  # Pending
                "Type of Jobwork": int(request.form.get('Type_of_Jobwork', 0)),
                "Your Reference": request.form.get('Your_Reference', ''),
                "approver_mailid": request.form.get('approver_email', ''),
                "email_send": None,
                "status": None,
                "timestamp": bytes.fromhex("00000000433780fd")
            }
            
            # Insert data using the db_utils function
            success = insert_im_purchase_req(data)
            
            if success:
                flash(f'IM Purchase Requisition #{data["No_"]} submitted successfully!', 'success')
                return redirect(url_for('im_purchase_requisitions'))
            else:
                flash('Error submitting IM purchase requisition: Database insertion failed', 'error')
                return render_template('submit_im_purchase.html')
            
        except Exception as e:
            flash(f'Error submitting IM purchase requisition: {str(e)}', 'error')
            return render_template('submit_im_purchase.html')
    
    return render_template('submit_im_purchase.html')

@app.route('/api/im-purchase-requisitions')
def api_im_purchase_requisitions():
    """API endpoint to get all IM purchase requisitions"""
    requisitions = IMPurchaseRequisition.query.order_by(IMPurchaseRequisition.Request_Date.desc()).all()
    return jsonify([req.to_dict() for req in requisitions])

@app.route('/quick-approve-im-purchase')
def quick_approve_im_purchase():
    """Show quick approval modal for IM purchase requisition"""
    request_id = request.args.get('id')
    if not request_id:
        return render_template('quick_modal.html', error='Request ID is required!')
    
    requisition = IMPurchaseRequisition.query.get(request_id)
    if not requisition:
        return render_template('quick_modal.html', error='IM Purchase Requisition not found!')
    
    return render_template('quick_approve_im_purchase.html', requisition=requisition)

@app.route('/quick-reject-im-purchase')
def quick_reject_im_purchase():
    """Show quick rejection modal for IM purchase requisition"""
    request_id = request.args.get('id')
    if not request_id:
        return render_template('quick_modal.html', error='Request ID is required!')
    
    requisition = IMPurchaseRequisition.query.get(request_id)
    if not requisition:
        return render_template('quick_modal.html', error='IM Purchase Requisition not found!')
    
    return render_template('quick_reject_im_purchase.html', requisition=requisition)

@app.route('/process-im-purchase', methods=['POST'])
def process_im_purchase():
    """Process IM purchase requisition approval/rejection"""
    request_id = request.form.get('request_id')
    action = request.form.get('action')  # 'approve' or 'reject'
    reason = request.form.get('reason', '')
    
    if not request_id or not action:
        flash('Missing required parameters!', 'error')
        return redirect(url_for('im_purchase_requisitions'))
    
    try:
        requisition = IMPurchaseRequisition.query.get(request_id)
        if not requisition:
            flash('IM Purchase Requisition not found!', 'error')
            return redirect(url_for('im_purchase_requisitions'))
        
        if action == 'approve':
            # Update status to approved
            requisition.Status = 1  # Assuming 1 means approved
            requisition.Approved_Date = datetime.utcnow()
            requisition.Approved_Time = datetime.utcnow()
            flash(f'IM Purchase Requisition #{requisition.No_} approved successfully!', 'success')
        elif action == 'reject':
            # Update status to rejected
            requisition.Status = 2  # Assuming 2 means rejected
            flash(f'IM Purchase Requisition #{requisition.No_} rejected. Reason: {reason}', 'warning')
        else:
            flash('Invalid action!', 'error')
            return redirect(url_for('im_purchase_requisitions'))
        
        db.session.commit()
        return redirect(url_for('im_purchase_requisitions'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error processing IM purchase requisition: {str(e)}', 'error')
        return redirect(url_for('im_purchase_requisitions'))

@app.route('/delete-im-purchase/<request_id>', methods=['POST'])
def delete_im_purchase(request_id):
    """Delete an IM purchase requisition"""
    try:
        requisition = IMPurchaseRequisition.query.get(request_id)
        if not requisition:
            flash('IM Purchase Requisition not found!', 'error')
            return redirect(url_for('im_purchase_requisitions'))
        
        db.session.delete(requisition)
        db.session.commit()
        flash(f'IM Purchase Requisition #{requisition.No_} deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting IM purchase requisition: {str(e)}', 'error')
    
    return redirect(url_for('im_purchase_requisitions'))

def create_tables():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)