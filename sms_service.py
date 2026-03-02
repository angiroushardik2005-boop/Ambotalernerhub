"""
OTP Service using Fast2SMS API
"""
import requests
import random
from flask import session

API_KEY = "89cX2udjrVOMxJpveIyBhTolsKgHqF4ZaGm3NDwL1AknC7zb5YS3oZbFKsD62reOYIg8McquNlHJvP9Q"

def send_otp(phone_number):
    """Send OTP to phone number using Fast2SMS"""
    try:
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        
        url = "https://www.fast2sms.com/dev/bulkV2"
        
        payload = {
            "sender_id": "FSTSMS",
            "message": f"Your Ambota Learners Hub OTP is {otp}. Valid for 10 minutes.",
            "language": "english",
            "route": "q",
            "numbers": phone_number
        }
        
        headers = {
            "authorization": API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            # Store OTP in session for verification
            session['registration_otp'] = otp
            session['registration_phone'] = phone_number
            return True, otp, "OTP sent successfully"
        else:
            return False, None, f"Failed to send OTP: {response.text}"
            
    except Exception as e:
        return False, None, str(e)

def verify_otp(entered_otp):
    """Verify the OTP entered by user"""
    stored_otp = session.get('registration_otp')
    
    if not stored_otp:
        return False, "No OTP found. Please request a new OTP."
    
    if stored_otp == entered_otp:
        # Clear OTP from session after successful verification
        session.pop('registration_otp', None)
        return True, "OTP verified successfully"
    else:
        return False, "Invalid OTP. Please try again."

def clear_otp_session():
    """Clear OTP data from session"""
    session.pop('registration_otp', None)
    session.pop('registration_phone', None)
    session.pop('registration_data', None)
