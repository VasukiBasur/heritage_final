import os
import sys
import re
import unittest
from datetime import datetime, timedelta

# Add root directory to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import jwt

class TestStripeKeySecurity(unittest.TestCase):
    def test_no_hardcoded_keys_in_tracked_files(self):
        """Ensure no live or real test Stripe keys exist in tracked files."""
        pattern = re.compile(r'\b(sk|pk|rk)_(live|test)_[a-zA-Z0-9]{16,}\b')
        flagged = []
        for root, dirs, files in os.walk(root_dir):
            if any(p in root for p in ['.git', '.venv', '__pycache__', 'scratch']):
                continue
            for f in files:
                # .env is local secret store and gitignored; check all other files
                if f == '.env':
                    continue
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                        for idx, line in enumerate(fp, 1):
                            m = pattern.search(line)
                            if m:
                                matched_val = m.group(0)
                                # Allow dummy placeholder in .env.example
                                if f == '.env.example' and 'sk_test_your_stripe_secret_key_here' in matched_val:
                                    continue
                                flagged.append(f"{os.path.relpath(path, root_dir)}:{idx}")
                except Exception:
                    pass
        self.assertEqual(len(flagged), 0, f"Found hardcoded Stripe secrets in: {flagged}")

    def test_supplier_settings_template_has_no_hardcoded_key(self):
        """Verify supplier_settings.html uses jinja placeholder."""
        tmpl_path = os.path.join(root_dir, 'templates', 'supplier_settings.html')
        with open(tmpl_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertNotIn('sk_live_', content)
        self.assertIn("{{ stripe_api_key or '' }}", content)

    def test_app_supplier_settings_route(self):
        """Verify app route renders supplier_settings with stripe_api_key."""
        from app import app, JWT_SECRET
        app.config['TESTING'] = True
        client = app.test_client()

        # Generate JWT token for Supplier
        payload = {
            'user_id': 999,
            'role': 'Supplier',
            'username': 'TestSupplier',
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        client.set_cookie('jwt_token', token)

        # Set a test stripe key in app config
        app.config['STRIPE_SECRET_KEY'] = 'test_config_stripe_key_abc123'

        res = client.get('/supplier/settings')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn('Command Center API Key', html)
        self.assertIn('id="command-center-key"', html)
        self.assertIn('value="test_config_stripe_key_abc123"', html)

    def test_app_supplier_settings_empty_when_unset(self):
        """Verify app route handles empty/unset key cleanly."""
        from app import app, JWT_SECRET
        app.config['TESTING'] = True
        client = app.test_client()

        payload = {
            'user_id': 999,
            'role': 'Supplier',
            'username': 'TestSupplier',
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        client.set_cookie('jwt_token', token)

        # Temporarily unset in config and env
        orig_config = app.config.get('STRIPE_SECRET_KEY')
        orig_env = os.environ.get('STRIPE_SECRET_KEY')
        try:
            app.config['STRIPE_SECRET_KEY'] = ''
            if 'STRIPE_SECRET_KEY' in os.environ:
                del os.environ['STRIPE_SECRET_KEY']

            res = client.get('/supplier/settings')
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            self.assertIn('id="command-center-key" value=""', html)
        finally:
            if orig_config is not None:
                app.config['STRIPE_SECRET_KEY'] = orig_config
            if orig_env is not None:
                os.environ['STRIPE_SECRET_KEY'] = orig_env

if __name__ == '__main__':
    unittest.main()
