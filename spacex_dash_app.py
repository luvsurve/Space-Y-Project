# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
print(spacex_df.columns)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',  options=[{'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                value='ALL',
                                placeholder='Launch Sites'
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, value=[0, 10000],marks={0: '0',2500: '2,500',5000:'5,000',7500:'7,500',10000:'10,000'}),
                                                                                                         
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    data = spacex_df.groupby('Launch Site').sum()/spacex_df['Flight Number'].sum()*100
    if entered_site=='ALL':
        fig = px.pie(data, names=data.index,values='Flight Number')
    else:
        temp = data.reset_index().copy(deep=False)
        temp.loc[:,'Launch Site'][temp['Launch Site']!=entered_site] = 'Others'
        data = temp.groupby('Launch Site').sum()/spacex_df['Flight Number'].sum()*100
        fig = px.pie(data, names=data.index, values='Flight Number')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site,payload_values):
    min_payload = payload_values[0]
    max_payload = payload_values[1]
    #print(min_payload,max_payload)
    data = spacex_df[(spacex_df['Payload Mass (kg)']>=min_payload) & (spacex_df['Payload Mass (kg)']<max_payload)]
    if entered_site=='ALL':
        scat_fig = px.scatter(data,x='Payload Mass (kg)',y='class',color="Booster Version Category")
    else:
        plot = data[data['Launch Site']==entered_site]
        scat_fig = px.scatter(plot,x='Payload Mass (kg)',y='class',color="Booster Version Category")
    return scat_fig
# Run the app
if __name__ == '__main__':
    app.run_server(port=3000)