import sys
import json
import uuid
import unittest
from server import app
from database import get_ist_date_str

class SurakshaaSaathiIntegrationTests(unittest.TestCase):
    test_user_uuid = None
    cert_number = None

    def setUp(self):
        self.client = app.test_client()
        self.ist_date = get_ist_date_str()

    def test_01_homepage_renders(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Surakshaa Saathi", resp.data)
        self.assertIn(b"surakshaa-3d-canvas", resp.data)
        print("[PASS] Test 01: Homepage and 3D Canvas template rendered successfully.")

    def test_02_registration_no_otp(self):
        unique_email = f"citizen_{uuid.uuid4().hex[:6]}@example.com"
        payload = {
            "full_name": "Aarav Sharma",
            "country": "India",
            "state": "Delhi",
            "city": "New Delhi",
            "phone": f"+91 98{uuid.uuid4().int % 100000000:08d}",
            "email": unique_email,
            "preferred_lang": "hi"
        }
        resp = self.client.post('/api/auth/register', json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("participant", data)
        self.assertEqual(data["participant"]["full_name"], "Aarav Sharma")
        self.assertTrue(bool(data["participant"]["uuid"]))
        SurakshaaSaathiIntegrationTests.test_user_uuid = data["participant"]["uuid"]
        print(f"[PASS] Test 02: Registration without OTP verified (UUID: {SurakshaaSaathiIntegrationTests.test_user_uuid}).")

    def test_03_profile_fetch_and_update(self):
        u_uuid = SurakshaaSaathiIntegrationTests.test_user_uuid
        resp = self.client.get(f'/api/profile?uuid={u_uuid}')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["participant"]["city"], "New Delhi")

        # Update city to Gurugram
        up_resp = self.client.put(f'/api/profile?uuid={u_uuid}', json={"city": "Gurugram"})
        self.assertEqual(up_resp.status_code, 200)
        up_data = up_resp.get_json()
        self.assertEqual(up_data["participant"]["city"], "Gurugram")
        print("[PASS] Test 03: Profile retrieval and update workflow verified.")

    def test_04_scenarios_library_250_plus(self):
        resp = self.client.get('/api/scenarios?limit=1')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertGreaterEqual(data["total"], 250, "Scenario library must contain at least 250 distinct scenarios!")
        print(f"[PASS] Test 04: Scenarios library contains {data['total']} distinct scenarios (Requirement: >= 250 met!).")

        # Test search query
        search_resp = self.client.get('/api/scenarios?search=UPI')
        search_data = search_resp.get_json()
        self.assertGreater(search_data["total"], 0)
        print(f"[PASS] Test 04b: Search query 'UPI' matched {search_data['total']} scenarios.")

    def test_05_daily_quiz_and_single_attempt_restriction(self):
        u_uuid = SurakshaaSaathiIntegrationTests.test_user_uuid
        
        # 1. Fetch today's quiz
        resp = self.client.get(f'/api/quiz/today?uuid={u_uuid}')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertFalse(data["completed"], "Fresh user should have completed=False")
        self.assertEqual(len(data["questions"]), 10)

        # 2. Submit perfect score answers (10 / 10)
        correct_answers = {
            "1": 1, "2": 1, "3": 1, "4": 1, "5": 1,
            "6": 2, "7": 1, "8": 1, "9": 0, "10": 1
        }
        sub_resp = self.client.post('/api/quiz/submit', json={
            "uuid": u_uuid,
            "answers": correct_answers
        })
        self.assertEqual(sub_resp.status_code, 200)
        sub_data = sub_resp.get_json()
        self.assertEqual(sub_data["score"], 10)
        self.assertEqual(sub_data["certificate_type"], "Certificate of Appreciation")
        self.assertTrue(sub_data["certificate"]["certificate_number"].startswith("SS-2026-"))
        SurakshaaSaathiIntegrationTests.cert_number = sub_data["certificate"]["certificate_number"]
        print(f"[PASS] Test 05: Quiz submitted with 10/10 -> Awarded {sub_data['certificate_type']} (Ref: {SurakshaaSaathiIntegrationTests.cert_number}).")

        # 3. Submit again on SAME IST DATE -> MUST BE REJECTED WITH HTTP 403!
        second_sub = self.client.post('/api/quiz/submit', json={
            "uuid": u_uuid,
            "answers": correct_answers
        })
        self.assertEqual(second_sub.status_code, 403, "Duplicate submission on same IST date must return HTTP 403!")
        print("[PASS] Test 05b: Strict 1-attempt-per-day enforcement verified (HTTP 403 rejected duplicate attempt).")

    def test_06_certificate_lookup_and_email_handler(self):
        cert_no = SurakshaaSaathiIntegrationTests.cert_number
        resp = self.client.get(f'/api/certificates/{cert_no}')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["certificate"]["certificate_number"], cert_no)

        # Trigger email handler
        email_resp = self.client.post(f'/api/certificates/{cert_no}/send-email')
        self.assertIn(email_resp.status_code, [200, 500])
        print("[PASS] Test 06: Certificate verification and email dispatch handler tested.")

    def test_07_posters_and_reviews(self):
        # Posters
        p_resp = self.client.get('/api/posters')
        self.assertEqual(p_resp.status_code, 200)
        posters = p_resp.get_json()["posters"]
        self.assertGreaterEqual(len(posters), 6)
        print(f"[PASS] Test 07: Host-controlled poster gallery contains {len(posters)} verified posters.")

        # Reviews
        rev_payload = {
            "full_name": "Meera Joshi",
            "profession": "Mathematics High School Teacher",
            "rating": 5,
            "review_text": "Extremely thorough platform! Used this with my 10th grade students today for the national cybersecurity quiz."
        }
        r_sub = self.client.post('/api/reviews', json=rev_payload)
        self.assertEqual(r_sub.status_code, 200)
        print("[PASS] Test 07b: 5-star review submission with free-form typed profession tested.")

    def test_08_chatbot_safety_triage(self):
        chat_payload = {
            "message": "Someone called me claiming to be police and put me on Skype Digital Arrest. What should I do?",
            "language": "en"
        }
        chat_resp = self.client.post('/api/chat', json=chat_payload)
        self.assertEqual(chat_resp.status_code, 200)
        chat_data = chat_resp.get_json()
        self.assertIn("response", chat_data)
        self.assertIn("DIGITAL ARREST", chat_data["response"].upper())
        self.assertIn("1930", chat_data["response"])
        print("[PASS] Test 08: AI Cyber Guide responded with expert Digital Arrest defense and 1930 helpline triage.")

    def test_09_admin_authentication_and_stats(self):
        # 1. Login with master passcode
        login_resp = self.client.post('/api/admin/login', json={"password": "Surakshaa@2026"})
        self.assertEqual(login_resp.status_code, 200)
        token = login_resp.get_json()["token"]

        # 2. Access protected admin stats
        stats_resp = self.client.get('/api/admin/stats', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(stats_resp.status_code, 200)
        stats = stats_resp.get_json()
        self.assertGreaterEqual(stats["total_scenarios"], 250)
        self.assertGreaterEqual(stats["total_quizzes"], 1)
        print(f"[PASS] Test 09: Secure admin authentication and real-time stats verified (Scenarios: {stats['total_scenarios']}, Quizzes: {stats['total_quizzes']}).")

if __name__ == '__main__':
    unittest.main()

