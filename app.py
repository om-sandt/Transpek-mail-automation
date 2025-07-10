from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, IMPurchaseRequisition
from dotenv import load_dotenv
import os
from datetime import datetime

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
            # Create new IM purchase requisition
            new_requisition = IMPurchaseRequisition()
            new_requisition.timestamp = request.form.get('timestamp')
            new_requisition.Document_Type = int(request.form.get('Document_Type', 0))
            new_requisition.No_ = request.form.get('No_')
            new_requisition.Employee_No = int(request.form.get('Employee_No', 0))
            new_requisition.Employee_Name = request.form.get('Employee_Name')
            new_requisition.Your_Reference = request.form.get('Your_Reference')
            request_date = request.form.get('Request_Date')
            new_requisition.Request_Date = datetime.fromisoformat(request_date) if request_date else datetime.utcnow()
            posting_date = request.form.get('Posting_Date')
            new_requisition.Posting_Date = datetime.fromisoformat(posting_date) if posting_date else datetime.utcnow()
            expected_receipt_date = request.form.get('Expected_Receipt_Date')
            new_requisition.Expected_Receipt_Date = datetime.fromisoformat(expected_receipt_date) if expected_receipt_date else datetime.utcnow()
            new_requisition.Posting_Description = request.form.get('Posting_Description')
            due_date = request.form.get('Due_Date')
            new_requisition.Due_Date = datetime.fromisoformat(due_date) if due_date else datetime.utcnow()
            new_requisition.Location_Code = request.form.get('Location_Code')
            new_requisition.Shortcut_Dimension_1 = request.form.get('Shortcut_Dimension_1')
            new_requisition.Shortcut_Dimension_2 = request.form.get('Shortcut_Dimension_2')
            new_requisition.Shortcut_Dimension_3 = request.form.get('Shortcut_Dimension_3')
            new_requisition.Comment = request.form.get('Comment')
            new_requisition.Posting_No = int(request.form.get('Posting_No', 0))
            new_requisition.Last_Posting_No = request.form.get('Last_Posting_No')
            new_requisition.Reason_Code = request.form.get('Reason_Code')
            new_requisition.Gen_Bus_Posting_Group = request.form.get('Gen_Bus_Posting_Group')
            document_date = request.form.get('Document_Date')
            new_requisition.Document_Date = datetime.fromisoformat(document_date) if document_date else datetime.utcnow()
            new_requisition.NO_Series = request.form.get('NO_Series')
            new_requisition.Posting_No_Series = request.form.get('Posting_No_Series')
            new_requisition.Status = int(request.form.get('Status', 0))
            new_requisition.Dimension_Set_ID = int(request.form.get('Dimension_Set_ID', 0))
            new_requisition.Responsibility_Center = request.form.get('Responsibility_Center')
            new_requisition.Assigned_User_ID = request.form.get('Assigned_User_ID')
            new_requisition.Posted = int(request.form.get('Posted', 0))
            new_requisition.Purchase_Type = request.form.get('Purchase_Type')
            new_requisition.Indenting_Department = request.form.get('Indenting_Department')
            new_requisition.Employee_Department = int(request.form.get('Employee_Department', 0))
            new_requisition.Type_of_Jobwork = int(request.form.get('Type_of_Jobwork', 0))
            new_requisition.Capital_Item_Premises = request.form.get('Capital_Item_Premises')
            new_requisition.Shortcut_Dimension_3_Code = request.form.get('Shortcut_Dimension_3_Code')
            new_requisition.Shortcut_Dimension_6_Code = request.form.get('Shortcut_Dimension_6_Code')
            new_requisition.Indent_Type = int(request.form.get('Indent_Type', 0))
            new_requisition.Approved_By = request.form.get('Approved_By')
            approved_date = request.form.get('Approved_Date')
            new_requisition.Approved_Date = datetime.fromisoformat(approved_date) if approved_date else datetime.utcnow()
            approved_time = request.form.get('Approved_Time')
            new_requisition.Approved_Time = datetime.fromisoformat(approved_time) if approved_time else datetime.utcnow()
            new_requisition.Job_Card_No = request.form.get('Job_Card_No')
            job_card_date = request.form.get('Job_Card_Date')
            new_requisition.Job_Card_Date = datetime.fromisoformat(job_card_date) if job_card_date else datetime.utcnow()
            new_requisition.Job_Task_NO = request.form.get('Job_Task_NO')
            new_requisition.Approved_By_Account = int(request.form.get('Approved_By_Account', 0))
            new_requisition.approver_email = request.form.get('approver_email')
            
            db.session.add(new_requisition)
            db.session.commit()
            flash(f'IM Purchase Requisition #{new_requisition.No_} submitted successfully!', 'success')
            return redirect(url_for('im_purchase_requisitions'))
        except Exception as e:
            db.session.rollback()
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