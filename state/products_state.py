import reflex as rx
import pandas as pd
import os
from typing import List, Dict, Any

# Resolve CSV path relative to this file so it works locally AND on Reflex Cloud
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
CSV_PATH = os.path.join(_ROOT, "cleaned_data.csv")

class ProductsState(rx.State):
    """Local state for fetching global catalog of products."""
    all_products: List[Dict[str, Any]] = []
    search_query: str = ""
    sort_order: str = "default" # default, low_to_high, high_to_low
    
    def fetch_products(self):
        # Extract query from URL if visiting via search redirect
        params = self.get_query_params()
        if "q" in params:
            self.search_query = params["q"]
            
        try:
            if os.path.exists(CSV_PATH):
                data = pd.read_csv(CSV_PATH)

                unique_products = data.drop_duplicates(subset=['ProdID'])
                
                # Pre-calculate prices for sorting (since they are synthetic)
                unique_products["Price_Num"] = unique_products["ProdID"].astype(int).apply(lambda x: (x % 2500) + 499)
                
                # Filter
                if self.search_query:
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
        # Force a redirect to the products page with the query
        return rx.redirect(f"/products?q={query}")
