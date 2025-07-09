from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class JobWorkReport(db.Model):
    __tablename__ = 'job_work_report'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Required fields
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    No_ = db.Column(db.String(20), nullable=False)
    AOP = db.Column(db.SmallInteger, nullable=False)  # tinyint equivalent
    OBJECTIVE_OF_JOB_CARD = db.Column(db.String(250), nullable=False)
    EXPECTED_BENEFITS = db.Column(db.String(250), nullable=False)
    COMPLETION_AFTER = db.Column(db.String(250), nullable=False)
    PREPARED = db.Column(db.String(20), nullable=False)
    PREPARED_BY_NAME = db.Column(db.String(100), nullable=False)
    CHECKED_BY = db.Column(db.String(20), nullable=False)
    CHECKED_BY_NAME = db.Column(db.String(100), nullable=False)
    Department_Name = db.Column(db.String(250), nullable=False)
    Remarks = db.Column(db.String(250), nullable=False)
    Job_Card_Type = db.Column(db.String(250), nullable=False)
    Expected_Completion = db.Column(db.DateTime, nullable=False)
    Estimated_Amount = db.Column(db.Numeric(38, 20), nullable=False)
    Sanctioned_Amount = db.Column(db.Numeric(38, 20), nullable=False)
    Completed = db.Column(db.SmallInteger, nullable=False)  # tinyint equivalent
    Approved = db.Column(db.SmallInteger, nullable=False)  # tinyint equivalent
    Technical_Completion = db.Column(db.DateTime, nullable=False)
    Commercial_Completion = db.Column(db.DateTime, nullable=False)
    Approval_Date_Time = db.Column(db.DateTime, nullable=False)
    Approver_ID = db.Column(db.String(50), nullable=False)
    Original_Approval_Date = db.Column(db.DateTime, nullable=False)
    TPT_Approval_Status = db.Column(db.Integer, nullable=False)
    TPT_Job_Type = db.Column(db.Integer, nullable=False)
    approver_email = db.Column(db.String(255), nullable=False)
    email_sent = db.Column(db.Boolean, default=False)  # Track if email was sent
    
    def __repr__(self):
        return f'<JobWorkReport {self.No_}: {self.OBJECTIVE_OF_JOB_CARD}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'No_': self.No_,
            'AOP': self.AOP,
            'OBJECTIVE_OF_JOB_CARD': self.OBJECTIVE_OF_JOB_CARD,
            'EXPECTED_BENEFITS': self.EXPECTED_BENEFITS,
            'COMPLETION_AFTER': self.COMPLETION_AFTER,
            'PREPARED': self.PREPARED,
            'PREPARED_BY_NAME': self.PREPARED_BY_NAME,
            'CHECKED_BY': self.CHECKED_BY,
            'CHECKED_BY_NAME': self.CHECKED_BY_NAME,
            'Department_Name': self.Department_Name,
            'Remarks': self.Remarks,
            'Job_Card_Type': self.Job_Card_Type,
            'Expected_Completion': self.Expected_Completion.isoformat() if self.Expected_Completion else None,
            'Estimated_Amount': float(self.Estimated_Amount) if self.Estimated_Amount else None,
            'Sanctioned_Amount': float(self.Sanctioned_Amount) if self.Sanctioned_Amount else None,
            'Completed': self.Completed,
            'Approved': self.Approved,
            'Technical_Completion': self.Technical_Completion.isoformat() if self.Technical_Completion else None,
            'Commercial_Completion': self.Commercial_Completion.isoformat() if self.Commercial_Completion else None,
            'Approval_Date_Time': self.Approval_Date_Time.isoformat() if self.Approval_Date_Time else None,
            'Approver_ID': self.Approver_ID,
            'Original_Approval_Date': self.Original_Approval_Date.isoformat() if self.Original_Approval_Date else None,
            'TPT_Approval_Status': self.TPT_Approval_Status,
            'TPT_Job_Type': self.TPT_Job_Type,
            'approver_email': self.approver_email
        }

class IMPurchaseRequisition(db.Model):
    __tablename__ = 'im_purchase_requisition'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Required fields
    Document_Type = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    No = db.Column(db.Integer, nullable=False)
    Employee_No = db.Column(db.String(20), nullable=False)
    Employee_Name = db.Column(db.String(20), nullable=False)
    Your_Reference = db.Column(db.String(50), nullable=False)
    Request_Date = db.Column(db.String(30), nullable=False)
    Posting_Date = db.Column(db.DateTime, nullable=False)
    Expected_Receipt_Date = db.Column(db.DateTime, nullable=False)
    Posting_Description = db.Column(db.String(50), nullable=False)
    Due_Date = db.Column(db.DateTime, nullable=False)
    Location_Code = db.Column(db.String(10), nullable=False)
    Shortcut_Dimension_1 = db.Column(db.String(20), nullable=False)
    Shortcut_Dimension_2 = db.Column(db.String(20), nullable=False)
    Shortcut_Dimension_3 = db.Column(db.String(20), nullable=False)
    Comment = db.Column(db.String(100), nullable=False)
    Posting_No = db.Column(db.SmallInteger, nullable=False)  # tinyint equivalent
    Last_Posting_No = db.Column(db.String(20), nullable=False)
    Reason_Code = db.Column(db.String(20), nullable=False)
    Gen_Bus_Posting_Group = db.Column(db.String(10), nullable=False)
    Document_Date = db.Column(db.DateTime, nullable=False)
    NO_Series = db.Column(db.String(10), nullable=False)
    Posting_No_Series = db.Column(db.String(10), nullable=False)
    Status = db.Column(db.Integer, nullable=False)
    Dimension_Set_ID = db.Column(db.Integer, nullable=False)
    Responsibility_Center = db.Column(db.String(10), nullable=False)
    Assigned_User_ID = db.Column(db.String(50), nullable=False)
    Posted = db.Column(db.Integer, nullable=False)
    Purchase_Type = db.Column(db.String(100), nullable=False)
    Indenting_Department = db.Column(db.String(10), nullable=False)
    Employee_Department = db.Column(db.SmallInteger, nullable=False)  # tinyint equivalent
    Type_of_Jobwork = db.Column(db.Integer, nullable=False)
    Capital_Item_Premises = db.Column(db.String(10), nullable=False)
    Shortcut_Dimension_3_Code = db.Column(db.String(20), nullable=False)
    Shortcut_Dimension_6_Code = db.Column(db.String(20), nullable=False)
    Indent_Type = db.Column(db.Integer, nullable=False)
    Approved_By = db.Column(db.String(250), nullable=False)
    Approved_Date = db.Column(db.DateTime, nullable=False)
    Approved_Time = db.Column(db.DateTime, nullable=False)
    Job_Card_No = db.Column(db.String(20), nullable=False)
    Job_Card_Date = db.Column(db.DateTime, nullable=False)
    Job_Task_NO = db.Column(db.String(20), nullable=False)
    Approved_By_Account = db.Column(db.SmallInteger, nullable=False)  # tinyint equivalent
    SystemId = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), nullable=False)
    SystemCreatedAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    SystemCreatedBy = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), nullable=False)
    SystemModifiedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    SystemModifiedBy = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), nullable=False)
    approver_email = db.Column(db.String(255), nullable=False)
    email_sent = db.Column(db.Boolean, default=False)  # Track if email was sent
    
    def __repr__(self):
        return f'<IMPurchaseRequisition {self.No}: {self.Employee_Name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'Document_Type': self.Document_Type.isoformat() if self.Document_Type else None,
            'No': self.No,
            'Employee_No': self.Employee_No,
            'Employee_Name': self.Employee_Name,
            'Your_Reference': self.Your_Reference,
            'Request_Date': self.Request_Date,
            'Posting_Date': self.Posting_Date.isoformat() if self.Posting_Date else None,
            'Expected_Receipt_Date': self.Expected_Receipt_Date.isoformat() if self.Expected_Receipt_Date else None,
            'Posting_Description': self.Posting_Description,
            'Due_Date': self.Due_Date.isoformat() if self.Due_Date else None,
            'Location_Code': self.Location_Code,
            'Shortcut_Dimension_1': self.Shortcut_Dimension_1,
            'Shortcut_Dimension_2': self.Shortcut_Dimension_2,
            'Shortcut_Dimension_3': self.Shortcut_Dimension_3,
            'Comment': self.Comment,
            'Posting_No': self.Posting_No,
            'Last_Posting_No': self.Last_Posting_No,
            'Reason_Code': self.Reason_Code,
            'Gen_Bus_Posting_Group': self.Gen_Bus_Posting_Group,
            'Document_Date': self.Document_Date.isoformat() if self.Document_Date else None,
            'NO_Series': self.NO_Series,
            'Posting_No_Series': self.Posting_No_Series,
            'Status': self.Status,
            'Dimension_Set_ID': self.Dimension_Set_ID,
            'Responsibility_Center': self.Responsibility_Center,
            'Assigned_User_ID': self.Assigned_User_ID,
            'Posted': self.Posted,
            'Purchase_Type': self.Purchase_Type,
            'Indenting_Department': self.Indenting_Department,
            'Employee_Department': self.Employee_Department,
            'Type_of_Jobwork': self.Type_of_Jobwork,
            'Capital_Item_Premises': self.Capital_Item_Premises,
            'Shortcut_Dimension_3_Code': self.Shortcut_Dimension_3_Code,
            'Shortcut_Dimension_6_Code': self.Shortcut_Dimension_6_Code,
            'Indent_Type': self.Indent_Type,
            'Approved_By': self.Approved_By,
            'Approved_Date': self.Approved_Date.isoformat() if self.Approved_Date else None,
            'Approved_Time': self.Approved_Time.isoformat() if self.Approved_Time else None,
            'Job_Card_No': self.Job_Card_No,
            'Job_Card_Date': self.Job_Card_Date.isoformat() if self.Job_Card_Date else None,
            'Job_Task_NO': self.Job_Task_NO,
            'Approved_By_Account': self.Approved_By_Account,
            'SystemId': self.SystemId,
            'SystemCreatedAt': self.SystemCreatedAt.isoformat() if self.SystemCreatedAt else None,
            'SystemCreatedBy': self.SystemCreatedBy,
            'SystemModifiedAt': self.SystemModifiedAt.isoformat() if self.SystemModifiedAt else None,
            'SystemModifiedBy': self.SystemModifiedBy,
            'approver_email': self.approver_email
        }

# Keep the old ApprovalRequest model for backward compatibility
class ApprovalRequest(db.Model):
    __tablename__ = 'approval_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    approver_email = db.Column(db.String(255), nullable=False)
    reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<ApprovalRequest {self.id}: {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'data': self.data,
            'status': self.status,
            'approver_email': self.approver_email,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 