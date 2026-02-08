import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import linear_sum_assignment

def clean_clock(val):
    """Converts '03:00:00' or 3.0 or '3' into a float 3.0"""
    if pd.isna(val): return 0.0
    if isinstance(val, str) and ':' in val:
        return float(val.split(':')[0])
    try:
        return float(val)
    except:
        return 0.0

def robust_align(source_df, master_df, label):
    print(f"Aligning {label} to Master (2022)...")
    src_gw = source_df[source_df['feature_type'].str.contains('Weld|GW', case=False)].copy()
    mst_gw = master_df[master_df['feature_type'].str.contains('Weld|GW', case=False)].copy()

    common_src, common_mst = [], []
    for _, m_row in mst_gw.iterrows():
        distances = abs(src_gw['distance'] - m_row['distance'])
        if not distances.empty and distances.min() < 20: # 20ft window
            idx = distances.idxmin()
            common_src.append(src_gw.loc[idx, 'distance'])
            common_mst.append(m_row['distance'])
            src_gw = src_gw.drop(idx)

    print(f"   Found {len(common_src)} matching Girth Welds.")
    align_func = interp1d(common_src, common_mst, fill_value="extrapolate")
    source_df['adj_dist'] = align_func(source_df['distance'])
    return source_df

def match_anomalies(old_df, new_df):
    # Filter for Metal Loss / Corrosion
    old_anom = old_df[old_df['feature_type'].str.contains('Loss|Corrosion|Pitting', case=False, na=False)].copy()
    new_anom = new_df[new_df['feature_type'].str.contains('Loss|Corrosion|Pitting', case=False, na=False)].copy()
    
    if old_anom.empty or new_anom.empty:
        print("   ⚠️ No anomalies found to match.")
        return pd.DataFrame(columns=['old_idx', 'new_idx', 'match_score'])

    # Clean clock positions to floats
    old_anom['clock_float'] = old_anom['clock'].apply(clean_clock)
    new_anom['clock_float'] = new_anom['clock'].apply(clean_clock)

    matrix = np.zeros((len(old_anom), len(new_anom)))
    for i, r_old in enumerate(old_anom.itertuples()):
        for j, r_new in enumerate(new_anom.itertuples()):
            dist_gap = abs(r_old.adj_dist - r_new.distance)
            clock_gap = min(abs(r_old.clock_float - r_new.clock_float), 12 - abs(r_old.clock_float - r_new.clock_float))
            # Increase threshold to 10ft for hackathon testing
            matrix[i, j] = dist_gap + (clock_gap * 2) if dist_gap < 10 else 9999

    row_idx, col_idx = linear_sum_assignment(matrix)
    
    matches = []
    for r, c in zip(row_idx, col_idx):
        if matrix[r, c] < 50: # Reasonable threshold
            matches.append({'old_idx': old_anom.index[r], 'new_idx': new_anom.index[c]})
    
    return pd.DataFrame(matches)

# --- EXECUTION ---
df07 = pd.read_csv("standardized/ILI_2007_cleaned.csv")
df15 = pd.read_csv("standardized/ILI_2015_cleaned.csv")
df22 = pd.read_csv("standardized/ILI_2022_cleaned.csv")

df07 = robust_align(df07, df22, "2007")
df15 = robust_align(df15, df22, "2015")

print("Matching 2015 to 2022...")
matches_15_22 = match_anomalies(df15, df22)

# Verify if we found matches before merging
if not matches_15_22.empty:
    final_table = df22[df22['feature_type'].str.contains('Loss|Corrosion', case=False, na=False)].copy()
    final_table = final_table.rename(columns={'depth': 'depth_2022'})
    
    depth_map_15 = dict(zip(matches_15_22['new_idx'], matches_15_22['old_idx']))
    final_table['depth_2015'] = final_table.index.map(lambda x: df15.loc[depth_map_15[x], 'depth'] if x in depth_map_15 else np.nan)
    
    final_table.to_csv("master_alignment_results.csv", index=False)
    print(f"🚀 Success! Found {len(matches_15_22)}/{len(df15)} matches. Saved to master_alignment_results.csv")
else:
    print("❌ Critical Error: No matches found. Check your 'feature_type' filters.")

print("Matching 2007 to 2022...")
matches_07_22 = match_anomalies(df07, df22)

if not matches_07_22.empty:
    depth_map_07 = dict(zip(matches_07_22['new_idx'], matches_07_22['old_idx']))
    final_table['depth_2007'] = final_table.index.map(
        lambda x: df07.loc[depth_map_07[x], 'depth'] if x in depth_map_07 else np.nan
    )
    
    # Final save with all three years
    final_table.to_csv("master_alignment_results.csv", index=False)
    print(f"✅ Full timeline complete! Found {len(matches_07_22)}/{len(df07)} matches from 2007.")