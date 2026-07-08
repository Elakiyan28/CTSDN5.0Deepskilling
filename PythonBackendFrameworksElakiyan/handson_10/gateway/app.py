import requests
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

SERVICES = {
    'courses': 'http://127.0.0.1:5001',
    'students': 'http://127.0.0.1:5002',
}


def proxy(service_url, path):
    url = f'{service_url}{path}'
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={k: v for k, v in request.headers if k != 'Host'},
            json=request.get_json(silent=True),
            params=request.args,
            timeout=5,
        )
        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type'))
    except requests.ConnectionError:
        return jsonify({'error': f'Service at {service_url} is unavailable'}), 503


@app.route('/api/courses/', defaults={'subpath': ''}, methods=['GET', 'POST'])
@app.route('/api/courses/<path:subpath>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def route_courses(subpath):
    return proxy(SERVICES['courses'], f'/api/courses/{subpath}')


@app.route('/api/students/', defaults={'subpath': ''}, methods=['GET', 'POST'])
@app.route('/api/students/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_students(subpath):
    return proxy(SERVICES['students'], f'/api/students/{subpath}')


@app.route('/health')
def health():
    return jsonify({'gateway': 'ok', 'routes': list(SERVICES.keys())})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
