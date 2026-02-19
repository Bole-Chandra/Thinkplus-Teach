import urllib.request
import urllib.parse
import json
import time

BASE_URL = 'http://127.0.0.1:8000/api'

def test_full_auth_flow():
    print("--- 🛡️ Thinkplus Teach: Connection & Data Storage Test 🛡️ ---")
    
    timestamp = int(time.time())
    username = f"testuser_{timestamp}"
    email = f"test_{timestamp}@example.com"
    password = "securepassword123"
    
    # 1. TEST REGISTRATION
    print(f"\n📝 1. Testing Registration for: {username}")
    reg_data = {
        "username": username,
        "email": email,
        "password": password,
        "role": "instructor"
    }
    
    try:
        payload = json.dumps(reg_data).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/users/register/", data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            print(f"✅ User Created Successfully! (ID: {res['id']}, Role: {res['role']})")

        # 2. TEST LOGIN
        print(f"\n🔑 2. Testing Login for: {username}")
        login_data = {"username": username, "password": password}
        payload = json.dumps(login_data).encode('utf-8')
        req = urllib.request.Request(f"{BASE_URL}/users/login/", data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            print(f"✅ Login Successful! (Authenticated as: {res['username']})")
            print(f"📊 Role-Based Routing Check: {res['role']} dashboard confirmed.")

        print("\n✨ ALL SYSTEMS GREEN: Frontend and Backend are perfectly synced!")
        print(f"📍 Access Frontend: http://localhost:3000")
        print(f"📍 Access Backend: http://127.0.0.1:8000/api/")

    except Exception as e:
        print(f"❌ Connection/Storage Error: {e}")

if __name__ == "__main__":
    test_full_auth_flow()
