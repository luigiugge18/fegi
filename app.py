from flask import Flask, request, send_file
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='email_opens.log', level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/track/<email>')
def track(email):
    # Log the open event
    logging.info(f'Email opened by: {email}')
    
    # Return a 1x1 transparent pixel
    return send_file('pixel.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
