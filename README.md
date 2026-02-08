# 🛡️ Predictive Pipeline Integrity System

A multi-phase, AI-augmented engineering solution designed to synchronize 15 years of In-Line Inspection (ILI) data to predict pipeline corrosion risks through 2030.

---

## 📌 Project Overview
Pipeline operators often struggle to track specific corrosion anomalies across different inspection years due to sensor "drift" and inconsistent odometer readings. This system solves that problem by **aligning** 2007, 2015, and 2022 ILI logs into a single master baseline, **verifying** the data with generative AI, and **predicting** future wall-thickness loss.

---

## 🏗️ Technical Architecture & Workflow

### **Phase 1: Foundation & Alignment (The "Stapling" Process)**
Instead of aligning the entire pipeline at once, we used fixed physical structures to create a "Master Timeline."
* **Technologies:** Python, Pandas, AWS S3.
* **Process:** We used **Girth Welds** as anchor points. By "stapling" these fixed points across the 2007, 2015, and 2022 datasets, we eliminated global odometer drift, achieving sub-foot precision in feature location.
* **Benefit:** This creates a high-fidelity spatial baseline, ensuring that a defect found at 15,000 ft in 2007 is exactly the same one we look at in 2022.

### **Phase 2: The Matching Engine (Feature Synchronization)**
We narrowed down thousands of raw signals into a **"Golden Dataset"** of 42 high-confidence physical anomalies tracked over 15 years.
* **Technologies:** SciPy (`linear_sum_assignment`), Google Gemini 1.5 Flash.
* **Process:** * **Hungarian Algorithm:** We used an optimal pairing algorithm to minimize the spatial "cost" between 2015 and 2022 features.
    * **Agentic Verification:** We integrated **Gemini 1.5 Flash** as an auditor. The AI analyzed the depth changes; if a sensor suggested a pipe "healed" itself (depth reversal), the AI flagged it as a "Physical Impossibility" and excluded it from the growth model.
* **Benefit:** This prevents "sensor noise" from ruining the predictive math.

### **Phase 3: Analytics & Prediction (Risk Forecasting)**
* **Technologies:** AWS SageMaker, Scikit-Learn (Linear Regression), Plotly.
* **Process:** We calculated the **Corrosion Growth Rate (CGR)** for the verified survivors and used a regression model to project their depth to the year 2030.
* **Benefit:** Operators can now see not just where the pipe is thin today, but which spots are **"Fast-Growers"** that will become dangerous by 2030.

### **Phase 4: Intelligent Visualization**
* **Technologies:** Streamlit, AWS.
* **Tab 1 (Longitudinal Alignment):** Displays the 15-year history of matched features with 100% anchored precision.
* **Tab 2 (Risk Forecast):** An interactive **"Risk Radar"** that ranks defects by their 2030 predicted depth and future growth speed.

---

## 📊 Reliability & Results Matrix
Based on our final audit of the **"Golden 42"** high-confidence dataset:

| Metric | Result | Engineering Logic |
| :--- | :--- | :--- |
| **Reference Precision** | **High (Anchored)** | Achieved via Girth-Weld stapling to eliminate drift. |
| **Validated Survivors** | **42 Unique Sites** | Anomalies with a verified 15-year consensus history. |
| **Audit Consensus Score** | **90.4%** | Percentage of math predictions verified by Gemini as physically possible. |
| **Average Growth Rate** | **0.1175% / year** | The systemic pace of corrosion across verified sites. |
| **2030 Max Risk** | **32.3% Depth** | All features are predicted to stay well below the 80% failure limit. |

---

## 📊 Predictive Performance & Safety Results
Based on our 15-year longitudinal analysis and AI-verified 2030 forecast, the system provides the following safety metrics:

| Metric | Result | Engineering Significance |
| :--- | :--- | :--- |
| **2030 Maximum Risk** | **32.3% Depth** | The deepest predicted anomaly remains safely in the "Low" category. |
| **Failure Threshold** | **80% Wall Loss** | Industry-standard critical limit for immediate repair. |
| **Safety Margin** | **47.7%** | The gap between maximum predicted 2030 risk and failure limit. |
| **Integrity Verdict** | **SAFE** | All features are currently predicted to stay well below the 80% failure limit. |

---
## 📁 Final Deliverables

### **1. Master Tracking Report**
Our system successfully generated a **Master_Output.csv** that provides a 15-year traceable history for 42 verified anomalies.
* **Unique Traceability**: Every defect is assigned a persistent `Master_ID`.
* **High Confidence**: The average **Confidence_Score** across the dataset is **95.0%**, verified by both the Hungarian Algorithm and Gemini 1.5 Flash.

### **2. Safety Summary**
* **2030 Max Risk**: 32.3% Depth
* **Current Status**: **SAFE** (All features predicted to remain <80% through 2030).

### **3. AI Audit Results**
The AI-Model Consensus score of **90.4%** proves that our predictive math aligns with physical engineering realities. Our auditor successfully filtered out sensor noise where the pipe appeared to "heal" itself.
---

## 💡 Why This Solution Wins
* **Safety First:** By using AI to reject physically impossible data (like "shrinking" rust), we ensure repair budgets are spent on real threats, not sensor errors.
* **Scalable Intelligence:** Using AWS SageMaker and Gemini 1.5 Flash allows this system to process 100+ miles of pipeline data in minutes—a task that would take human engineers weeks.
* **Actionable Insights:** Instead of a static report, the Streamlit dashboard provides a living **"Radar"** that identifies the top 5 targets for preventative monitoring before they become critical.
