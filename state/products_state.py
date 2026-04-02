import reflex as rx
import pandas as pd
import os
from typing import List, Dict, Any
from config import DATA_PATH

class ProductsState(rx.State):
    """Local state for fetching global catalog of products."""
    all_products: List[Dict[str, Any]] = []
    search_query: str = ""
    past_searches: List[str] = []
    sort_order: str = "default" # default, low_to_high, high_to_low
    
    def sync_searches_to_db(self):
        """Push the current search history to Firebase."""
        from state.user_state import get_firebase_db, UserState
        try:
            uid = self.get_state(UserState).firebase_uid
            db = get_firebase_db()
            if db and uid:
                db.child("users").child(uid).child("searches").set(self.past_searches)
        except Exception as e:
            print(f"Failed to sync searches: {e}")

    def load_searches_from_db(self, uid: str):
        """Load search items from Firebase on login."""
        from state.user_state import get_firebase_db
        db = get_firebase_db()
        if db and uid:
            try:
                search_data = db.child("users").child(uid).child("searches").get().val()
                if search_data:
                    self.past_searches = [item for item in search_data if item is not None]
                else:
                    self.past_searches = []
            except Exception as e:
                print(f"Failed to load searches: {e}")
    
    def fetch_products(self):
        # Extract query from URL if visiting via search redirect
        params = self.router.page.params
        if "q" in params:
            self.search_query = params["q"]
        else:
            self.search_query = ""
            
        try:
            if os.path.exists(DATA_PATH):
                data = pd.read_csv(DATA_PATH)
                unique_products = data.drop_duplicates(subset=['ProdID']).copy()
                
                # Pre-calculate prices for sorting (since they are synthetic)
                unique_products["Price_Num"] = unique_products["ProdID"].astype(int).apply(lambda x: (x % 2500) + 499)
                
                # Filter
                if self.search_query:
                    if self.search_query not in self.past_searches:
                        self.past_searches.append(self.search_query)
                        # Keep only last 10 searches to prevent data bloat
                        if len(self.past_searches) > 10:
                            self.past_searches.pop(0)
                        self.sync_searches_to_db()
                        
                    mask = (
                        unique_products['Brand'].str.contains(self.search_query, case=False, na=False) |
                        unique_products['Category'].str.contains(self.search_query, case=False, na=False) |
                        unique_products['Description'].str.contains(self.search_query, case=False, na=False)
                    )
                    unique_products = unique_products[mask]
                
                # Sort
                if self.sort_order == "low_to_high":
                    unique_products = unique_products.sort_values("Price_Num", ascending=True)
                elif self.sort_order == "high_to_low":
                    unique_products = unique_products.sort_values("Price_Num", ascending=False)
                
                # Cap and Fill
                unique_products = unique_products.head(48).fillna('')
                unique_products["Price"] = unique_products["Price_Num"].apply(lambda x: f"{x}.00")
                
                if "ImageURL" in unique_products.columns:
                    unique_products["ImageURL"] = unique_products["ImageURL"].apply(lambda x: str(x).split(" | ")[0] if pd.notnull(x) and str(x) != "" else "/placeholder.jpg")
                if "Rating" in unique_products.columns:
                    unique_products["Rating"] = unique_products["Rating"].apply(lambda x: f"{float(x):.1f}" if pd.notnull(x) and str(x) != "" else "N/A")
                
                self.all_products = unique_products.to_dict('records')
        except Exception as e:
            print(f"Error fetching products: {e}")

    def update_sort(self, val: str):
        self.sort_order = val
        return self.fetch_products()

    def update_search(self, q: str):
        self.search_query = q
        return self.fetch_products()
    
    def handle_search_submit(self, form_data: Dict[str, Any]):
        query = form_data.get("q", "")
        # Force a redirect to the home page with the query
        return rx.redirect(f"/?q={query}")
