from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from datetime import datetime

db = SQLAlchemy()

class IMPurchaseRequisition(db.Model):
    __tablename__ = '[Transpek Industry Limited$TPT_IM Purch_ Req_ Header$114fe92f-996b-45f1-94bb-c0d5b6ba317e]'

    # Primary key and system fields
    systemId = db.Column('$systemId', UNIQUEIDENTIFIER, primary_key=True)
    systemCreatedAt = db.Column('$systemCreatedAt', db.DateTime, nullable=False)
    systemCreatedBy = db.Column('$systemCreatedBy', UNIQUEIDENTIFIER, nullable=False)
    systemModifiedAt = db.Column('$systemModifiedAt', db.DateTime, nullable=False)
    systemModifiedBy = db.Column('$systemModifiedBy', UNIQUEIDENTIFIER, nullable=False)

    # Business fields with exact data types
    timestamp = db.Column('timestamp', db.String, nullable=False)
    Document_Type = db.Column('Document Type', db.Integer, nullable=False)
    No_ = db.Column('No_', db.String(20), nullable=False)
    Employee_No = db.Column('Employee No_', db.String(20), nullable=False)
    Employee_Name = db.Column('Employee Name', db.String(50), nullable=False)
    Your_Reference = db.Column('Your Reference', db.String(30), nullable=False)
    Request_Date = db.Column('Request Date', db.DateTime, nullable=False)
    Posting_Date = db.Column('Posting Date', db.DateTime, nullable=False)
    Expected_Receipt_Date = db.Column('Expected Receipt Date', db.DateTime, nullable=False)
    Posting_Description = db.Column('Posting Description', db.String(50), nullable=False)
    Due_Date = db.Column('Due Date', db.DateTime, nullable=False)
    Location_Code = db.Column('Location Code', db.String(10), nullable=False)
    Shortcut_Dimension_1_Code = db.Column('Shortcut Dimension 1 Code', db.String(20), nullable=False)
    Shortcut_Dimension_2_Code = db.Column('Shortcut Dimension 2 Code', db.String(20), nullable=False)
    Shortcut_Dimension_2_Value = db.Column('Shortcut Dimension 2 Value', db.String(100), nullable=False)
    Comment = db.Column('Comment', db.SmallInteger, nullable=False)  # tinyint maps to SmallInteger
    Posting_No = db.Column('Posting No_', db.String(20), nullable=False)
    Last_Posting_No = db.Column('Last Posting No_', db.String(20), nullable=False)
    Reason_Code = db.Column('Reason Code', db.String(10), nullable=False)
    Gen_Bus_Posting_Group = db.Column('Gen_ Bus_ Posting Group', db.String(10), nullable=False)
    Document_Date = db.Column('Document Date', db.DateTime, nullable=False)
    NO_Series = db.Column('No_ Series', db.String(10), nullable=False)
    Posting_No_Series = db.Column('Posting No_ Series', db.String(10), nullable=False)
    Status = db.Column('Status', db.Integer, nullable=False)
    Dimension_Set_ID = db.Column('Dimension Set ID', db.Integer, nullable=False)
    Responsibility_Center = db.Column('Responsibility Center', db.String(10), nullable=False)
    Assigned_User_ID = db.Column('Assigned User ID', db.String(50), nullable=False)
    Posted = db.Column('Posted', db.SmallInteger, nullable=False)
    Purchase_Type = db.Column('Purchase Type', db.Integer, nullable=False)
    Indenting_Department = db.Column('Indenting Department', db.String(100), nullable=False)
    Employee_Department = db.Column('Employee Department', db.String(10), nullable=False)
    Type_of_Jobwork = db.Column('Type of Jobwork', db.Integer, nullable=False)
    Capital_Item_Premises = db.Column('Capital Item Premises', db.Integer, nullable=False)
    Shortcut_Dimension_3_Code = db.Column('Shortcut Dimension 3 Code', db.String(20), nullable=False)
    Shortcut_Dimension_6_Code = db.Column('Shortcut Dimension 6 Code', db.String(20), nullable=False)
    Indent_Type = db.Column('Indent Type', db.Integer, nullable=False)
    Approved_By = db.Column('Approved By', db.String(250), nullable=False)
    Approved_Date = db.Column('Approved Date', db.DateTime, nullable=False)
    Approved_Time = db.Column('Approved Time', db.DateTime, nullable=False)
    Job_Card_No = db.Column('Job Card No_', db.String(20), nullable=False)
    Job_Card_Date = db.Column('Job Card Date', db.DateTime, nullable=False)
    Job_Task_NO = db.Column('Job Task No_', db.String(20), nullable=False)
    Approved_By_Account = db.Column('Approved By Account Dept_', db.SmallInteger, nullable=False)

    # Nullable text fields
    approver_email = db.Column('approver_mailid', db.Text, nullable=True)
    status_text = db.Column('status', db.Text, nullable=True)
    email_send = db.Column('email_send', db.Text, nullable=True)

    def __repr__(self):
        return f'<IMPurchaseRequisition {self.No_}>'

    def to_dict(self):
        """Convert model to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}