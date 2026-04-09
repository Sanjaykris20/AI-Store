import reflex as rx
import pandas as pd
import os
from typing import List, Dict, Any
from config import DATA_PATH

class ProductsState(rx.State):
    """Local state for fetching global catalog of products."""
    all_products: List[Dict[str, Any]] = []
    filtered_products: List[Dict[str, Any]] = []
    search_query: str = ""
    selected_category: str = "All Categories"
    sort_by: str = "Price: Low to High"
    items_per_page: int = 20
    current_page: int = 1
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
        try:
            # Try to get params from router (handle both old and new API)
            if hasattr(self.router, 'url_params'):
                params = self.router.url_params
            else:
                params = self.router.page.params if hasattr(self.router, 'page') else {}
            
            if "q" in params:
                self.search_query = params["q"]
            else:
                self.search_query = ""
        except Exception:
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
                self.apply_filters()  # Apply initial filters
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

    def set_search_query(self, value: str):
        """Set search query and apply filters."""
        self.search_query = value
        self.apply_filters()

    def set_selected_category(self, value: str):
        """Set selected category and apply filters."""
        self.selected_category = value
        self.apply_filters()

    def set_sort_by(self, value: str):
        """Set sort option and apply filters."""
        self.sort_by = value
        self.apply_filters()

    def apply_filters(self):
        """Apply search, category, and sort filters to products."""
        filtered = self.all_products.copy()

        # Apply search filter
        if self.search_query:
            filtered = [
                product for product in filtered
                if self.search_query.lower() in product.get('Brand', '').lower() or
                   self.search_query.lower() in product.get('Category', '').lower() or
                   self.search_query.lower() in product.get('Description', '').lower()
            ]

        # Apply category filter
        if self.selected_category != "All Categories":
            filtered = [
                product for product in filtered
                if product.get('Category', '') == self.selected_category
            ]

        # Apply sorting
        if self.sort_by == "Price: Low to High":
            filtered.sort(key=lambda x: float(x.get('Price_Num', 0)))
        elif self.sort_by == "Price: High to Low":
            filtered.sort(key=lambda x: float(x.get('Price_Num', 0)), reverse=True)
        elif self.sort_by == "Rating":
            filtered.sort(key=lambda x: float(x.get('Rating', '0').replace('N/A', '0')), reverse=True)
        elif self.sort_by == "Newest":
            filtered.sort(key=lambda x: x.get('ProdID', 0), reverse=True)

        # Apply pagination
        start_idx = 0
        end_idx = self.current_page * self.items_per_page
        self.filtered_products = filtered[:end_idx]

    def load_more_products(self):
        """Load more products for pagination."""
        self.current_page += 1
        self.apply_filters()
