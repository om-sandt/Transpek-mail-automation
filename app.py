from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, ApprovalRequest, JobWorkReport, IMPurchaseRequisition
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

@app.route('/job-work-reports')
def job_work_reports():
    """List all job work reports"""
    reports = JobWorkReport.query.order_by(JobWorkReport.timestamp.desc()).all()
    return render_template('job_work_reports.html', reports=reports)

@app.route('/im-purchase-requisitions')
def im_purchase_requisitions():
    """List all IM purchase requisitions"""
    requisitions = IMPurchaseRequisition.query.order_by(IMPurchaseRequisition.Document_Type.desc()).all()
    return render_template('im_purchase_requisitions.html', requisitions=requisitions)

@app.route('/submit-job-work', methods=['GET', 'POST'])
def submit_job_work():
    """Submit a new job work report"""
    if request.method == 'POST':
        try:
            # Create new job work report
            new_report = JobWorkReport()
            new_report.No_ = request.form.get('No_')
            new_report.AOP = int(request.form.get('AOP', 0))
            new_report.OBJECTIVE_OF_JOB_CARD = request.form.get('OBJECTIVE_OF_JOB_CARD')
            new_report.EXPECTED_BENEFITS = request.form.get('EXPECTED_BENEFITS')
            new_report.COMPLETION_AFTER = request.form.get('COMPLETION_AFTER')
            new_report.PREPARED = request.form.get('PREPARED')
            new_report.PREPARED_BY_NAME = request.form.get('PREPARED_BY_NAME')
            new_report.CHECKED_BY = request.form.get('CHECKED_BY')
            new_report.CHECKED_BY_NAME = request.form.get('CHECKED_BY_NAME')
            new_report.Department_Name = request.form.get('Department_Name')
            new_report.Remarks = request.form.get('Remarks')
            new_report.Job_Card_Type = request.form.get('Job_Card_Type')
            expected_completion = request.form.get('Expected_Completion')
            new_report.Expected_Completion = datetime.fromisoformat(expected_completion) if expected_completion else datetime.utcnow()
            new_report.Estimated_Amount = float(request.form.get('Estimated_Amount', 0))
            new_report.Sanctioned_Amount = float(request.form.get('Sanctioned_Amount', 0))
            new_report.Completed = int(request.form.get('Completed', 0))
            new_report.Approved = int(request.form.get('Approved', 0))
            technical_completion = request.form.get('Technical_Completion')
            new_report.Technical_Completion = datetime.fromisoformat(technical_completion) if technical_completion else datetime.utcnow()
            commercial_completion = request.form.get('Commercial_Completion')
            new_report.Commercial_Completion = datetime.fromisoformat(commercial_completion) if commercial_completion else datetime.utcnow()
            approval_date_time = request.form.get('Approval_Date_Time')
            new_report.Approval_Date_Time = datetime.fromisoformat(approval_date_time) if approval_date_time else datetime.utcnow()
            new_report.Approver_ID = request.form.get('Approver_ID')
            original_approval_date = request.form.get('Original_Approval_Date')
            new_report.Original_Approval_Date = datetime.fromisoformat(original_approval_date) if original_approval_date else datetime.utcnow()
            new_report.TPT_Approval_Status = int(request.form.get('TPT_Approval_Status', 0))
            new_report.TPT_Job_Type = int(request.form.get('TPT_Job_Type', 0))
            new_report.approver_email = request.form.get('approver_email')
            
            db.session.add(new_report)
            db.session.commit()
            flash(f'Job Work Report #{new_report.No_} submitted successfully!', 'success')
            return redirect(url_for('job_work_reports'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting job work report: {str(e)}', 'error')
            return render_template('submit_job_work.html')
    
    return render_template('submit_job_work.html')

@app.route('/submit-im-purchase', methods=['GET', 'POST'])
def submit_im_purchase():
    """Submit a new IM purchase requisition"""
    if request.method == 'POST':
        try:
            # Create new IM purchase requisition
            new_requisition = IMPurchaseRequisition()
            new_requisition.No = int(request.form.get('No', 0))
            new_requisition.Employee_No = request.form.get('Employee_No')
            new_requisition.Employee_Name = request.form.get('Employee_Name')
            new_requisition.Your_Reference = request.form.get('Your_Reference')
            new_requisition.Request_Date = request.form.get('Request_Date')
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
            flash(f'IM Purchase Requisition #{new_requisition.No} submitted successfully!', 'success')
            return redirect(url_for('im_purchase_requisitions'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting IM purchase requisition: {str(e)}', 'error')
            return render_template('submit_im_purchase.html')
    
    return render_template('submit_im_purchase.html')

# Legacy routes for backward compatibility
@app.route('/legacy')
def legacy_index():
    """Legacy home page with list of all approval requests"""
    requests = ApprovalRequest.query.order_by(ApprovalRequest.created_at.desc()).all()
    return render_template('legacy_index.html', requests=requests)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """Submit a new approval request (legacy)"""
    if request.method == 'POST':
        data = request.form.get('data')
        approver_email = request.form.get('approver_email')
        
        if not data or not approver_email:
            flash('Both data and approver email are required!', 'error')
            return render_template('submit.html')
        
        # Create new approval request
        new_request = ApprovalRequest()
        new_request.data = data
        new_request.approver_email = approver_email
        new_request.status = 'Pending'
        
        try:
            db.session.add(new_request)
            db.session.commit()
            flash(f'Approval request #{new_request.id} submitted successfully!', 'success')
            return redirect(url_for('legacy_index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting request: {str(e)}', 'error')
            return render_template('submit.html')
    
    return render_template('submit.html')

@app.route('/quick-approve')
def quick_approve():
    """Show quick approval modal"""
    request_id = request.args.get('id')
    if not request_id:
        return render_template('quick_modal.html', error='Request ID is required!')
    
    approval_request = ApprovalRequest.query.get(request_id)
    if not approval_request:
        return render_template('quick_modal.html', error='Approval request not found!')
    
    if approval_request.status != 'Pending':
        return render_template('quick_modal.html', error='This request has already been processed!')
    
    return render_template('quick_approve.html', request=approval_request)

@app.route('/quick-reject')
def quick_reject():
    """Show quick rejection modal"""
    request_id = request.args.get('id')
    if not request_id:
        return render_template('quick_modal.html', error='Request ID is required!')
    
    approval_request = ApprovalRequest.query.get(request_id)
    if not approval_request:
        return render_template('quick_modal.html', error='Approval request not found!')
    
    if approval_request.status != 'Pending':
        return render_template('quick_modal.html', error='This request has already been processed!')
    
    return render_template('quick_reject.html', request=approval_request)

@app.route('/process', methods=['POST'])
def process():
    """Process approval or rejection"""
    request_id = request.form.get('request_id')
    status = request.form.get('status')
    reason = request.form.get('reason', '')
    
    if not request_id or not status:
        flash('Request ID and status are required!', 'error')
        return redirect(url_for('legacy_index'))
    
    if status not in ['Approved', 'Rejected']:
        flash('Invalid status!', 'error')
        return redirect(url_for('legacy_index'))
    
    # Validate reason for rejection
    if status == 'Rejected' and not reason.strip():
        flash('Reason is required for rejection!', 'error')
        return redirect(url_for('reject', id=request_id))
    
    approval_request = ApprovalRequest.query.get(request_id)
    if not approval_request:
        flash('Approval request not found!', 'error')
        return redirect(url_for('legacy_index'))
    
    if approval_request.status != 'Pending':
        flash('This request has already been processed!', 'error')
        return redirect(url_for('legacy_index'))
    
    # Update the request
    approval_request.status = status
    approval_request.reason = reason if reason.strip() else None
    
    try:
        db.session.commit()
        status_emoji = '✅' if status == 'Approved' else '❌'
        flash(f'{status_emoji} Request #{request_id} has been {status.lower()}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error processing request: {str(e)}', 'error')
    
    return redirect(url_for('legacy_index'))

@app.route('/api/requests')
def api_requests():
    """API endpoint to get all requests"""
    requests = ApprovalRequest.query.order_by(ApprovalRequest.created_at.desc()).all()
    return jsonify([req.to_dict() for req in requests])

@app.route('/api/requests/<int:request_id>')
def api_request_detail(request_id):
    """API endpoint to get a specific request"""
    approval_request = ApprovalRequest.query.get(request_id)
    if not approval_request:
        return jsonify({'error': 'Request not found'}), 404
    return jsonify(approval_request.to_dict())

@app.route('/api/job-work-reports')
def api_job_work_reports():
    """API endpoint to get all job work reports"""
    reports = JobWorkReport.query.order_by(JobWorkReport.timestamp.desc()).all()
    return jsonify([report.to_dict() for report in reports])

@app.route('/api/im-purchase-requisitions')
def api_im_purchase_requisitions():
    """API endpoint to get all IM purchase requisitions"""
    requisitions = IMPurchaseRequisition.query.order_by(IMPurchaseRequisition.Document_Type.desc()).all()
    return jsonify([req.to_dict() for req in requisitions])

@app.route('/quick-approve-job-work')
def quick_approve_job_work():
    """Show quick approval modal for job work report"""
    request_id = request.args.get('id')
    if not request_id:
        return render_template('quick_modal.html', error='Request ID is required!')
    
    job_work = JobWorkReport.query.get(request_id)
    if not job_work:
        return render_template('quick_modal.html', error='Job work report not found!')
    
    if job_work.Approved != 0:
        return render_template('quick_modal.html', error='This job work report has already been processed!')
    
    return render_template('quick_approve_job_work.html', job_work=job_work)

@app.route('/quick-reject-job-work')
def quick_reject_job_work():
    """Show quick rejection modal for job work report"""
    request_id = request.args.get('id')
    if not request_id:
        return render_template('quick_modal.html', error='Request ID is required!')
    
    job_work = JobWorkReport.query.get(request_id)
    if not job_work:
        return render_template('quick_modal.html', error='Job work report not found!')
    
    if job_work.Approved != 0:
        return render_template('quick_modal.html', error='This job work report has already been processed!')
    
    return render_template('quick_reject_job_work.html', job_work=job_work)

@app.route('/quick-approve-im-purchase')
def quick_approve_im_purchase():
    """Show quick approval modal for IM purchase requisition"""
    request_id = request.args.get('id')
    if not request_id:
        return render_template('quick_modal.html', error='Request ID is required!')
    
    im_purchase = IMPurchaseRequisition.query.get(request_id)
    if not im_purchase:
        return render_template('quick_modal.html', error='IM purchase requisition not found!')
    
    if im_purchase.Status != 0:
        return render_template('quick_modal.html', error='This IM purchase requisition has already been processed!')
    
    return render_template('quick_approve_im_purchase.html', im_purchase=im_purchase)

@app.route('/quick-reject-im-purchase')
def quick_reject_im_purchase():
    """Show quick rejection modal for IM purchase requisition"""
    request_id = request.args.get('id')
    if not request_id:
        return render_template('quick_modal.html', error='Request ID is required!')
    
    im_purchase = IMPurchaseRequisition.query.get(request_id)
    if not im_purchase:
        return render_template('quick_modal.html', error='IM purchase requisition not found!')
    
    if im_purchase.Status != 0:
        return render_template('quick_modal.html', error='This IM purchase requisition has already been processed!')
    
    return render_template('quick_reject_im_purchase.html', im_purchase=im_purchase)

@app.route('/process-job-work', methods=['POST'])
def process_job_work():
    """Process job work report approval or rejection"""
    request_id = request.form.get('request_id')
    status = request.form.get('status')
    reason = request.form.get('reason', '')
    
    if not request_id or not status:
        flash('Request ID and status are required!', 'error')
        return redirect(url_for('job_work_reports'))
    
    if status not in ['Approved', 'Rejected']:
        flash('Invalid status!', 'error')
        return redirect(url_for('job_work_reports'))
    
    # Validate reason for rejection
    if status == 'Rejected' and not reason.strip():
        flash('Reason is required for rejection!', 'error')
        return redirect(url_for('quick_reject_job_work', id=request_id))
    
    job_work = JobWorkReport.query.get(request_id)
    if not job_work:
        flash('Job work report not found!', 'error')
        return redirect(url_for('job_work_reports'))
    
    if job_work.Approved != 0:
        flash('This job work report has already been processed!', 'error')
        return redirect(url_for('job_work_reports'))
    
    # Update the job work report
    job_work.Approved = 1 if status == 'Approved' else 2
    job_work.Remarks = reason if reason.strip() else job_work.Remarks
    
    try:
        db.session.commit()
        status_emoji = '✅' if status == 'Approved' else '❌'
        return f'{status_emoji} Job Work Report #{request_id} has been {status.lower()}!'
    except Exception as e:
        db.session.rollback()
        return f'Error processing job work report: {str(e)}'

@app.route('/process-im-purchase', methods=['POST'])
def process_im_purchase():
    """Process IM purchase requisition approval or rejection"""
    request_id = request.form.get('request_id')
    status = request.form.get('status')
    reason = request.form.get('reason', '')
    
    if not request_id or not status:
        flash('Request ID and status are required!', 'error')
        return redirect(url_for('im_purchase_requisitions'))
    
    if status not in ['Approved', 'Rejected']:
        flash('Invalid status!', 'error')
        return redirect(url_for('im_purchase_requisitions'))
    
    # Validate reason for rejection
    if status == 'Rejected' and not reason.strip():
        flash('Reason is required for rejection!', 'error')
        return redirect(url_for('quick_reject_im_purchase', id=request_id))
    
    im_purchase = IMPurchaseRequisition.query.get(request_id)
    if not im_purchase:
        flash('IM purchase requisition not found!', 'error')
        return redirect(url_for('im_purchase_requisitions'))
    
    if im_purchase.Status != 0:
        flash('This IM purchase requisition has already been processed!', 'error')
        return redirect(url_for('im_purchase_requisitions'))
    
    # Update the IM purchase requisition
    im_purchase.Status = 1 if status == 'Approved' else 2
    im_purchase.Comment = reason if reason.strip() else im_purchase.Comment
    
    try:
        db.session.commit()
        status_emoji = '✅' if status == 'Approved' else '❌'
        return f'{status_emoji} IM Purchase Requisition #{request_id} has been {status.lower()}!'
    except Exception as e:
        db.session.rollback()
        return f'Error processing IM purchase requisition: {str(e)}'

@app.route('/delete-job-work/<int:request_id>', methods=['POST'])
def delete_job_work(request_id):
    """Delete a job work report"""
    job_work = JobWorkReport.query.get(request_id)
    if not job_work:
        flash('Job work report not found!', 'error')
        return redirect(url_for('job_work_reports'))
    
    try:
        db.session.delete(job_work)
        db.session.commit()
        flash(f'Job Work Report #{request_id} has been deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting job work report: {str(e)}', 'error')
    
    return redirect(url_for('job_work_reports'))

@app.route('/delete-im-purchase/<int:request_id>', methods=['POST'])
def delete_im_purchase(request_id):
    """Delete an IM purchase requisition"""
    im_purchase = IMPurchaseRequisition.query.get(request_id)
    if not im_purchase:
        flash('IM purchase requisition not found!', 'error')
        return redirect(url_for('im_purchase_requisitions'))
    
    try:
        db.session.delete(im_purchase)
        db.session.commit()
        flash(f'IM Purchase Requisition #{request_id} has been deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting IM purchase requisition: {str(e)}', 'error')
    
    return redirect(url_for('im_purchase_requisitions'))

@app.route('/delete-approval-request/<int:request_id>', methods=['POST'])
def delete_approval_request(request_id):
    """Delete a legacy approval request"""
    approval_request = ApprovalRequest.query.get(request_id)
    if not approval_request:
        flash('Approval request not found!', 'error')
        return redirect(url_for('index'))
    
    try:
        db.session.delete(approval_request)
        db.session.commit()
        flash(f'Approval Request #{request_id} has been deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting approval request: {str(e)}', 'error')
    
    return redirect(url_for('index'))

def create_tables():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    # Create tables if they don't exist
    create_tables()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000) 