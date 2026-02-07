

<img width="628" height="247" alt="image" src="https://github.com/user-attachments/assets/e48d2ef0-d0fb-42f6-9bae-6e55a73bb8ff" />


#### Phase 1: Data Ingestion & Normalization (The Foundation)

1. **S3 Storage:** Upload `2007.csv`, `2015.csv`, and `2022.csv` to an **Amazon S3** bucket.
2. **Schema Mapping:** Use a Python script (on **SageMaker** or **Lambda**) to rename inconsistent columns.
* *Example:* Map `ILI Wheel Count` (2022) and `log dist.` (2007) to a standard `corrected_dist` field.


3. **Feature Extraction:** Filter each dataset into two categories:
* **Reference Points:** Girth Welds, Valves, Tees.
* **Anomalies:** Metal loss, dents, corrosion.



#### Phase 2: Global Sequence Alignment (The "Brains")

1. **Anchor Alignment (DTW):** Use the **Dynamic Time Warping (DTW)** algorithm to align the distances of the 2007 and 2015 runs to the 2022 "Master" run. Use only the **Girth Welds** for this math.
2. **Piecewise Correction:** Since a pipeline is 100+ miles, don't align it all at once. Use a "sliding window" or align segment-by-segment between major **Valves**.
3. **Local Registration (ICP):** For clusters of defects, use **Iterative Closest Point (ICP)** to fine-tune the  coordinates (Distance and Clock Position).

#### Phase 3: Intelligent Matching & Entity Resolution

1. **Optimal Pairing (Hungarian Algorithm):** Build a "Cost Matrix" based on the spatial distance between the 2015 and 2022 points. Run the **Hungarian Algorithm** to find the 1-to-1 matches that minimize the total error.
2. **AI Verification (Gemini API):** For matches with a low confidence score, send the `Comments` and `Event Description` to **Google Gemini**.
* *Prompt:* "Is an 'External Metal Loss' at 10:00 o'clock in 2015 the same as 'General Corrosion' at 10:05 in 2022?"



#### Phase 4: Prediction & Risk Assessment

1. **Growth Calculation:** Calculate the **Corrosion Growth Rate (CGR)** for every matched pair: .
2. **Predictive Modeling:** Use **AWS SageMaker** to train a simple regression model to project the depth of these anomalies for the next 5 and 10 years.
3. **Risk Flagging:** Identify any "Threats" where the predicted depth exceeds 80% of the wall thickness.

#### Phase 5: Visualization & Delivery

1. **Streamlit Dashboard:** Host a **Streamlit** app on AWS.
* **Tab 1:** "Alignment View" showing the 2007/2015/2022 logs synced.
* **Tab 2:** "Risk Map" showing the location of anomalies with the highest growth rates.


2. **Final Report:** Generate a CSV output that includes a unique `Master_ID` for every defect so its history can be tracked across all three years.

---

### Why this Workflow Wins:

* **Scalability:** It uses **AWS** to handle data that would crash a local laptop.
* **Accuracy:** It uses **DTW** and the **Hungarian Algorithm** as specified in the "Technical Considerations."
* **Innovation:** It uses **Gemini** to solve the "human" part of the problem—interpreting messy notes and comments.
