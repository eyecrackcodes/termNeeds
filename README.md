# Life Insurance Calculator

A simple Streamlit app that calculates life insurance needs based on various financial inputs and generates downloadable PDF reports.

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your default web browser at http://localhost:8501.

## Deployment

This app can be easily deployed on Streamlit Cloud:

1. Push this repository to GitHub
2. Go to https://streamlit.io/cloud
3. Create an account if you don't have one
4. Click "New app" and select your repository
5. Set the main file path to `app.py`
6. Click "Deploy"

## Features

- Calculates required life insurance amount based on:
  - Income needs
  - Final expenses
  - Mortgage and debts
  - College costs
- Takes into account existing assets:
  - Savings and investments
  - Retirement savings
  - Current life insurance coverage
- Clean, organized UI with expandable sections
- Generates downloadable PDF reports
- Client-friendly interface that can be shared via link
- Includes an informational "About" page with instructions
- Provides a clear summary of results with formatted data tables

## Usage for Financial Advisors

1. Share the URL with clients for them to fill out on their own
2. Have clients download and send you the PDF report
3. Use the app during client meetings to calculate insurance needs in real-time
4. Generate PDF reports for client files and documentation 