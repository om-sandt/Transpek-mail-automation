#!/usr/bin/env python3
"""
Startup Script for Approval Workflow System

This script helps you start both the Flask web application and the background email processor.
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...")
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("❌ .env file not found!")
        print("Please copy env_example.txt to .env and configure your settings.")
        return False
    
    # Check if requirements are installed
    try:
        import flask
        import sqlalchemy
        import fpdf
        print("✅ Required packages are installed")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    return True

def start_flask_app():
    """Start the Flask web application"""
    print("🌐 Starting Flask web application...")
    try:
        # Start Flask app in background
        flask_process = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for Flask to start
        time.sleep(3)
        
        if flask_process.poll() is None:
            print("✅ Flask application started successfully!")
            print("   Access at: http://localhost:5000")
            return flask_process
        else:
            stdout, stderr = flask_process.communicate()
            print(f"❌ Flask application failed to start:")
            print(f"   Error: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting Flask application: {e}")
        return None

def start_email_processor():
    """Start the background email processor"""
    print("📧 Starting email processor...")
    try:
        # Start email processor in background
        email_process = subprocess.Popen(
            [sys.executable, 'send_emails.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for processor to start
        time.sleep(2)
        
        if email_process.poll() is None:
            print("✅ Email processor started successfully!")
            return email_process
        else:
            stdout, stderr = email_process.communicate()
            print(f"❌ Email processor failed to start:")
            print(f"   Error: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting email processor: {e}")
        return None

def main():
    """Main startup function"""
    print("🚀 Approval Workflow System Startup")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    print("\n📋 Starting services...")
    
    # Start Flask app
    flask_process = start_flask_app()
    if not flask_process:
        print("❌ Failed to start Flask application")
        sys.exit(1)
    
    # Start email processor
    email_process = start_email_processor()
    if not email_process:
        print("⚠️  Email processor failed to start, but Flask app is running")
        print("   You can still use the web interface, but email notifications won't work")
    
    print("\n🎉 System startup completed!")
    print("\n📊 Services Status:")
    print(f"   Flask Web App: {'✅ Running' if flask_process and flask_process.poll() is None else '❌ Stopped'}")
    print(f"   Email Processor: {'✅ Running' if email_process and email_process.poll() is None else '❌ Stopped'}")
    
    print("\n🌐 Access your application:")
    print("   Web Interface: http://localhost:5000")
    print("   API Endpoints: http://localhost:5000/api/requests")
    
    print("\n📝 Next steps:")
    print("   1. Open http://localhost:5000 in your browser")
    print("   2. Click 'Submit New Request' to create your first approval request")
    print("   3. The email processor will automatically send notifications")
    
    print("\n⏹️  To stop the system:")
    print("   Press Ctrl+C in this terminal")
    
    try:
        # Keep the script running and monitor processes
        while True:
            time.sleep(5)
            
            # Check if processes are still running
            if flask_process and flask_process.poll() is not None:
                print("❌ Flask application has stopped unexpectedly")
                break
                
            if email_process and email_process.poll() is not None:
                print("❌ Email processor has stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
        
        # Stop Flask app
        if flask_process:
            flask_process.terminate()
            try:
                flask_process.wait(timeout=5)
                print("✅ Flask application stopped")
            except subprocess.TimeoutExpired:
                flask_process.kill()
                print("⚠️  Flask application force stopped")
        
        # Stop email processor
        if email_process:
            email_process.terminate()
            try:
                email_process.wait(timeout=5)
                print("✅ Email processor stopped")
            except subprocess.TimeoutExpired:
                email_process.kill()
                print("⚠️  Email processor force stopped")
        
        print("👋 Goodbye!")

if __name__ == "__main__":
    main() 