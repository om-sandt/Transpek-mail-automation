import pyodbc

REQUIRED_DRIVER = 'ODBC Driver 17 for SQL Server'

def check_driver():
    drivers = [driver for driver in pyodbc.drivers()]
    print('Available ODBC drivers:')
    for driver in drivers:
        print(f'  - {driver}')
    if REQUIRED_DRIVER in drivers:
        print(f'✅ Required driver "{REQUIRED_DRIVER}" is installed.')
        return True
    else:
        print(f'❌ Required driver "{REQUIRED_DRIVER}" is NOT installed.')
        print('Download it from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server')
        return False

if __name__ == "__main__":
    check_driver() 