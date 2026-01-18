#!/usr/bin/env python3
"""
Quick test to verify Token Company API integration works
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/token-compression"

print("🧪 Testing Token Company API Integration\n")
print("=" * 60)

# Test 1: Status
print("\n1️⃣  Testing Service Status...")
response = requests.get(f"{BASE_URL}/status")
print(f"Status: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# Test 2: Basic Compression
print("\n2️⃣  Testing Basic Compression...")
data = {
    "input": "How many stars are there in the galaxy?",
    "aggressiveness": 0.5
}
response = requests.post(f"{BASE_URL}/compress", json=data)
print(f"Status: {response.status_code}")
result = response.json()
print(json.dumps(result, indent=2))

if result.get("success"):
    print(f"\n✅ Compression worked!")
    print(f"   Original: {data['input']}")
    print(f"   Compressed: {result['output']}")
    if result.get("stats"):
        print(f"   Saved {result['stats']['saved_tokens']} tokens ({result['stats']['compression_ratio']})")

# Test 3: Demo
print("\n3️⃣  Testing Demo Endpoint...")
response = requests.post(f"{BASE_URL}/compress/demo")
print(f"Status: {response.status_code}")
demo = response.json()
print(f"Demo tested {len(demo.get('results', []))} aggressiveness levels")

print("\n" + "=" * 60)
print("✅ All tests completed!")
