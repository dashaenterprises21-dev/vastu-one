import os
from dotenv import load_dotenv
load_dotenv()
import razorpay

key_id = os.getenv('RAZORPAY_KEY_ID', '')
key_secret = os.getenv('RAZORPAY_KEY_SECRET', '')

print(f'Testing key: {key_id[:25]}...')

client = razorpay.Client(auth=(key_id, key_secret))

try:
    order = client.order.create({
        'amount': 100,
        'currency': 'INR',
        'receipt': 'test_005',
    })
    print('SUCCESS! Order created: ' + order['id'])
except Exception as e:
    print('FAILED: ' + str(e))