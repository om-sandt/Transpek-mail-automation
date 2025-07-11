# Transpek Mail Automation System

A web-based approval workflow system for purchase requisitions with automatic email notifications.

## Features

- ✅ **Form Submission**: Submit IM Purchase Requisitions through web interface
- ✅ **Database Integration**: Direct integration with SQL Server database
- ✅ **Email Automation**: Automatic email notifications to approvers
- ✅ **Status Tracking**: Track approval status and email sending status
- ✅ **Web Interface**: Modern, responsive web interface

## Quick Start

### 1. Environment Setup

Copy the environment template and configure your settings:

```bash
cp env_example.txt .env
```

Edit `.env` file with your configuration:

```env
# Database Configuration
DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server

# Email Configuration (Optional - for email notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### 2. Test the System

Run the test script to verify everything is working:

```bash
python test_system.py
```

This will test:
- ✅ Database connection
- ✅ Form submission
- ✅ Email functionality (if configured)

### 3. Start the System

Start both the web application and email processor:

```bash
python start.py
```

This will start:
- 🌐 **Flask Web App** at http://localhost:5000
- 📧 **Email Processor** (background service)

### 4. Use the System

1. Open http://localhost:5000 in your browser
2. Click "Submit New Request" to create a purchase requisition
3. Fill in the form with required information
4. Submit the form - data will be inserted into the database
5. If approver email is provided, automatic email notifications will be sent

## System Components

### Core Files

- `app.py` - Flask web application
- `db_utils.py` - Database utilities and email functions
- `send_emails.py` - Background email processor
- `start.py` - System startup script
- `test_system.py` - System testing script

### Database

The system connects to the SQL Server table:
```
[dbo].[Transpek Industry Limited$TPT_IM Purch_ Req_ Header$114fe92f-996b-45f1-94bb-c0d5b6ba317e]
```

### Email System

- Automatically sends approval emails when new requests are submitted
- Tracks email sending status in the database
- Runs as a background service checking every 60 seconds

## Troubleshooting

### Database Connection Issues

1. Check your `DATABASE_URL` in `.env` file
2. Ensure SQL Server is running and accessible
3. Verify ODBC driver is installed
4. Run `python test_system.py` to test connection

### Email Issues

1. Check SMTP settings in `.env` file
2. For Gmail, use App Password instead of regular password
3. Ensure firewall allows SMTP connections
4. Check email processor logs in console

### Web Interface Issues

1. Check if Flask app is running on port 5000
2. Verify all required Python packages are available
3. Check console for error messages

## API Endpoints

- `GET /` - Home page
- `GET /health` - Health check endpoint
- `GET /im-purchase-requisitions` - List all requisitions
- `GET /submit-im-purchase` - Submit form page
- `POST /submit-im-purchase` - Submit new requisition
- `GET /api/im-purchase-requisitions` - API endpoint for requisitions

## Development

### Testing

```bash
# Test individual components
python test_system.py

# Test database connection
python check_odbc_driver.py

# Test form submission
python example_insert.py
```

### Logs

- Flask app logs appear in the console
- Email processor logs appear in the console
- Database errors are logged with detailed information

## Deployment

1. Set up your production environment variables
2. Install required Python packages
3. Run `python start.py` to start the system
4. Use a process manager like PM2 or systemd for production
5. Set up reverse proxy (nginx) for web traffic
6. Configure SSL certificates for HTTPS

## Support

For issues or questions:
1. Check the troubleshooting section
2. Run `python test_system.py` to identify problems
3. Check console logs for error messages
4. Verify environment configuration 
