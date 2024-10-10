import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load the processed data
df = pd.read_excel("processed_china_crime_data.xlsx")

# Initialize the Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Crime Dashboard"),
    
    # Dropdown to select Crime Type
    dcc.Dropdown(
        id='crime-type-dropdown',
        options=[{'label': crime, 'value': crime} for crime in df['Crime_Type'].unique()],
        value=df['Crime_Type'].unique()[0],  # Default value
        multi=False,
        placeholder="Select Crime Type"
    ),
    
    # Dropdown to select the attribute to visualize on x-axis
    dcc.Dropdown(
        id='x-axis-dropdown',
        options=[
            {'label': 'Date', 'value': 'Date'},
            {'label': 'Victim Age', 'value': 'Victim_Age'},
            {'label': 'Suspect Age', 'value': 'Suspect_Age'},
            {'label': 'Weapon Used', 'value': 'Weapon_Used'},
            {'label': 'Month', 'value': 'Month'}  # If you extracted Month earlier
        ],
        value='Date',  # Default value
        multi=False,
        placeholder="Select x-axis attribute"
    ),
    
    # Graph to display the results
    dcc.Graph(id='crime-graph')
])

# Callback to update the graph based on selected crime type and x-axis attribute
@app.callback(
    Output('crime-graph', 'figure'),
    [Input('crime-type-dropdown', 'value'),
     Input('x-axis-dropdown', 'value')]
)
def update_graph(selected_crime, selected_x):
    filtered_data = df[df['Crime_Type'] == selected_crime]
    
    # Plotting based on selected x-axis attribute
    if selected_x == 'Date':
        fig = px.histogram(filtered_data, x='Date', title=f'Crimes over Time for {selected_crime}', nbins=30)
    else:
        fig = px.histogram(filtered_data, x=selected_x, title=f'Distribution of {selected_x} for {selected_crime}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
