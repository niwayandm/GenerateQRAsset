# QR Asset Generator API

This API was used to generate QR codes in my Asset Management project. The QR has embedded logos for assets and locators.

## Features

- Authentication via Basic Auth
- Generates QR codes with logos
- Differentiates between asset and locator QR codes
- Provides JSON responses for API interactions

## Requirements

- Python 3.7
- Dependencies: `base64`, `cgi`, `os`, `json`, `qrcode`, `PIL` (Pillow)

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install dependencies:
    ```sh
    pip install qrcode[pil]
    pip install Pillow
    ```

## Usage

1. Start the server (make sure the script is executable):
    ```sh
    python qrasset.py
    ```

2. Make a POST request with the necessary parameters and Basic Auth.

### Request

- **URL:** `/`
- **Method:** `POST`
- **Headers:**
  - `Authorization: Basic <base64-encoded-credentials>`
- **Parameters:**
  - `code`: MD5 hash of the coded string
  - `type`: `locator` or `asset`

### Example

```sh
curl -X POST -H "Authorization: Basic <base64-encoded-credentials>" -d "code=<md5>&type=locator" http://<server-address>/
```

### Response

- **Content-Type:** application/json
- **Body:**

```json
{
  "status": "S",
  "message": "QR <type> image generated"
}
```

or

```json
{
  "status": "E",
  "message": "Error: <error-message>"
}
```

## Environment variables

- **HTTP_AUTHORIZATION**: Required for Basic Auth

## Example Code

Here's an example of a POST request to call the python using AJAX:

```html
<!DOCTYPE html>
<html>
<head>
    <title>QR Asset Generator</title>
    <script>
        function generateQRCode() {
            const code = document.getElementById('code').value;
            const type = document.getElementById('type').value;
            const credentials = btoa('user:pass');  // Base64 encode username and password

            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/path/to/your/qrasset.py', true);
            xhr.setRequestHeader('Authorization', 'Basic ' + credentials);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    const response = JSON.parse(xhr.responseText);
                    alert(response.message);
                }
            };
            
            xhr.send(`code=${encodeURIComponent(code)}&type=${encodeURIComponent(type)}`);
        }
    </script>
</head>
<body>
    <h1>QR Asset Generator</h1>
    <input type="text" id="code" placeholder="Enter code (md5)" />
    <select id="type">
        <option value="locator">Locator</option>
        <option value="asset">Asset</option>
    </select>
    <button onclick="generateQRCode()">Generate QR Code</button>
</body>
</html>
```

or PHP `curl`:

```html
<?php
$code = "your_md5_code";
$type = "locator"; // or "asset"
$username = "username";
$password = "pass";
$credentials = base64_encode("$username:$password");

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, "http://path/to/your/qrasset.py");
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(array('code' => $code, 'type' => $type)));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$headers = [
    "Authorization: Basic $credentials",
    "Content-Type: application/x-www-form-urlencoded"
];

curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

$response = curl_exec($ch);
curl_close($ch);

$responseData = json_decode($response, true);

if ($responseData['status'] == 'S') {
    echo "Success: " . $responseData['message'];
} else {
    echo "Error: " . $responseData['message'];
}
?>
```

**Notes**:
- For AJAX (JavaScript) Example: Make sure the path to your Python script (/path/to/your/qrasset.py) is correct and accessible from the client-side. You may need to configure your server to execute the Python script and handle POST requests.
- For PHP cURL Example: Ensure the URL (http://path/to/your/qrasset.py) points to the correct location of your Python script on the server.