import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# LOAD
# ─────────────────────────────────────────────
df = pd.read_csv(r'data\processed_sales.csv')
print(f"Original shape: {df.shape}")

# ─────────────────────────────────────────────
# 1. STANDARDISE CATEGORY
#    Handles: 'elec', 'Elec', 'Electronics ', ' electronics', ' Furniture ', 'furnitur', etc.
# ─────────────────────────────────────────────
def standardise_category(val):
    v = str(val).strip().lower()
    if v in ('electronics', 'elec', 'electronic', ' electronics'):
        return 'Electronics'
    elif v in ('furniture', 'furnitur', ' furniture ', 'furnitu'):
        return 'Furniture'
    else:
        return val.strip()   # keep original if truly unknown

df['category'] = df['category'].apply(standardise_category)
print(f"\n[1] Categories after standardisation:\n{df['category'].value_counts().to_string()}")

# ─────────────────────────────────────────────
# 2. FIX WRONG CATEGORY (product ↔ category mismatch)
# ─────────────────────────────────────────────
electronics_products = {'Phone','Laptop','Monitor','Keyboard','Webcam',
                        'Mouse','Tablet','Headphones'}
furniture_products   = {'Table','Chair','Desk','Shelf','Sofa'}

def correct_category(row):
    product  = row['product']
    category = row['category']
    if product in electronics_products and category != 'Electronics':
        return 'Electronics'
    if product in furniture_products and category != 'Furniture':
        return 'Furniture'
    return category

df['category'] = df.apply(correct_category, axis=1)
print(f"\n[2] Categories after product-mismatch fix:\n{df['category'].value_counts().to_string()}")

# ─────────────────────────────────────────────
# 3. REMOVE NEGATIVE QUANTITIES (likely data-entry or return errors)
# ─────────────────────────────────────────────
neg_mask = df['quantity'] < 0
print(f"\n[3] Removing {neg_mask.sum()} rows with negative quantity.")
df = df[~neg_mask].copy()

# ─────────────────────────────────────────────
# 4. REMOVE PRICE OUTLIERS (> 3 standard deviations)
# ─────────────────────────────────────────────
mean_p = df['price'].mean()
std_p  = df['price'].std()
outlier_mask = df['price'] > mean_p + 3 * std_p
print(f"\n[4] Removing {outlier_mask.sum()} rows with extreme price outliers "
      f"(threshold: ₹{mean_p + 3*std_p:,.0f}).")
df = df[~outlier_mask].copy()

# ─────────────────────────────────────────────
# 5. RECALCULATE REVENUE (ensure consistency)
# ─────────────────────────────────────────────
df['revenue'] = df['quantity'] * df['price']
print(f"\n[5] Revenue recalculated as quantity × price for all rows.")

# ─────────────────────────────────────────────
# 6. STANDARDISE DATE FORMAT  →  YYYY-MM-DD
# ─────────────────────────────────────────────
df['date'] = pd.to_datetime(df['date'], format='mixed', dayfirst=False)
df['date'] = df['date'].dt.strftime('%Y-%m-%d')
print(f"\n[6] Dates normalised to YYYY-MM-DD.")
print(f"    Sample: {df['date'].head(5).tolist()}")

# ─────────────────────────────────────────────
# 7. REMOVE DUPLICATE ORDER IDs (keep first occurrence)
# ─────────────────────────────────────────────
before = len(df)
df = df.drop_duplicates(subset='order_id', keep='first').reset_index(drop=True)
print(f"\n[7] Removed {before - len(df)} duplicate order_id rows.")

# ─────────────────────────────────────────────
# 8. RESET INDEX
# ─────────────────────────────────────────────
df = df.reset_index(drop=True)

# ─────────────────────────────────────────────
# FINAL REPORT
# ─────────────────────────────────────────────
print("\n" + "="*50)
print("CLEANING COMPLETE")
print("="*50)
print(f"Final shape  : {df.shape}")
print(f"Null values  :\n{df.isnull().sum().to_string()}")
print(f"\nCategories   :\n{df['category'].value_counts().to_string()}")
print(f"\nQuantity range: {df['quantity'].min()} – {df['quantity'].max()}")
print(f"Price range   : ₹{df['price'].min():,.0f} – ₹{df['price'].max():,.0f}")
print(f"\nSample (first 5 rows):\n{df.head().to_string()}")

# ─────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────
output_path = r'data\processed_sales_1.csv'
df.to_csv(output_path, index=False)
print(f"\n✅  Saved to: {output_path}")