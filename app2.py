import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import plotly.graph_objects as go
# Apply full-page width
st.set_page_config(layout="wide")
# Load pre-trained machine learning model (RandomForest)
with open('arbitrage_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
# Function to make predictions using the loaded model
def classification_model(data):
    prediction = model.predict(data)
    # return prediction
    return "YES" if prediction == 1 else "NO"
# Function to create a gauge chart for total probability
def create_gauge_chart(total_prob, title="Total Implied Probability"):
    # Ensure the total probability is within 0-100 range
    if total_prob > 100:
        total_prob = 100
    elif total_prob < 0:
        total_prob = 0
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total_prob,
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "lightblue"}},
        title={'text': title}
    ))
    return fig
# Display the custom header image at the top of the page
st.image("https://files.oaiusercontent.com/file-tKT6fPrnuoa84PeHTRMKROZE?se=2024-10-15T23%3A38%3A44Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D738e7c86-790c-465b-ba11-a042017853a2.webp&sig=RDwu77dqshhm69Yx2ZOqVZLrxZ/12znVp0IOoe3noZ0%3D")
# Streamlit UI with full-page design
st.title("BET ARBITRAGE AI PREDICTOR")
# Full-page layout using columns and CSS
col1, col2 = st.columns([1, 5])
# File uploader to upload CSV with a single row of data
uploaded_file = st.file_uploader("Load Single Game Data (1 Row CSV File)", type="csv")
# Initialize an empty DataFrame
df = pd.DataFrame()
# If a file is uploaded
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Calculate the average home, draw, and away probabilities across all bookmakers
    df['Avg_Home_Prob'] = 1 / df.filter(like='Home_Odds_').mean(axis=1)
    df['Avg_Draw_Prob'] = 1 / df.filter(like='Draw_Odds_').mean(axis=1)
    df['Avg_Away_Prob'] = 1 / df.filter(like='Away_Odds_').mean(axis=1)
    # Calculate total probability
    df['Total_Prob'] = df['Avg_Home_Prob'] + df['Avg_Draw_Prob'] + df['Avg_Away_Prob']
    
    # Calculate arbitrage opportunity
    df['Arbitrage_Opportunity'] = df['Total_Prob'] < 1
    # Preview the data and visualize it
    st.markdown(
    """
    <style>
    .hometeam-title {
        font-size: 22px;
        font-weight: bold;
        color:  #2ca02c;
    }
    .awayteam-title {
        font-size: 22px;
        font-weight: bold;
        color: #1f77b4;
    }
    .probability {
        font-size: 18px;
        margin-bottom: 5px;
    }
    .highlight {
        font-weight: bold;
        font-size: 18px;
        color: #d62728;
    }
    .separator {
        margin-top: 20px;
        margin-bottom: 20px;
        border-top: 2px solid #ccc;
    }
    </style>
    """, 
    unsafe_allow_html=True
    )
# Display formatted content
if st.button("Preview Data"):
    st.write("### Data Preview:")
    
    # Convert the probabilities to percentages for better readability
    df['Avg_Home_Prob_Percentage'] = (df['Avg_Home_Prob'] * 100).round(2)
    df['Avg_Draw_Prob_Percentage'] = (df['Avg_Draw_Prob'] * 100).round(2)
    df['Avg_Away_Prob_Percentage'] = (df['Avg_Away_Prob'] * 100).round(2)
    df['Total_Prob_Percentage'] = (df['Total_Prob'] * 100).round(2)
    
    # Rename columns for better display names
    df_display = df[['Home_Team', 'Away_Team', 'Avg_Home_Prob_Percentage', 
                    'Avg_Draw_Prob_Percentage', 'Avg_Away_Prob_Percentage', 
                    'Total_Prob_Percentage']].rename(columns={
        'Home_Team': 'Home Team',
        'Away_Team': 'Away Team',
        'Avg_Home_Prob_Percentage': 'Home Win Implied Probability (%)',
        'Avg_Draw_Prob_Percentage': 'Draw Implied Probability (%)',
        'Avg_Away_Prob_Percentage': 'Away Win Implied Probability (%)',
        'Total_Prob_Percentage': 'Total Implied Probability (%)'
    })
    # Display the data in a vertical format with enhanced styling
    for index, row in df_display.iterrows():
        st.markdown(f"<div class='hometeam-title'>Home Team: {row['Home Team']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='awayteam-title'>Away Team: {row['Away Team']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='probability'>Home Win Implied Probability: <span class='highlight'>{row['Home Win Implied Probability (%)']:.2f}%</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='probability'>Draw Implied Probability: <span class='highlight'>{row['Draw Implied Probability (%)']:.2f}%</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='probability'>Away Win Implied Probability: <span class='highlight'>{row['Away Win Implied Probability (%)']:.2f}%</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='probability'>Total Implied Probability: <span class='highlight'>{row['Total Implied Probability (%)']:.2f}%</span></div>", unsafe_allow_html=True)
        # Create and display gauge chart for Total Implied Probability
        st.plotly_chart(create_gauge_chart(row['Total Implied Probability (%)'], "Total Implied Probability Gauge"))
        # Separator for each row
        st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
        
# Submit button for model prediction
if st.button("Submit"):
    if len(df) == 1:  # Ensure it's a single-row CSV
            st.write("Running the model...")
            # Prepare data for prediction (ensure it matches model input)
            prediction = classification_model(df[['Avg_Home_Prob', 'Avg_Draw_Prob', 'Avg_Away_Prob']])
            # Display the result
            st.write(f"### Model Prediction: {prediction} , Arbitrage Betting is possible for this match.")
    else:
            st.write("Please upload a CSV file with only one row.")
# CSS for custom full-width styles
st.markdown(
    """
    <style>
    .css-1d391kg {
        display: flex;
        justify-content: center;
        padding: 10px 0;
    }
    .css-18e3th9 {
        padding: 0;
    }
    .css-12oz5g7 {
        background-color: #f8f9fa;
        border: none;
    }
    body {
        background-color: #f8f9fa;
    }
    </style>
    """, 
    unsafe_allow_html=True
)