import requests
import sys

BASE_URL = "http://127.0.0.1:8001"

def test_flow():
    print("Testing session start...")
    try:
        resp = requests.post(f"{BASE_URL}/session/start", json={"pid": "test_user_1", "study_id": "study_001", "experiment_id": 1})
        resp.raise_for_status()
        data = resp.json()
        print("Session start response:", data)
        chat_session_id = data["chat_session_id"]
        condition_id = data["condition_id"]
    except Exception as e:
        print(f"Session start failed: {e}")
        if 'resp' in locals():
            print(resp.text)
        sys.exit(1)

    print(f"\nTesting chat with session {chat_session_id}...")
    try:
        chat_payload = {
            "chat_session_id": chat_session_id,
            "user_message": "Hello, how are you?"
        }
        resp = requests.post(f"{BASE_URL}/chat", json=chat_payload)
        resp.raise_for_status()
        chat_data = resp.json()
        print("Chat response:", chat_data)
        
        if not chat_data.get("assistant_message"):
            print("Error: No assistant message received")
            sys.exit(1)
            
    except Exception as e:
        print(f"Chat failed: {e}")
        if 'resp' in locals():
            print(resp.text)
        sys.exit(1)

    print("\nVerification Successful!")

if __name__ == "__main__":
    test_flow()
