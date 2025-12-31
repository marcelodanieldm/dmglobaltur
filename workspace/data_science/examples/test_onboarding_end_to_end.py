import requests

def test_onboarding_end_to_end():
    url = 'http://localhost:8000/api/onboarding/analyze'
    files = {
        'inventory': open('data_science/examples/example_inventory.csv', 'rb')
    }
    data = {
        'city': 'Shanghai',
        'archetypes': '["Old Money","New Rich"]',
        'channels': '{"whatsapp":true,"email":true}',
        'user_id': 'test_user_001'
    }
    response = requests.post(url, data=data, files=files)
    print('Status:', response.status_code)
    print('Response:', response.json())

if __name__ == '__main__':
    test_onboarding_end_to_end()
