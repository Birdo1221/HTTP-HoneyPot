from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json
from datetime import datetime
import subprocess

ABUSE_IPDB_API_KEY = 'Replace with Abuse-IPDB API Token'

class FakeWordPressHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _serve_login_page(self):
        self._set_headers()
        with open('index.html', 'r') as file:
            self.wfile.write(file.read().encode('utf-8'))

    def do_GET(self):
        if self.path in ['/wp-login.php', '/login', '/admin', '/wp-admin', '/']:
            self._serve_login_page()
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        if self.path in ['/wp-login.php', '/login', '/admin', '/wp-admin', '/']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urlparse.parse_qs(post_data.decode('utf-8'))
            ip_address = self.client_address[0]
            username = parsed_data.get('log', [''])[0]
            password = parsed_data.get('pwd', [''])[0]
            user_agent = self.headers.get('User-Agent')
            headers = dict(self.headers)

            # Get geolocation data based on IP address
            geo_info = self.get_geolocation(ip_address)

            attempt = {
                'ip': ip_address,
                'username': username,
                'password': password,
                'user_agent': user_agent,
                'headers': headers,
                'geolocation': geo_info,
                'timestamp': datetime.utcnow().isoformat()
            }

            with open('login_attempts.log', 'a') as log_file:
                log_file.write(json.dumps(attempt) + '\n')

            # Report to AbuseIPDB
            self.report_to_abuse_ipdb(ip_address)

            self._set_headers()
            self.wfile.write(b"Login attempt recorded. Thank you.")
        else:
            self.send_error(404, "Page Not Found")

    def get_geolocation(self, ip):
        url = f'http://ip-api.com/json/{ip}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f'Error fetching geolocation data: {e}')
        return {}

    def report_to_abuse_ipdb(self, ip):
        curl_command = f'curl https://api.abuseipdb.com/api/v2/report \
            --data-urlencode "ip={ip}" \
            -d categories=18 \
            --data-urlencode "comment=WordPress fake login attempt" \
            -H "Key: {ABUSE_IPDB_API_KEY}" \
            -H "Accept: application/json"'

        # Execute curl command using subprocess
        try:
            subprocess.run(curl_command, shell=True, check=True)
            print(f'Reported IP {ip} to AbuseIPDB successfully.')
        except subprocess.CalledProcessError as e:
            print(f'Failed to report IP {ip} to AbuseIPDB: {e}')

def run(server_class=HTTPServer, handler_class=FakeWordPressHandler, port=8100):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
