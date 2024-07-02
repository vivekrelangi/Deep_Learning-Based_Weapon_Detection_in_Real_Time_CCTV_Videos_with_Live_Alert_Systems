from twilio.rest import Client
from password import twilioauth,twiliosid

def mes():
    account_sid = 
    auth_token = twilioauth
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='0987654321',#use twilio given number
    body='weapon detected in camera get to safe place and call for help i.e. call 100',
    to='1234567890'#use the number with which you registered in twilio
    )

    #print(message.sid)
    print("Message sent successfully")
#mes()