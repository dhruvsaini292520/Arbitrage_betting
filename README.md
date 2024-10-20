# Arbitrage Betting Detector

A web application for detecting opportunities for arbitrage betting in soccer matches. The application is built using Python, Streamlit, and Plotly, and provides users with visual tools to gauge the implied probabilities of outcomes in soccer games.

## Table of Contents
- Overview
- Features
- Installation
- Usage
- Project Structure
- Dependencies
- Contributing
- License

## Overview
This project provides an easy-to-use web interface that helps users identify arbitrage opportunities in soccer betting markets. By analyzing the implied probabilities of home win, draw, and away win outcomes, the app helps betting websites to evaluate the total implied probability of a match, highlighting potential risk of arbitrage opportunities for bettors.

## Features
- **Data Visualization**: Displays implied probabilities using an interactive gauge chart and a radar chart.
- **Probability Analysis**: Visualize the implied probability of home, draw, and away outcomes in a soccer match.
- **Arbitrage Detection**: Alerts users if arbitrage betting is possible based on calculated probabilities.
- **User-friendly Interface**: Built with Streamlit for easy and interactive usage.

## Installation
To get started with the Arbitrage Betting Detector, follow these steps:

### Clone the Repository
```bash
git clone https://github.com/rdeshir10/Arbitrage_betting.git
cd Arbitrage_betting
```

### Set Up a Virtual Environment
It's recommended to create a virtual environment to manage dependencies:
```bash
python -m venv env
source env/bin/activate # On Windows use `env\Scripts\activate`
```

### Install Dependencies
Install the required dependencies from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Run the Application
Launch the Streamlit application:
```bash
streamlit run app2.py
```

## Usage
Once the application is running, you can use it as follows:

- **Upload Match Data**: Upload a CSV file containing match data, including probabilities for home win, draw, and away win.
- **Preview Data**: Click on "Preview Data" to see a summary of the data you uploaded.
- **Analyze Probabilities**: Use the provided visualizations (gauge and radar charts) to analyze the implied probabilities of the match outcomes.
- **Arbitrage Detection**: The app will display whether arbitrage betting is possible based on the given probabilities, along with a thumbs-up or thumbs-down image.

## Project Structure
The key files and directories in the project are:
```
Arbitrage_betting/
├── app2.py # Main application script for Streamlit
├── requirements.txt # List of dependencies
├── README.md # Project documentation
└── assets/ # Images and other assets used in the application
```

## Dependencies
The key dependencies for the project are:

- **Streamlit**: For building the interactive web interface.
- **Pandas**: For handling match data and probability calculations.
- **Plotly**: For generating interactive visualizations (gauge and radar charts).
- **XGBoost**: If the application uses machine learning for prediction.
- **Matplotlib**: For additional visual representation of data.

All required dependencies are listed in the `requirements.txt` file, which can be installed using `pip`.

## Proposed Improvements for Betting Website/Model

- **Arbitrage Betting Options**:
Implement a feature that captures and displays all potential arbitrage betting opportunities for specific dates. This will allow users to easily identify risky scenarios across various fixtures. Instead of the user inputting data for each individual fixture. 

- **Optimal Odds Calculation**:
Develop a tool that calculates optimal odds for the listed fixtures.

- **Risk Assessment Tab**:
Introduce a dedicated tab that evaluates the risk level of their chosen betting website. This tool will analyze various factors to determine the site's exposure to risk.

- **Odds Adjustment Recommendations**:
Based on the risk assessment, provide users with recommended changes to odds that can mitigate identified risks. This will empower users to make chnages to reduce their risks.

- **Model Development**:
Build a predictive model incorporating these adjustments, which can be integrated into the website's front end. This model will enhance user experience by providing tailored recommendations based on current data.

