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

    # Create the gauge chart
    # Function to create a soccer-themed gauge chart for total probability
def create_gauge_chart(total_prob, title="Total Implied Probability"):
    # Ensure the total probability is within 0-120 range (since you used 120 in the range)
    if total_prob > 120:
        total_prob = 120
    elif total_prob < 0:
        total_prob = 0
    
#     # Create the gauge chart with soccer theme
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=total_prob,
        delta={'reference': 100, 'increasing': {'color': "Green"}},
        gauge={
            'axis': {'range': [0, 120], 'tickwidth': 2, 'tickcolor': "black"},
            'bar': {'color': "Blue"},  # You can change the bar color to represent goals
            'steps': [
                {'range': [0, 40], 'color': 'Green'},  # Representing the soccer field (low value range)
                {'range': [40, 80], 'color': 'yellow'},     # Mid-range values, depicting midfield action
                {'range': [80, 120], 'color': 'Red'}        # High value, depicting the goal zone
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': total_prob
            }
        },
        title={'text': title, 'font': {'size': 24, 'color': 'darkgreen', 'family': "Arial Black"}},
        number={'suffix': "%", 'font': {'size': 36}}
    ))


#     # Update layout to include a soccer field green background and make it eye-catching
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",  # Making the background transparent
        plot_bgcolor="lightgreen",  # Light green to resemble a soccer field
        margin=dict(t=100, b=50, l=50, r=50),  # Add some margin for better visuals
    )

    return fig

# Function to create a radar chart to visualize probabilities
def create_radar_chart(home_prob, draw_prob, away_prob, title="Probability Radar Chart"):
    categories = ['Home Win', 'Draw', 'Away Win']
    values = [home_prob, draw_prob, away_prob]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Probabilities',
        line=dict(color='Green')
    ))

    fig.update_layout(
        title={'text': title, 'font': {'size': 24, 'color': 'darkgreen', 'family': "Arial Black"}},
        polar=dict(
            bgcolor='red',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[20, 40, 60, 80, 100],
                tickangle=45,
                tickfont=dict(size=12)
            ),
            angularaxis=dict(
                tickfont=dict(size=14)
            )
        ),
        showlegend=False,
        margin=dict(t=100, b=50, l=50, r=50),
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig

st.markdown("<h1 style='text-align: center; font-family: Copperplate Gothic, sans-serif; color: GREEN;'>Arbitrage Betting Detector</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .full-width-image {
        width: 100%;
        height: auto;
        max-height: 400px; /* Adjust the max height as per your requirement */
        object-fit: cover;  /* Ensures the aspect ratio is maintained */
    }
    </style>
    <img src="https://cdn.wallpapersafari.com/51/18/lzn2Zf.jpg" class="full-width-image">
    """,
    unsafe_allow_html=True
)

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
        col1, col2 = st.columns(2)
        with col1:
        # Create and display gauge chart for Total Implied Probability
            st.plotly_chart(create_gauge_chart(row['Total Implied Probability (%)'], "Total Implied Probability Gauge"))
        with col2:
            st.plotly_chart(create_radar_chart(row['Home Win Implied Probability (%)'], row['Draw Implied Probability (%)'], row['Away Win Implied Probability (%)'], "Probability Radar Chart"))
        # Separator for each row
        st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

if st.button("Submit"):
    if len(df) == 1:  # Ensure it's a single-row CSV
        st.write("Running the model...")
        # Prepare data for prediction (ensure it matches model input)
        prediction = model.predict(df[['Avg_Home_Prob', 'Avg_Draw_Prob', 'Avg_Away_Prob']])[0]

          # Display the result and thumbs up or down image using markdown with inline HTML
        if prediction == 1:
            st.markdown(
                """
                <div style="text-align: center;">
                    <h3 style="margin-right: 15px;">YES, Arbitrage Betting is possible.</h3>
                    <img src="https://media.istockphoto.com/id/962056670/photo/soccer-ball-character-with-thumbs-up-gesture.jpg?s=612x612&w=0&k=20&c=fWSlhJnqj3rkkfdBE13MIr0-sPN2hLkxGhI7R_mCb-I=" width="500">
                </div>
                """,
                unsafe_allow_html=True
            )
        elif prediction == 0:
            st.markdown(
                """
                <div style="text-align: center;">
                    <h3 style="margin-right: 15px;">NO, Arbitrage Betting is not possible.</h3>
                    <img src="https://thumbs.dreamstime.com/z/soccer-ball-character-thumbs-down-gesture-soccer-ball-character-thumbs-down-gesture-isolated-white-background-d-123887600.jpg" width="500">
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("Please upload a CSV file with only one row.")
    
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
