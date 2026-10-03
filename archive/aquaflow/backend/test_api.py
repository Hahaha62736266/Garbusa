import requests

BASE = "http://127.0.0.1:5000/api"

def test_endpoint(name, method, url, data=None):
    print(f"\n🔍 Testing {name}...")
    try:
        if method == "GET":
            res = requests.get(url, timeout=5)
        elif method == "POST":
            res = requests.post(url, json=data, timeout=5)
        
        if res.status_code in (200, 201):
            print(f"✅ PASS — Status: {res.status_code}")
            print(f"   Data: {res.json()}")
        else:
            print(f"❌ FAIL — Status: {res.status_code}")
    except Exception as e:
        print(f"❌ ERROR — {e}")

# Run all tests
print("=" * 50)
print("💧 AQUAFLOW API ENDPOINT TEST")
print("=" * 50)

test_endpoint("Dashboard Stats", "GET", f"{BASE}/dashboard/stats")
test_endpoint("Get Orders", "GET", f"{BASE}/orders")
test_endpoint("Create Order", "POST", f"{BASE}/orders",
              {"customer": "Test Customer", "liters": 15})
test_endpoint("Get Inventory", "GET", f"{BASE}/inventory")
test_endpoint("Get Users", "GET", f"{BASE}/users")

print("\n" + "=" * 50)
print("🏁 All tests completed")
print("=" * 50)