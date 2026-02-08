import pandas as pd
import numpy as np
import uuid

def generate_final_report(input_csv='GENTOO_DASHBOARD_DATA.csv', ai_csv='ai_audited.csv'):
    # Load the datasets
    df = pd.read_csv(input_csv)
    ai_df = pd.read_csv(ai_csv)
    
    # 1. Generate Unique Master_IDs for every physical defect
    df['Master_ID'] = [f"FEAT-{str(uuid.uuid4())[:8].upper()}" for _ in range(len(df))]
    
    # 2. Calculate Confidence_Score
    # Logic: Base 100% - deduct for high spatial cost or AI warnings
    conf_scores = []
    for i, row in df.iterrows():
        base_conf = 95.0 # Starting high for matched survivors
        
        # Check corresponding AI verdict
        site_audit = ai_df[ai_df['distance'] == row['distance']]
        if not site_audit.empty:
            verdict = site_audit.iloc[0]['ai_verdict']
            if verdict == 'REJECT': base_conf -= 40.0
            if verdict == 'EXTREME': base_conf -= 15.0
            if verdict == 'NEW': base_conf += 2.0 # Higher confidence for new initiations
            
        conf_scores.append(min(max(base_conf, 0.0), 100.0))
    
    df['Confidence_Score'] = conf_scores
    
    # 3. Final Column Selection as per Requirements
    final_cols = [
        'Master_ID', 'distance', 'clock', 'depth_2007', 
        'depth_2015', 'depth_2022', 'CGR', 
        'predicted_depth_2030', 'Risk_Level', 'Confidence_Score'
    ]
    
    output_df = df[final_cols]
    output_df.to_csv('Master_Output.csv', index=False)
    print("✅ Final Report Generated: Master_Output.csv")

if __name__ == "__main__":
    generate_final_report()