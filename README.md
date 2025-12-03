# AI Outcomes Synthesizer

A multimodal **Precision Analytics** engine for computational psychiatry research. This project generates realistic synthetic longitudinal mental-health datasets (clinical, sensor, and EMA-style text), performs mixed-effects modeling, creates plots, and uses LLMs to generate manuscript-ready research summaries.

This project mirrors workflows used in and focusing on:
- Longitudinal modeling
- Multimodal data fusion
- Digital phenotyping
- AI-assisted scientific writing

---

## 🚀 Features
- **Synthetic multimodal dataset generation**
  - Clinical outcomes
  - Sensor-derived features (steps, sleep, phone use)
  - EMA-style qualitative text notes
- **Mixed-effects longitudinal modeling** (`statsmodels`)
- **Automatic EDA plots**
- **LLM-generated Methods, Results, Executive Summary**
- **Downloadable Markdown report**
- **Streamlit UI** for easy research workflows

---

## 📦 Installation

Clone the repository:
```powershell
cd C:\dev
git clone https://github.com/<your-username>/ai-outcomes-synthesizer.git
cd ai-outcomes-synthesizer
```

Create a virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🧬 Generate Synthetic Data
Run the script:
```powershell
python .\src\generate_multimodal_data.py
```
This creates:
```
data/
├── clinical_longitudinal_data.csv
├── sensor_longitudinal_data.csv
└── text_notes_longitudinal_data.csv
```
<img width="1177" height="1309" alt="ai-ouctomes-synthesizer ERD" src="https://github.com/user-attachments/assets/d09c8e35-75e0-48c4-aa09-0c71abad398d" />

---

## ▶️ Run the App
```powershell
streamlit run .\src\app.py
```

This launches the interactive research dashboard.

---

## 🖥️ Using the App
1. Upload **clinical_longitudinal_data.csv**
2. Upload **config_example.json**
3. Click **Run Analysis**

You will see:
- EDA
- Mixed-effects model
- Data plots
- Sensor relationships
- AI-written research sections
- **Downloadable report.md**

---

## 📁 Project Structure
```
ai-outcomes-synthesizer/
│
├── data/                         # Generated multimodal data
├── src/
│   ├── app.py                    # Streamlit app
│   ├── generate_multimodal_data.py
│   ├── data_loader.py
│   ├── analysis.py
│   ├── plotting.py
│   ├── llm_writer.py
│   ├── report_generator.py
│   └── __init__.py
│
├── config_example.json
├── requirements.txt
└── README.md
```

---

## 🧠 AI Models Used
### **Classical Model**
- **Mixed-Effects Linear Model (MixedLM)**  
Used for longitudinal clinical modeling, treatment effects, and covariate adjustment.

### **LLM (Generative AI)**
- Powered via `OpenAI` API  
Generates:
- Methods
- Results
- Executive summary
- Text explanations

### **Synthetic Data Generators**
- Rule-based generative engine for clinical + sensor + text data

---

## 📊 Multimodal Relationships Modeled
Symptoms influence:
- **↓ steps** (psychomotor slowing, reduced activity)
- **↓ sleep stability** (insomnia, circadian disruption)
- **↑ phone use** (rumination, distraction behaviors)

These patterns mirror digital phenotyping literature.

---

## 🧪 Example Research Use-Cases
- Computational psychiatry modeling
- Treatment response prediction
- Multimodal data fusion
- LLM-assisted qualitative + quantitative synthesis
- Longitudinal trajectory modeling
- Precision analytics prototyping

---

## 📝 Roadmap
- Add Reinforcement Learning–based patient modeling
- Add Drift Diffusion Models (DDM) for cognitive biometrics
- Add multimodal transformers
- Add cluster-based patient trajectory analysis
- Add clinician-facing PDF report generator

---

## 📜 License
MIT License.

---

## 📬 Contact
For collaboration or research inquiries, open an Issue or contact the project maintainer.

