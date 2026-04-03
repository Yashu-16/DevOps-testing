from flask import Flask, jsonify, request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def hello_world():
    """Simple hello world endpoint."""
    logger.info('Hello world endpoint accessed')
    return jsonify({
        'message': 'Hello, World!',
        'status': 'success',
        'version': '1.0.0'
    })


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'flask-app'
    })


@app.route('/api/data', methods=['POST'])
def process_data():
    """Process incoming data and return formatted response."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'name' not in data:
            return jsonify({'error': 'Missing required field: name'}), 400
        
        # Process the data
        processed_data = {
            'original': data,
            'processed': True,
            'name_length': len(data['name']),
            'timestamp': '2023-01-01T00:00:00Z'
        }
        
        logger.info(f'Processed data for: {data["name"]}')
        return jsonify(processed_data)
    
    except Exception as e:
        logger.error(f'Error processing data: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
