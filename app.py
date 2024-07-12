from flask import Flask, request, send_file, make_response
import logging
import os

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
