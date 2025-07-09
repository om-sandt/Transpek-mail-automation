# Transpek Approval System

A comprehensive Flask web application for managing Job Work Reports and IM Purchase Requisitions with automated email notifications, PDF generation, and a modern web interface.

## Features

- ✅ **Job Work Reports**: Complete management of job work reports with detailed fields
- ✅ **IM Purchase Requisitions**: Comprehensive purchase requisition system
- ✅ **Web Interface**: Modern, responsive UI built with Bootstrap 5
- ✅ **Database**: PostgreSQL support with SQLAlchemy ORM
- ✅ **Email Notifications**: Automated HTML emails with PDF attachments
- ✅ **PDF Generation**: In-memory PDF creation using FPDF
- ✅ **Approval/Rejection**: One-click approval or rejection with reason tracking
- ✅ **Background Processing**: Automated email sending for pending requests
- ✅ **API Endpoints**: RESTful API for integration
- ✅ **Status Tracking**: Complete audit trail of all requests
- ✅ **Legacy Support**: Backward compatibility with old approval system

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask Web     │    │  Background     │    │   PostgreSQL    │
│   Application   │◄──►│  Email Script   │◄──►│   Database      │
│                 │    │                 │    │                 │
│ • Submit forms  │    │ • Check pending │    │ • approval_     │
│ • View requests │    │ • Send emails   │    │   requests      │
│ • Approve/Reject│    │ • Generate PDFs │    │ • Status tracking│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Database Schema

### job_work_report Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary Key |
| `timestamp` | TIMESTAMP | Creation timestamp |
| `No_` | VARCHAR(20) | Report number |
| `AOP` | SMALLINT | AOP value |
| `OBJECTIVE_OF_JOB_CARD` | VARCHAR(250) | Job card objective |
| `EXPECTED_BENEFITS` | VARCHAR(250) | Expected benefits |
| `COMPLETION_AFTER` | VARCHAR(250) | Completion details |
| `PREPARED` | VARCHAR(20) | Prepared by ID |
| `PREPARED_BY_NAME` | VARCHAR(100) | Prepared by name |
| `CHECKED_BY` | VARCHAR(20) | Checked by ID |
| `CHECKED_BY_NAME` | VARCHAR(100) | Checked by name |
| `Department_Name` | VARCHAR(250) | Department name |
| `Remarks` | VARCHAR(250) | Remarks |
| `Job_Card_Type` | VARCHAR(250) | Job card type |
| `Expected_Completion` | TIMESTAMP | Expected completion date |
| `Estimated_Amount` | NUMERIC(38,20) | Estimated amount |
| `Sanctioned_Amount` | NUMERIC(38,20) | Sanctioned amount |
| `Completed` | SMALLINT | Completion status (0/1) |
| `Approved` | SMALLINT | Approval status (0/1) |
| `Technical_Completion` | TIMESTAMP | Technical completion date |
| `Commercial_Completion` | TIMESTAMP | Commercial completion date |
| `Approval_Date_Time` | TIMESTAMP | Approval date and time |
| `Approver_ID` | VARCHAR(50) | Approver ID |
| `Original_Approval_Date` | TIMESTAMP | Original approval date |
| `TPT_Approval_Status` | INTEGER | TPT approval status |
| `TPT_Job_Type` | INTEGER | TPT job type |
| `approver_email` | VARCHAR(255) | Approver email |

### im_purchase_requisition Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary Key |
| `Document_Type` | TIMESTAMP | Document type timestamp |
| `No` | INTEGER | Requisition number |
| `Employee_No` | VARCHAR(20) | Employee number |
| `Employee_Name` | VARCHAR(20) | Employee name |
| `Your_Reference` | VARCHAR(50) | Reference |
| `Request_Date` | VARCHAR(30) | Request date |
| `Posting_Date` | TIMESTAMP | Posting date |
| `Expected_Receipt_Date` | TIMESTAMP | Expected receipt date |
| `Posting_Description` | VARCHAR(50) | Posting description |
| `Due_Date` | TIMESTAMP | Due date |
| `Location_Code` | VARCHAR(10) | Location code |
| `Shortcut_Dimension_1` | VARCHAR(20) | Shortcut dimension 1 |
| `Shortcut_Dimension_2` | VARCHAR(20) | Shortcut dimension 2 |
| `Shortcut_Dimension_3` | VARCHAR(20) | Shortcut dimension 3 |
| `Comment` | VARCHAR(100) | Comment |
| `Posting_No` | SMALLINT | Posting number |
| `Last_Posting_No` | VARCHAR(20) | Last posting number |
| `Reason_Code` | VARCHAR(20) | Reason code |
| `Gen_Bus_Posting_Group` | VARCHAR(10) | Gen bus posting group |
| `Document_Date` | TIMESTAMP | Document date |
| `NO_Series` | VARCHAR(10) | NO series |
| `Posting_No_Series` | VARCHAR(10) | Posting NO series |
| `Status` | INTEGER | Status |
| `Dimension_Set_ID` | INTEGER | Dimension set ID |
| `Responsibility_Center` | VARCHAR(10) | Responsibility center |
| `Assigned_User_ID` | VARCHAR(50) | Assigned user ID |
| `Posted` | INTEGER | Posted status |
| `Purchase_Type` | VARCHAR(100) | Purchase type |
| `Indenting_Department` | VARCHAR(10) | Indenting department |
| `Employee_Department` | SMALLINT | Employee department |
| `Type_of_Jobwork` | INTEGER | Type of jobwork |
| `Capital_Item_Premises` | VARCHAR(10) | Capital item premises |
| `Shortcut_Dimension_3_Code` | VARCHAR(20) | Shortcut dimension 3 code |
| `Shortcut_Dimension_6_Code` | VARCHAR(20) | Shortcut dimension 6 code |
| `Indent_Type` | INTEGER | Indent type |
| `Approved_By` | VARCHAR(250) | Approved by |
| `Approved_Date` | TIMESTAMP | Approved date |
| `Approved_Time` | TIMESTAMP | Approved time |
| `Job_Card_No` | VARCHAR(20) | Job card number |
| `Job_Card_Date` | TIMESTAMP | Job card date |
| `Job_Task_NO` | VARCHAR(20) | Job task number |
| `Approved_By_Account` | SMALLINT | Approved by account |
| `SystemId` | VARCHAR(36) | System ID |
| `SystemCreatedAt` | TIMESTAMP | System created at |
| `SystemCreatedBy` | VARCHAR(36) | System created by |
| `SystemModifiedAt` | TIMESTAMP | System modified at |
| `SystemModifiedBy` | VARCHAR(36) | System modified by |
| `approver_email` | VARCHAR(255) | Approver email |

### approval_requests Table (Legacy)

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary Key |
| `data` | TEXT | Request content (required) |
| `status` | VARCHAR(50) | Status: 'Pending', 'Approved', 'Rejected' |
| `approver_email` | VARCHAR(255) | Email of approver (required) |
| `reason` | TEXT | Approval/rejection reason (nullable) |
| `created_at` | TIMESTAMP | Creation timestamp (auto) |

## Installation & Setup

### 1. Prerequisites

- Python 3.8+
- PostgreSQL database
- SMTP email server (Gmail, Outlook, etc.)

### 2. Clone and Install Dependencies

```bash
git clone <repository-url>
cd approval-workflow
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy `env_example.txt` to `.env` and configure:

```bash
cp env_example.txt .env
```

Edit `.env` with your settings:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/approval_workflow

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_APP_URL=http://localhost:5000
```

### 4. Database Setup

Create PostgreSQL database:

```sql
CREATE DATABASE approval_workflow;
```

The application will automatically create tables on first run.

### 5. Run the Application

#### Start Flask Web Server
```bash
python app.py
```
Access at: http://localhost:5000

#### Start Background Email Processor
```bash
python send_emails.py
```

## Usage Guide

### 1. Submit a Job Work Report

1. Navigate to http://localhost:5000
2. Click "Submit New Report" under Job Work Reports
3. Fill in all required fields:
   - **Basic Information**: Report number, AOP, objective, benefits, completion details
   - **Personnel Information**: Prepared by, checked by, department
   - **Job Details**: Remarks, job card type, expected completion, amounts
   - **Status and Approval**: Completion status, approval status, dates
   - **Additional Information**: Approver ID, TPT status, job type
   - **Contact Information**: Approver email
4. Click "Submit Report"

### 2. Submit an IM Purchase Requisition

1. Navigate to http://localhost:5000
2. Click "Submit New Requisition" under IM Purchase Requisitions
3. Fill in all required fields:
   - **Basic Information**: Requisition number, employee details, reference
   - **Dates and Timing**: Posting date, expected receipt, due date, document date
   - **Description and Details**: Posting description, comment, location, purchase type
   - **Dimensions and Codes**: All shortcut dimensions
   - **Posting Information**: Posting numbers, reason codes, series
   - **Status and Department**: Status, posted status, dimensions, departments
   - **Job Work and Approval**: Job work type, approval details
   - **Job Card Information**: Job card details, task numbers
   - **Contact Information**: Approver email
4. Click "Submit Requisition"

### 2. Email Notification Process

The background script (`send_emails.py`) automatically:
- Checks for pending requests every 5 minutes
- Generates PDF documents from request data
- Sends HTML emails with:
  - Request details
  - PDF attachment
  - ✅ Approve button
  - ❌ Reject button

### 3. Approval/Rejection Process

When approver receives email:
1. **Click Approve/Reject button** → Opens simple modal popup
2. **Review request details** → Request data displayed in modal
3. **Add comments** → Optional for approval, required for rejection
4. **Submit decision** → Modal closes automatically, returns to email

### 4. View All Requests

- **Dashboard**: Overview of all requests with statistics
- **Status tracking**: Pending, Approved, Rejected counts
- **Email status**: Shows when emails have been sent
- **Read-only interface**: No direct approval actions from web interface

## API Endpoints

### Job Work Reports
- **GET /api/job-work-reports** - Returns all job work reports as JSON
- **GET /job-work-reports** - View all job work reports
- **GET /submit-job-work** - Submit new job work report form
- **POST /submit-job-work** - Submit new job work report

### IM Purchase Requisitions
- **GET /api/im-purchase-requisitions** - Returns all IM purchase requisitions as JSON
- **GET /im-purchase-requisitions** - View all IM purchase requisitions
- **GET /submit-im-purchase** - Submit new IM purchase requisition form
- **POST /submit-im-purchase** - Submit new IM purchase requisition

### Legacy System (Backward Compatibility)
- **GET /api/requests** - Returns all legacy approval requests as JSON
- **GET /api/requests/{id}** - Returns specific legacy request details
- **GET /legacy** - View legacy approval requests
- **POST /submit** - Submit new legacy approval request
- **GET /quick-approve?id={id}** - Show quick approval modal for specific request
- **GET /quick-reject?id={id}** - Show quick rejection modal for specific request
- **POST /process** - Process approval/rejection decision

## File Structure

```
transpek-approval-system/
├── app.py                 # Main Flask application
├── models.py              # SQLAlchemy database models
├── send_emails.py         # Background email processor
├── pdf_generator.py       # PDF generation utilities
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.md             # This file
└── templates/            # HTML templates
    ├── base.html         # Base template
    ├── index.html        # Main navigation page
    ├── job_work_reports.html      # Job work reports list
    ├── submit_job_work.html       # Job work report form
    ├── im_purchase_requisitions.html  # IM purchase requisitions list
    ├── submit_im_purchase.html    # IM purchase requisition form
    ├── legacy_index.html          # Legacy approval requests
    ├── submit.html       # Legacy submit form
    ├── approve.html      # Legacy approval form
    └── reject.html       # Legacy rejection form
```

## Configuration Options

### Email Settings

- **SMTP_SERVER**: Your email provider's SMTP server
- **SMTP_PORT**: Usually 587 for TLS or 465 for SSL
- **SMTP_USERNAME**: Your email address
- **SMTP_PASSWORD**: App password (not regular password for Gmail)

### Database Settings

- **DATABASE_URL**: PostgreSQL connection string
- Format: `postgresql://username:password@host:port/database`

### Application Settings

- **SECRET_KEY**: Flask secret key for sessions
- **FLASK_APP_URL**: Base URL for email links
- **FLASK_ENV**: Development/production mode

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check DATABASE_URL format
   - Ensure database exists

2. **Email Not Sending**
   - Verify SMTP credentials
   - Check firewall/network settings
   - Use app passwords for Gmail

3. **PDF Generation Issues**
   - Ensure FPDF is installed
   - Check data encoding

### Logs

- Flask app logs to console
- Email processor logs with emojis for easy reading
- Database errors shown in web interface

## Security Considerations

- Use environment variables for sensitive data
- Implement proper authentication in production
- Use HTTPS in production
- Regular database backups
- Monitor email sending limits

## Production Deployment

1. **Use WSGI server** (Gunicorn, uWSGI)
2. **Set up reverse proxy** (Nginx)
3. **Use production database**
4. **Configure proper logging**
5. **Set up monitoring**
6. **Use process manager** (systemd, supervisor)

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Check troubleshooting section
- Review logs for error messages
- Ensure all dependencies are installed
- Verify environment configuration "# Transpek-mail-automation" 
