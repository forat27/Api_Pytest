import requests
import pytest
import csv
import json

BASE_URL = "https://jsonplaceholder.typicode.com"
RESULTS_FILE = "results.csv"

# Load data from JSON file (for POST/PUT requests)
def load_request_data():
    with open('test_data.json', 'r', encoding='utf-8') as file:
        return json.load(file)

    
# Function to log results to CSV
def log_result(request_type, endpoint, status_code, result):
    with open(RESULTS_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([request_type, endpoint, status_code, result])

@pytest.fixture
def api_base_url():
    return BASE_URL

def clean_data():
    print("Simulating cleanup after test execution.")
    yield
    print("Cleanup completed.")


def setup_module(module):
    # Initialize the CSV file with headers
    with open(RESULTS_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Request Type", "Endpoint", "Status Code", "Result"])

#---------------------------------------POST--------------------------------------------
# Test for a successful POST request
def test_successful_post_request():
    url = f"{BASE_URL}/posts"
    payload = load_request_data()  
    response = requests.post(url, json=payload)
    result = "Success" if response.status_code in [200, 201] else "Failure"
    log_result("POST", url, response.status_code, result)
    assert response.status_code in [200, 201]

# Test for status code 201
def test_status_code_post():
    url = f"{BASE_URL}/posts"
    payload = load_request_data()  
    response = requests.post(url, json=payload)
    result = "Success" if response.status_code == 201 else "Failure"
    log_result("POST", url, response.status_code, result)
    assert response.status_code == 201

# Test for response time being less than 300ms
def test_response_time_post():
    url = f"{BASE_URL}/posts"
    payload = load_request_data() 
    response = requests.post(url, json=payload)
    result = "Success" if response.elapsed.total_seconds() * 1000 < 300 else "Failure"
    log_result("POST", url, response.status_code, result)
    assert response.elapsed.total_seconds() * 1000 < 300


# Test for changes in title and body
@pytest.mark.parametrize("test_data", load_request_data())  
def test_changes_in_title_and_body_post(test_data):
    url = f"{BASE_URL}/posts"
    response = requests.post(url, json=test_data)
    response_data = response.json()
    result = "Success" if (
        response_data.get("title") == test_data["title"] and
        response_data.get("body") == test_data["body"] and
        response_data.get("userId") == test_data["userId"]
    ) else "Failure"
    log_result("POST", url, response.status_code, result)
    assert response_data["title"] == test_data["title"]
    assert response_data["body"] == test_data["body"]
    assert response_data["userId"] == test_data["userId"]



# Test for presence of Content-Type header
def test_content_type_header_post():
    url = f"{BASE_URL}/posts"
    payload = load_request_data() 
    response = requests.post(url, json=payload)
    result = "Success" if "Content-Type" in response.headers else "Failure"
    log_result("POST", url, response.status_code, result)
    assert "Content-Type" in response.headers

#---------------------------------------GET--------------------------------------------

# Test for status code 200
def test_status_code_get():
    url = f"{BASE_URL}/posts"
    response = requests.get(url)
    result = "Success" if response.status_code == 200 else "Failure"
    log_result("GET", url, response.status_code, result)
    assert response.status_code == 200

# Test for response time being less than 200ms
def test_response_time_get():
    url = f"{BASE_URL}/posts"
    response = requests.get(url)
    result = "Success" if response.elapsed.total_seconds() * 1000 < 200 else "Failure"
    log_result("GET", url, response.status_code, result)
    assert response.elapsed.total_seconds() * 1000 < 200

# Test for the presence of Content-Type header
def test_content_type_is_present_get():
    url = f"{BASE_URL}/posts"
    response = requests.get(url)
    result = "Success" if "Content-Type" in response.headers else "Failure"
    log_result("GET", url, response.status_code, result)
    assert "Content-Type" in response.headers

# Test if response body is a non-empty array
def test_response_body_is_non_empty_array_get():
    url = f"{BASE_URL}/posts"
    response = requests.get(url)
    json_data = response.json()
    result = "Success" if isinstance(json_data, list) and len(json_data) > 0 else "Failure"
    log_result("GET", url, response.status_code, result)
    assert isinstance(json_data, list)
    assert len(json_data) > 0

# Test if response is an array
def test_response_is_array_get():
    url = f"{BASE_URL}/posts"
    response = requests.get(url)
    json_data = response.json()
    result = "Success" if isinstance(json_data, list) else "Failure"
    log_result("GET", url, response.status_code, result)
    assert isinstance(json_data, list)

#---------------------------------------PUT--------------------------------------------

# Test for a successful PUT request
def test_successful_put_request():
    url = f"{BASE_URL}/posts/1"  
    payload = load_request_data() 
    response = requests.put(url, json=payload)
    result = "Success" if response.status_code in [200, 201, 204] else "Failure"
    log_result("PUT", url, response.status_code, result)
    assert response.status_code in [200, 201, 204]

# Test for status code 200
def test_status_code_put():
    url = f"{BASE_URL}/posts/1"
    payload = load_request_data()  
    response = requests.put(url, json=payload)
    result = "Success" if response.status_code == 200 else "Failure"
    log_result("PUT", url, response.status_code, result)
    assert response.status_code == 200

# Test for response time being less than 200ms
def test_response_time_put():
    url = f"{BASE_URL}/posts/1"
    payload = load_request_data() 
    response = requests.put(url, json=payload)
    result = "Success" if response.elapsed.total_seconds() * 1000 < 200 else "Failure"
    log_result("PUT", url, response.status_code, result)
    assert response.elapsed.total_seconds() * 1000 < 200

# Test for the presence of Content-Type header
def test_content_type_is_present_put():
    url = f"{BASE_URL}/posts/1"
    payload = load_request_data()  
    response = requests.put(url, json=payload)
    result = "Success" if "Content-Type" in response.headers else "Failure"
    log_result("PUT", url, response.status_code, result)
    assert "Content-Type" in response.headers


# Test for changes in title and body
@pytest.mark.parametrize("index", [0, 1, 2])
def test_changes_in_title_and_body_put(index):
    url = f"{BASE_URL}/posts/1"
    payload = load_request_data()[index]  
    response = requests.put(url, json=payload)
    response_data = response.json()
    expected_title = payload["title"]
    expected_body = payload["body"]
    expected_userId = payload["userId"]
    result = "Success" if response_data.get("title") == expected_title and response_data.get("body") == expected_body and response_data.get("userId") == expected_userId else "Failure"
    log_result("PUT", url, response.status_code, result)
    assert response_data["title"] == expected_title 
    assert response_data["body"] == expected_body 
    assert response_data["userId"] == expected_userId 



#---------------------------------------DELETE--------------------------------------------

# Test for a successful DELETE request
def test_successful_delete_request():
    url = f"{BASE_URL}/posts/1"  
    response = requests.delete(url)
    result = "Success" if response.status_code in [200, 202, 204] else "Failure"
    log_result("DELETE", url, response.status_code, result)
    assert response.status_code in [200, 202, 204]

# Test for response time being less than 300ms
def test_response_time_delete():
    url = f"{BASE_URL}/posts/1"
    response = requests.delete(url)
    result = "Success" if response.elapsed.total_seconds() * 1000 < 300 else "Failure"
    log_result("DELETE", url, response.status_code, result)
    assert response.elapsed.total_seconds() * 1000 < 300

# Test for response body being an empty JSON object
def test_response_body_is_empty_json_object_delete():
    url = f"{BASE_URL}/posts/1"
    response = requests.delete(url)
    result = "Success" if response.text == "{}" else "Failure"
    log_result("DELETE", url, response.status_code, result)
    assert response.text == "{}"

# Test for the presence of Content-Type header
def test_content_type_is_present_delete():
    url = f"{BASE_URL}/posts/1"
    response = requests.delete(url)
    result = "Success" if "Content-Type" in response.headers else "Failure"
    log_result("DELETE", url, response.status_code, result)
    assert "Content-Type" in response.headers
