"""
Script to show database schema information for Transpek tables
"""
from db_utils import setup_database, PURCHASE_REQ_TABLE, get_table_schema
import sys

def main():
    """Show schema information for the database tables"""
    print("📋 Transpek Database Schema Information")
    print("======================================")
    
    # Setup database and print schema
    setup_successful = setup_database()
    
    if not setup_successful:
        print("\n❌ Database connection failed. Please check your connection settings.")
        return 1
        
    # List all columns for a specific table - interactive mode
    while True:
        print("\nOptions:")
        print("1. Show purchase requisition table schema")
        print("2. Show schema for another table")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            print(f"\nQuerying schema for {PURCHASE_REQ_TABLE}...")
            schema_info = get_table_schema(PURCHASE_REQ_TABLE)
            if schema_info:
                print(f"\nFound {len(schema_info)} columns in purchase requisition table.")
                print(f"{'Column Name':<30} {'Data Type':<15} {'Nullable':<8}")
                print("-" * 55)
                for col in schema_info:
                    nullable = "YES" if col['is_nullable'] else "NO"
                    print(f"{col['column_name']:<30} {col['data_type']:<15} {nullable:<8}")
            else:
                print("Could not retrieve schema information.")
        
        elif choice == "2":
            table_name = input("Enter table name: ")
            print(f"\nQuerying schema for {table_name}...")
            schema_info = get_table_schema(table_name)
            if schema_info:
                print(f"\nFound {len(schema_info)} columns in table.")
                print(f"{'Column Name':<30} {'Data Type':<15} {'Nullable':<8}")
                print("-" * 55)
                for col in schema_info:
                    nullable = "YES" if col['is_nullable'] else "NO"
                    print(f"{col['column_name']:<30} {col['data_type']:<15} {nullable:<8}")
            else:
                print("Could not retrieve schema information.")
        
        elif choice == "3":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
