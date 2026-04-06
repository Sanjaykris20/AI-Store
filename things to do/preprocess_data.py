import pandas as pd
import numpy as np

def preprocess_data(file_path):

    df = pd.read_csv(file_path)

    # Replace invalid empty values
    df.replace("", np.nan, inplace=True)

    # Convert ID columns
    df["User's ID"] = pd.to_numeric(df["User's ID"], errors='coerce')
    df["ProdID"] = pd.to_numeric(df["ProdID"], errors='coerce')

    # Remove rows with missing IDs
    df.dropna(subset=["User's ID","ProdID"], inplace=True)

    # Remove zero IDs
    df = df[(df["User's ID"] != 0) & (df["ProdID"] != 0)]

    # Drop unwanted column
    if "Unnamed: 0" in df.columns:
        df.drop("Unnamed: 0", axis=1, inplace=True)

    # Fill text columns
    text_cols = ["Category","Brand","Name","Description","Tags"]
    for col in text_cols:
        df[col] = df[col].fillna("")

    # Clean image URLs
    if "ImageURL" in df.columns:
        df["ImageURL"] = df["ImageURL"].str.replace("|","", regex=False)

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df


# Test
if __name__ == "__main__":
    cleaned_df = preprocess_data("clean_data.csv")
    print(cleaned_df.head())
