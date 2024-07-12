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
        save_logs_to_csv()
        time.sleep(900)  # Sleep for 15 minutes (900 seconds)

def save_logs_to_csv():
    if os.path.exists('email_opens.log'):
        print("email_opens.log exists")
        # Read the log file
        with open('email_opens.log', 'r') as f:
            lines = f.readlines()

        # Parse log lines
        data = []
        for line in lines:
            parts = line.strip().split(' - ')
            if len(parts) == 2:
                timestamp, message = parts
                if 'Email opened by:' in message:
                    try:
                        email_part = message.split('Email opened by: ')[1]
                        email = email_part.split(' - ATECO: ')[0]
                        ateco = email_part.split(' - ATECO: ')[1] if ' - ATECO: ' in email_part else 'None'
                        data.append([timestamp, email, ateco])
                    except Exception as e:
                        print(f"Error parsing line: {line.strip()}, error: {e}")
                        logging.warning(f"Error parsing line: {line.strip()}, error: {e}")
                else:
                    print(f"Skipping non-email line: {line.strip()}")
                    logging.warning(f"Skipping non-email line: {line.strip()}")
            else:
                print(f"Skipping malformed line: {line.strip()}")
                logging.warning(f"Skipping malformed line: {line.strip()}")

        # Create a DataFrame and save to CSV
        if data:  # Only save if there's data
            df = pd.DataFrame(data, columns=['Timestamp', 'Email', 'ATECO'])
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_filename = f'email_opens_{timestamp}.csv'
            df.to_csv(csv_filename, index=False)
            print(f"File saved: {csv_filename}")
            logging.info(f"CSV file saved: {csv_filename}")
        else:
            print("No valid data to save to CSV.")
            logging.info("No valid data to save to CSV.")
    else:
        print("email_opens.log does not exist")
        logging.error("email_opens.log does not exist")

if __name__ == '__main__':
    # Start the background thread to save logs periodically
    threading.Thread(target=save_logs_periodically, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
