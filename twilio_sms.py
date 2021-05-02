import os
import twilio

twilio_account_sid = os.environ.get('twilio_account_sid')
twilio_auth_token = os.environ.get('twilio_auth_token')
twilio_verify_service_sid = os.environ.get('twilio_verify_service_sid')

from twilio.rest import Client
client = Client(twilio_account_sid, twilio_auth_token)
verify = client.verify.services(twilio_verify_service_sid)
#verify.verifications.create(to='+5555555555', channel='sms')

#result = verify.verification_checks.create(to='+5555555555', code='12345')

print(result.status)