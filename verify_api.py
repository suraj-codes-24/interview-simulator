import requests

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("1. Registering/Logging in...")
    creds = {"email": "test@example.com", "password": "password"}
    # try register
    r = requests.post(f"{BASE_URL}/auth/register", json={**creds, "name": "Test User", "branch": "CSE", "year": 2})
    # login
    login_req = requests.post(f"{BASE_URL}/auth/login", json=creds)
    token = login_req.json().get("access_token")
    if not token:
        print("Failed to get token:", login_req.json())
        return
        
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n2. Getting subjects...")
    r = requests.get(f"{BASE_URL}/interview/subjects", headers=headers)
    subjects = r.json()
    print(f"Found {len(subjects)} subjects. First one:", subjects[0] if subjects else "None")
    
    if not subjects:
        return
        
    subject_id = subjects[0]["id"]
    
    print(f"\n3. Getting topics for subject {subject_id}...")
    r = requests.get(f"{BASE_URL}/interview/topics?subject_id={subject_id}", headers=headers)
    topics = r.json()
    print(f"Found {len(topics)} topics. First one:", topics[0] if topics else "None")
    
    if not topics: return
    topic_id = topics[0]["id"]
    
    print(f"\n4. Getting subtopics for topic {topic_id}...")
    r = requests.get(f"{BASE_URL}/interview/subtopics?topic_id={topic_id}", headers=headers)
    subtopics = r.json()
    print(f"Found {len(subtopics)} subtopics. First one:", subtopics[0] if subtopics else "None")

    print("\n5. Testing /interview/start...")
    payload = {
        "interview_type": "technical",
        "subject_id": subject_id,
        "topic_id": topic_id,
        "difficulty": "medium"
    }
    r = requests.post(f"{BASE_URL}/interview/start", json=payload, headers=headers)
    print("Start Response:", r.json())
    
test_api()
