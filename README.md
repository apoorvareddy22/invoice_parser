
# 🧾 Invoice Parser & Search App

This project is a complete pipeline for parsing, storing, and exploring scanned invoice documents using AI-powered extraction and modern data visualization tools.

---

## 🚀 Features

- OCR + LayoutLM for field extraction from scanned invoices
- Batch parsing and JSON ground-truth comparison
- FastAPI backend for structured querying
- Streamlit dashboard for filtering, searching, and visualization
- Invoice search by keywords, vendors, dates, and more

---

## 📊 Screenshots

### FastAPI Swagger UI
![FastAPI UI](./assets/swagger_ui.png)

### Streamlit Dashboard
![Streamlit UI](./assets/streamlit_ui.png)

---

## 📂 Folder Structure

```
invoice_parser/
├── app/                    # Core app logic
├── data/                   # Invoices, output.json, etc.
├── scripts/                # Batch parse + analytics
├── invoice_search_app.py   # Streamlit dashboard
├── README.md
├── requirements.txt
└── ...
```

---

## 🛠️ Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/invoice_parser.git
cd invoice_parser

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI backend
uvicorn app.main:app --reload

# Run the Streamlit app
streamlit run invoice_search_app.py
```

---

## 📌 Dependencies

All dependencies are listed in `requirements.txt`. Key libraries include:
- `transformers`, `sentence-transformers`
- `fastapi`, `pydantic`, `uvicorn`
- `streamlit`, `matplotlib`, `pandas`

---

## 📄 License

MIT License © 2025

---

Made with ❤️ for structured data from messy invoices.
