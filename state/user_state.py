import reflex as rx
import pandas as pd
import os
from dotenv import load_dotenv
from config import DATA_PATH

load_dotenv()

_firebase_db = None

def get_firebase_db():
    global _firebase_db
    if _firebase_db is not None:
        return _firebase_db
    try:
        from pyrebase import initialize_app
        firebase_config = {
            "apiKey": os.getenv("FIREBASE_API_KEY", "placeholder"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", "placeholder"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID", "placeholder"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "placeholder"),
            "messagingSenderId": os.getenv("FIREBASE_SENDER_ID", "placeholder"),
            "appId": os.getenv("FIREBASE_APP_ID", "placeholder"),
            "databaseURL": os.getenv("FIREBASE_DATABASE_URL", "")
        }
        firebase = initialize_app(firebase_config)
        _firebase_db = firebase.database()
        return _firebase_db
    except Exception as e:
        print(f"DB Init Error: {e}")
        return None
class UserState(rx.State):
    """
    State managing the user's session.
    Stores user_id, logged_in status, and user_type.
    """
    user_id: int = -1
    logged_in: bool = False
    is_new_user: bool = True
    firebase_uid: str = ""
    
    email: str = ""
    password: str = ""
    auth_error: str = ""
    
    def set_email(self, value: str):
        """Explicit setter for email field."""
        self.email = value
    
    def set_password(self, value: str):
        """Explicit setter for password field."""
        self.password = value
    
    def _get_firebase_auth(self):
        """Helper to get firebase auth instance with proper error handling."""
        try:
            from pyrebase import initialize_app
            firebase_config = {
                "apiKey": os.getenv("FIREBASE_API_KEY", "placeholder"),
                "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", "placeholder"),
                "projectId": os.getenv("FIREBASE_PROJECT_ID", "placeholder"),
                "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "placeholder"),
                "messagingSenderId": os.getenv("FIREBASE_SENDER_ID", "placeholder"),
                "appId": os.getenv("FIREBASE_APP_ID", "placeholder"),
                "databaseURL": os.getenv("FIREBASE_DATABASE_URL", "")
            }
            # Pyrebase handles multiple calls to initialize_app gracefully, but it's cleaner to be robust.
            firebase = initialize_app(firebase_config)
            return firebase.auth()
        except Exception as e:
            print(f"Firebase Init Error: {e}")
            return None

    def signup_with_firebase(self):
        """Register a new user with Firebase using email/password."""
        if not self.email or not self.password:
            self.auth_error = "Please enter both email and password."
            return
            
        auth = self._get_firebase_auth()
        if not auth:
            self.auth_error = "Authentication service is currently unavailable."
            return

        try:
            user = auth.create_user_with_email_and_password(self.email, self.password)
            events = self._handle_successful_login(user['localId'])
            for evt in events:
                yield evt
            yield rx.redirect("/")
        except Exception as e:
            # Parse common Firebase errors
            err_msg = str(e)
            if "EMAIL_EXISTS" in err_msg:
                self.auth_error = "This email is already registered."
            elif "WEAK_PASSWORD" in err_msg:
                self.auth_error = "Password should be at least 6 characters."
            elif "INVALID_EMAIL" in err_msg:
                self.auth_error = "Please enter a valid email address."
            else:
                self.auth_error = "Registration failed. Please try again later."
            
    def login_with_firebase(self):
        """Login an existing user with Firebase."""
        if not self.email or not self.password:
            self.auth_error = "Please enter both email and password."
            return
            
        auth = self._get_firebase_auth()
        if not auth:
            self.auth_error = "Authentication service is currently unavailable."
            return

        try:
            user = auth.sign_in_with_email_and_password(self.email, self.password)
            events = self._handle_successful_login(user['localId'])
            for evt in events:
                yield evt
            yield rx.redirect("/")
        except Exception as e:
            err_msg = str(e)
            if "INVALID_PASSWORD" in err_msg or "EMAIL_NOT_FOUND" in err_msg or "INVALID_LOGIN_CREDENTIALS" in err_msg:
                self.auth_error = "Invalid email or password."
            elif "USER_DISABLED" in err_msg:
                self.auth_error = "This account has been disabled."
            else:
                self.auth_error = "Login failed. Please check your internet connection."

    def login_with_google_credential(self, uid: str, email: str):
        """Called by Javascript after a successful Google popup sign in."""
        self.email = email
        events = self._handle_successful_login(uid)
        for evt in events:
            yield evt
        yield rx.redirect("/")

    def login_with_google_credential_wrapper(self, res: dict):
        if res and "uid" in res:
            return self.login_with_google_credential(res["uid"], res.get("email", ""))
        else:
            self.auth_error = "Google Login Failed or Cancelled."

    def trigger_google_login(self):
        """Mock Google sign in for demo purposes - simulates successful authentication."""
        # For demo purposes, we'll simulate a successful Google login
        # In production, this would use the actual Firebase Google Auth

        # Simulate Google user data
        mock_google_user = {
            "uid": "google_user_12345_demo",
            "email": "demo.user@gmail.com"
        }

        # Show loading state
        self.auth_error = ""
        yield

        # Simulate network delay
        import asyncio
        yield asyncio.sleep(1)

        # Process successful login
        events = self._handle_successful_login(mock_google_user["uid"])
        for evt in events:
            yield evt

        # Set user email for display
        self.email = mock_google_user["email"]

        yield rx.redirect("/")

    def _handle_successful_login(self, uid: str):
        """Common logic upon successful authentication."""
        self.firebase_uid = uid
        self.logged_in = True
        self.auth_error = ""
        
        # Real-world mapping logic: (Mocking map to 1705 like before)
        mapped_numeric_id = 1705  
        self.user_id = mapped_numeric_id
        
        # Check if user exists in the dataset
        try:
            if os.path.exists(DATA_PATH):
                data = pd.read_csv(DATA_PATH, usecols=["User's ID"])
                if self.user_id in data["User's ID"].values:
                    self.is_new_user = False
                else:
                    self.is_new_user = True
            else:
                self.is_new_user = True
        except Exception as e:
            self.is_new_user = True
            
        from state.cart_state import CartState
        from state.products_state import ProductsState
        return [
            CartState.load_cart_from_db(uid),
            ProductsState.load_searches_from_db(uid)
        ]
            
    def logout(self):
        """Reset state on logout."""
        self.user_id = -1
        self.logged_in = False
        self.is_new_user = True
        self.firebase_uid = ""

    def check_login_status(self):
        """Redirect to the login page if the user is not authenticated."""
        if not self.logged_in:
            return rx.redirect("/login")

    @rx.var
    def customer_display_name(self) -> str:
        """Computed property for customer identity."""
        return f"Customer: {self.email}" if self.email else "Customer: Guest"
