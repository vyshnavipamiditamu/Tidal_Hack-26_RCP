import pandas as pd
import boto3
import io
import os

# 1. Detect environment
IS_AWS = os.environ.get('AWS_EXECUTION_ENV') is not None

def lambda_handler(event, context):
    # --- CONFIGURATION ---
    bucket_name = "your-hackathon-bucket"
    input_file = "ILIDataV2.xlsx"
    years = ["2007", "2015", "2022"]
    
    mappings = {
        "2007": {"log dist. [ft]": "distance", "o'clock": "clock", "event": "feature_type", "depth [%]": "depth", "length [in]": "length", "width [in]": "width"},
        "2015": {"Log Dist. [ft]": "distance", "O'clock": "clock", "Event Description": "feature_type", "Depth [%]": "depth", "Length [in]": "length", "Width [in]": "width"},
        "2022": {"ILI Wheel Count \n[ft.]": "distance", "O'clock\n[hh:mm]": "clock", "Event Description": "feature_type", "Metal Loss Depth \n[%]": "depth", "Length [in]": "length", "Width [in]": "width"}
    }

    try:
        # 2. LOAD DATA: S3 vs Local
        if IS_AWS:
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=bucket_name, Key=input_file)
            excel_data = response['Body'].read()
        else:
            # Local mode: read directly from file
            with open(input_file, "rb") as f:
                excel_data = f.read()

        for year in years:
            df = pd.read_excel(io.BytesIO(excel_data), sheet_name=year)
            df = df.rename(columns=mappings[year])
            df['survey_year'] = int(year)
            
            target_cols = ["distance", "clock", "feature_type", "depth", "length", "width", "survey_year"]
            existing_cols = [c for c in target_cols if c in df.columns]
            df_final = df[existing_cols]

            # 3. SAVE DATA: S3 vs Local
            output_folder = "standardized"
            output_filename = f"ILI_{year}_cleaned.csv"
            
            if IS_AWS:
                csv_buffer = io.StringIO()
                df_final.to_csv(csv_buffer, index=False)
                s3.put_object(Bucket=bucket_name, Key=f"{output_folder}/{output_filename}", Body=csv_buffer.getvalue())
            else:
                # Local mode: create folder and save file
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                df_final.to_csv(os.path.join(output_folder, output_filename), index=False)
            
            print(f"✅ Processed {year} successfully.")

        return {"statusCode": 200, "body": "Standardization complete."}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"statusCode": 500, "body": str(e)}

# 4. Trigger for local testing
if __name__ == "__main__":
    lambda_handler({}, None)