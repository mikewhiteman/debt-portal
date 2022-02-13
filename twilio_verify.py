import os
from twilio.rest import Client, TwilioException

twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_verify_service_sid = os.environ.get('TWILIO_VERIFY_SERVICE_SID')

def get_verify_client():
    client = Client(twilio_account_sid, twilio_auth_token)
    verify = client.verify.services(twilio_verify_service_sid)
    return verify

def request_verification_token(phone):
    verify = get_verify_client()
    try:
        verify.verifications.create(to=phone, channel='sms')
    except TwilioException:
        verify.verifications.create(to=phone, channel='call')

def check_verification_token(phone, token):
    verify = get_verify_client()
    try:
        result = verify.verification_checks.create(to=phone, code=token)
    except TwilioException:
        return False
    return result.status == 'approved'
