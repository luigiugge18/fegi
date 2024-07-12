from flask import Flask, request, send_file, make_response
import logging
import os
import threading
import time
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='email_opens.log', level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/')
def home():
    return '<h1>Welcome to the Flask App!</h1>'

@app.route('/track/<email>')
def track(email):
    ateco = request.args.get('ateco')
    logging.info(f'Email opened by: {email} - ATECO: {ateco}')
    if not os.path.exists('pixel.png'):
        logging.error('pixel.png not found')
        return "Tracking pixel not found", 404

    response = make_response(send_file('pixel.png', mimetype='image/png'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

def save_logs_periodically():
    while True:
        time.sleep(900)  # Sleep for 15 minutes (900 seconds)
        save_logs_to_csv()

def save_logs_to_csv():
    if os.path.exists('email_opens.log'):
        # Read the log file
        with open('email_opens.log', 'r') as f:
            lines = f.readlines()
        
        # Parse log lines
        data = []
        for line in lines:
            parts = line.strip().split(' - ')
            if len(parts) == 2:
                timestamp, message = parts
                email = message.split(': ')[1].split(' - ATECO: ')[0]
                ateco = message.split(' - ATECO: ')[1]
                data.append([timestamp, email, ateco])
        
        # Create a DataFrame and save to CSV
        df = pd.DataFrame(data, columns=['Timestamp', 'Email', 'ATECO'])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        df.to_csv(f'email_opens_{timestamp}.csv', index=False)

if __name__ == '__main__':
    # Start the background thread to save logs periodically
    threading.Thread(target=save_logs_periodically, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
