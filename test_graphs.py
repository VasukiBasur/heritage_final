from app import app
import json

with app.test_client() as client:
    # First, login as admin to get the session cookie
    response = client.post('/login', data={'email': 'admin@example.com'})
    print("Login status:", response.status_code)
    
    # Now fetch artisan performance
    res_artisan = client.get('/api/stats/artisan_performance')
    print("\nArtisan Performance:", res_artisan.status_code)
    try:
        print(json.dumps(res_artisan.get_json(), indent=2))
    except Exception as e:
        print("Error parsing artisan JSON:", e)
        print(res_artisan.data.decode('utf-8')[:500])
        
    # Fetch status distribution
    res_status = client.get('/api/stats/status_distribution')
    print("\nStatus Distribution:", res_status.status_code)
    try:
        print(json.dumps(res_status.get_json(), indent=2))
    except Exception as e:
        print("Error parsing status JSON:", e)
        print(res_status.data.decode('utf-8')[:500])
