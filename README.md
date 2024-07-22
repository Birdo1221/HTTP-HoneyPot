# HTTP WordPress Reporting Server

This project provides an HTTP server script that simulates a fake WordPress login page. The server logs login attempts, fetches geolocation data for each IP address, and reports malicious IPs to AbuseIPDB.

## Features

- Simulates a WordPress login page at various endpoints.
- Logs login attempts including IP address, username, password, user agent, and headers.
- Fetches and includes geolocation data for each IP address.
- Reports suspicious IP addresses to AbuseIPDB.

## Getting Started

### Prerequisites

- Python 3.x
- Requests library
- Curl

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/http-reporting-server.git
    cd http-reporting-server
    ```

2. Install the required Python packages:
    ```sh
    pip install requests
    ```

3. Replace the placeholder in the script with your AbuseIPDB API key:
    ```python
    ABUSE_IPDB_API_KEY = 'Replace with your AbuseIPDB API key'
    ```

4. Create an `index.html` file with your desired login page content. This file should be in the same directory as the script.
   I have Provided a `index.html` which is a design to look like a fake wordpress page.
   
   The fake page is not a 1-to-1 design to an actual wordpress page.

### Example Image
![image](https://github.com/user-attachments/assets/2912a393-1440-471b-9692-7760d8f7d099)

### Usage

Run the server using the following command:
```sh
python server.py
