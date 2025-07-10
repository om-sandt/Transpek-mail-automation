from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class IMPurchaseRequisition(db.Model):
    __tablename__ = 'Transpek Industry Limited$TPT_IM Purch_ Req_ Header$114fe92f-996b-45f1-94bb-c0d5b6ba317e'
    
    # Primary key - using the first column from the schema
    timestamp = db.Column(db.String(50), primary_key=True)
    
    # All other fields based on the provided schema
    Document_Type = db.Column(db.Integer, nullable=False)
    No_ = db.Column(db.String(50), nullable=False)
    Employee_No = db.Column(db.Integer, nullable=False)
    Employee_Name = db.Column(db.String(255), nullable=False)
    Your_Reference = db.Column(db.String(255), nullable=False)
    Request_Date = db.Column(db.DateTime, nullable=False)
    Posting_Date = db.Column(db.DateTime, nullable=False)
    Expected_Receipt_Date = db.Column(db.DateTime, nullable=False)
    Posting_Description = db.Column(db.String(255), nullable=False)
    Due_Date = db.Column(db.DateTime, nullable=False)
    Location_Code = db.Column(db.String(50), nullable=False)
    Shortcut_Dimension_1 = db.Column(db.String(50), nullable=False)
    Shortcut_Dimension_2 = db.Column(db.String(50), nullable=False)
    Shortcut_Dimension_3 = db.Column(db.String(50), nullable=False)
    Comment = db.Column(db.String(255), nullable=False)
    Posting_No = db.Column(db.Integer, nullable=False)
    Last_Posting_No = db.Column(db.String(50), nullable=False)
    Reason_Code = db.Column(db.String(50), nullable=False)
    Gen_Bus_Posting_Group = db.Column(db.String(50), nullable=False)
    Document_Date = db.Column(db.DateTime, nullable=False)
    NO_Series = db.Column(db.String(50), nullable=False)
    Posting_No_Series = db.Column(db.String(50), nullable=False)
    Status = db.Column(db.Integer, nullable=False)
    Dimension_Set_ID = db.Column(db.Integer, nullable=False)
    Responsibility_Center = db.Column(db.String(50), nullable=False)
    Assigned_User_ID = db.Column(db.String(255), nullable=False)
    Posted = db.Column(db.Integer, nullable=False)
    Purchase_Type = db.Column(db.String(255), nullable=False)
    Indenting_Department = db.Column(db.String(50), nullable=False)
    Employee_Department = db.Column(db.Integer, nullable=False)
    Type_of_Jobwork = db.Column(db.Integer, nullable=False)
    Capital_Item_Premises = db.Column(db.String(50), nullable=False)
    Shortcut_Dimension_3_Code = db.Column(db.String(50), nullable=False)
    Shortcut_Dimension_6_Code = db.Column(db.String(50), nullable=False)
    Indent_Type = db.Column(db.Integer, nullable=False)
    Approved_By = db.Column(db.String(255), nullable=False)
    Approved_Date = db.Column(db.DateTime, nullable=False)
    Approved_Time = db.Column(db.DateTime, nullable=False)
    Job_Card_No = db.Column(db.String(50), nullable=False)
    Job_Card_Date = db.Column(db.DateTime, nullable=False)
    Job_Task_NO = db.Column(db.String(50), nullable=False)
    Approved_By_Account = db.Column(db.Integer, nullable=False)
    SystemId = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), nullable=False)
    SystemCreatedAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    SystemCreatedBy = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), nullable=False)
    SystemModifiedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    SystemModifiedBy = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), nullable=False)
    approver_email = db.Column(db.String(255), nullable=False)
    email_sent = db.Column(db.Boolean, default=False)  # Track if email was sent
    
    def __repr__(self):
        return f'<IMPurchaseRequisition {self.No_}: {self.Employee_Name}>'
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'Document_Type': self.Document_Type,
            'No_': self.No_,
            'Employee_No': self.Employee_No,
            'Employee_Name': self.Employee_Name,
            'Your_Reference': self.Your_Reference,
            'Request_Date': self.Request_Date.isoformat() if self.Request_Date else None,
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