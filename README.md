# Used-Car Market Intelligence — Business Analyst Portfolio Project

## Project overview
An interactive Python dashboard to explore used-car listings in India. It demonstrates a business-analysis workflow: data inspection, filtering, KPI definition, exploratory analysis, visual storytelling, and business recommendations.

**Important:** `data/used_car_listings.csv` is synthetic demonstration data created for this portfolio project. It is not scraped from a marketplace and should not be presented as actual market research.

## Business questions
1. Which brands and vehicle segments have the largest listing counts?
2. How do average listed prices differ by city, brand, and fuel type?
3. How are vehicle age and kilometres driven associated with listed price?
4. What proportion of the sample is marked available versus sold?
5. What additional data would be needed before making inventory or pricing decisions?

## Features
- Interactive filters for city, brand, fuel, listing status, vehicle age, and price cap
- KPI cards: listings analyzed, average price, median price, sold share
- Charts for brand and city comparisons, segment mix, age/mileage relationships, fuel-type pricing, and listing status
- Data explorer with CSV download
- Automatically generated observations based on the current filters

## Run in PyCharm
1. Install Python 3.10 or newer.
2. Open PyCharm and choose **Open**; select this project folder.
3. Configure a Python interpreter/virtual environment.
4. Open the PyCharm terminal in the project folder.
5. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Start the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

7. Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser.
8. Stop the app with `Ctrl+C` in the terminal.

## Project structure
```text
used_car_business_analyst_project/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── used_car_listings.csv
├── sql/
│   └── business_questions.sql
└── outputs/
    └── (place exported screenshots/reports here)
```

## Suggested next improvements
- Replace or supplement the synthetic data with a properly licensed public dataset.
- Add data-quality checks and document assumptions.
- Load the CSV into SQLite/PostgreSQL and run the SQL queries in `sql/business_questions.sql`.
- Add a short executive summary with evidence-backed recommendations.
- Publish the source code and README on GitHub; include dashboard screenshots.

## Resume bullet (use after you have run and reviewed the project)
**Used-Car Market Intelligence Dashboard | Python, Pandas, Plotly, Streamlit, SQL**
- Built an interactive dashboard to analyze 1,500 synthetic used-car listings across multiple cities, brands, and vehicle segments.
- Explored pricing relationships with vehicle age, kilometres driven, fuel type, and ownership history.
- Created dynamic filters, KPI cards, and business observations to demonstrate how marketplace teams could investigate inventory and pricing decisions.

Be transparent that the data is synthetic. Do not claim business impact or causal findings that the dataset cannot establish.
