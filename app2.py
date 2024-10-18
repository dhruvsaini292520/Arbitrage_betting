import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go

# Apply full-page width
st.set_page_config(layout="wide")

# Authentication users
users = {
    "admin": "password",
    "user1": "password1",
    "user2": "password2"
}

# Check if the user is logged in by checking session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# If the user is not logged in, show the login form
if not st.session_state.logged_in:
    # Display App Title
    st.markdown("<h1 style='text-align: center; font-family: Copperplate Gothic, sans-serif; color: GOLD; font-size: 60px;'>ARBITECTIVE</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-family: Copperplate Gothic, sans-serif; color: SILVER;'>Arbitrage Betting Detector</h1>", unsafe_allow_html=True)

    # Image at the top
    st.markdown(
        """
        <style>
        .full-width-image {
            width: 100%;
            height: auto;
            max-height: 400px;
            object-fit: cover;
        }
        </style>
        <img src="https://cdn.wallpapersafari.com/51/18/lzn2Zf.jpg" class="full-width-image">
        """,
        unsafe_allow_html=True
    )
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Add a "Sign In" button
    if st.button("Sign In"):
        # Check if the username and password are correct
        if username in users and password == users[username]:
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Username or Password is incorrect. Please try again!")
else:
    # Load pre-trained machine learning model (RandomForest)
    with open('arbitrage_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    # Function to make predictions using the loaded model
    def classification_model(data):
        prediction = model.predict(data)
        return "YES" if prediction == 1 else "NO"

    # Function to create a soccer-themed gauge chart
    def create_gauge_chart(total_prob, title="Total Implied Probability"):
        if total_prob > 120:
            total_prob = 120
        elif total_prob < 0:
            total_prob = 0

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=total_prob,
            delta={'reference': 100, 'increasing': {'color': "Green"}},
            gauge={
                'axis': {'range': [80, 120], 'tickwidth': 2, 'tickcolor': "black"},
                'bar': {'color': "Blue", 'thickness': 0.4},
                'steps': [
                    {'range': [80, 99.5], 'color': 'Red'},
                    {'range': [99.5, 100.5], 'color': 'yellow'},
                    {'range': [100.5, 120], 'color': 'Green'}
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

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="lightgreen",
            margin=dict(t=100, b=50, l=50, r=50),
        )

        return fig

    # Function to create a radar chart
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

    # Display App Title
    st.markdown("<h1 style='text-align: center; font-family: Copperplate Gothic, sans-serif; color: GOLD; font-size: 60px;'>ARBITECTIVE</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-family: Copperplate Gothic, sans-serif; color: SILVER;'>Arbitrage Betting Detector</h1>", unsafe_allow_html=True)

    # Image at the top
    st.markdown(
        """
        <style>
        .full-width-image {
            width: 100%;
            height: auto;
            max-height: 400px;
            object-fit: cover;
        }
        </style>
        <img src="https://cdn.wallpapersafari.com/51/18/lzn2Zf.jpg" class="full-width-image">
        """,
        unsafe_allow_html=True
    )

    # Full-page layout using columns and CSS
    col1, col2 = st.columns([1, 5])

    # Load sample data from a CSV file
    sample_file_path = 'new_variation_row_5.csv'  # Replace with your sample file path
    df = pd.read_csv(sample_file_path)

    # File uploader to upload CSV with a single row of data
    uploaded_file = st.file_uploader("Load Single Game Data (1 Row CSV File)", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

    # Calculate probabilities and other data
    df['Avg_Home_Prob'] = 1 / df.filter(like='Home_Odds_').mean(axis=1)
    df['Avg_Draw_Prob'] = 1 / df.filter(like='Draw_Odds_').mean(axis=1)
    df['Avg_Away_Prob'] = 1 / df.filter(like='Away_Odds_').mean(axis=1)
    df['Total_Prob'] = df['Avg_Home_Prob'] + df['Avg_Draw_Prob'] + df['Avg_Away_Prob']

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
            # Styling for Home Team in green
            st.markdown(f"<div class='hometeam-title' style='color: green;'>Home Team: {row['Home Team']}</div>", unsafe_allow_html=True)
            
            # Styling for Away Team in blue
            st.markdown(f"<div class='awayteam-title' style='color: blue;'>Away Team: {row['Away Team']}</div>", unsafe_allow_html=True)
            
            # Styling for probabilities (percentages) in red
            st.markdown(f"<div class='probability'>Home Win Implied Probability: <span class='highlight' style='color: red;text-align: left'>{row['Home Win Implied Probability (%)']:.2f}%</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='probability'>Draw Implied Probability: <span class='highlight' style='color: red;text-align: center'>{row['Draw Implied Probability (%)']:.2f}%</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='probability'>Away Win Implied Probability: <span class='highlight' style='color: red;text-align: right'>{row['Away Win Implied Probability (%)']:.2f}%</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='probability'>Total Implied Probability: <span class='highlight' style='color: red;text-align: center'>{row['Total Implied Probability (%)']:.2f}%</span></div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
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
                        <img src="https://media.istockphoto.com/id/962056670/photo/soccer-ball-character-with-thumbs-up-gesture.jpg" width="500">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif prediction == 0:
                st.markdown(
                    """
                    <div style="text-align: center;">
                        <h3 style="margin-right: 15px;">NO, Arbitrage Betting is not possible.</h3>
                        <img src="https://thumbs.dreamstime.com/z/soccer-ball-character-thumbs-down-gesture-soccer-ball-character-thumbs-down-gesture-isolated-white-background-d-123887600.jpg"
                        style="width: 500px; height: auto; object-fit: cover; object-position: top; clip-path: inset(0% 0% 15% 0%);">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.write("Please upload a CSV file with only one row.")
