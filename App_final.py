import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

avg_temp = pd.read_csv('..\weather_dash\merged_temp_data.csv')
avg_temp

# Working code for 1 country selection
# Create a DataTable
d_table = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in avg_temp.columns],
    data=avg_temp.to_dict('records'),
    style_data={'color': 'white', 'backgroundColor': 'black'},
    style_header={'backgroundColor': 'rgb(210, 210, 210)', 'color': 'black', 'fontWeight': 'bold'}
)

# Create figures for demonstration
color_continuous_scale = px.colors.sequential.Plasma

fig_1 = px.choropleth(
    data_frame=avg_temp,
    locations="alpha-3",
    color="avg_temp_month",
    locationmode='ISO-3',
    color_continuous_scale=px.colors.sequential.Jet,
    hover_name="country",
    animation_frame="month",
    projection='natural earth',
    title='Yearly Average Temperature Variations in 8 Major Cities'
)

fig_1 = fig_1.update_layout(
    plot_bgcolor="#222222", paper_bgcolor="#222222", geo_bgcolor="#222222", font_color="White", width=1050, height=600,
    coloraxis_colorbar=dict(title='Average Temperature (°C)'),
    coloraxis=dict(cmin=avg_temp['avg_temp_month'].min(), cmax=avg_temp['avg_temp_month'].max()),
)

graph1 = dcc.Graph(id='graph1', figure=fig_1, style={'border': '3px solid #636EFA'})

fig_2 = px.line(
    avg_temp, x='month', y='avg_temp_month', height=300,
    title='Monthly average temperature overview', markers=True
)

fig_2 = fig_2.update_layout(plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="White")

graph2 = dcc.Graph(id='graph2', figure=fig_2, style={'backgroundColor': 'black', 'border': '3px solid #636EFA'})

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])
server = app.server
# Create dropdown options from unique cities in the DataFrame
dropdown_options_cities = [{'label': city, 'value': city} for city in avg_temp['city'].unique()]

app.layout = html.Div([
    html.H1('Yearly Weather Patterns in 8 Major Cities', style={'textAlign': 'center', 'color': '#636EFA'}),

    html.Div(html.P("Overview of Weather fluctuations using Weather API Data"),
             style={'marginLeft': 50, 'marginRight': 25}),

    html.Div([
        dcc.Dropdown(
            id='city-dropdown',
            options=dropdown_options_cities,
            value=dropdown_options_cities[0]['value'],
            multi=False,
            style={'width': '50%', 'marginLeft': 'auto', 'marginRight': 'auto'}
        ),

        html.Div(id='selected-city-info'),
        d_table,
        graph1,
        graph2
    ])
])

# Define callback functions to update the table and graphs based on dropdown selection
@app.callback(
    Output('selected-city-info', 'children'),
    Output('table', 'data'),
    Output('table', 'columns'),
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Input('city-dropdown', 'value')
)
def update_data(selected_city):
    # Filter the DataFrame based on the selected city
    filtered_data = avg_temp[avg_temp['city'] == selected_city]

    # Display selected city information
    info_text = f'Selected City: {selected_city}'

    # Display filtered table
    table_data = filtered_data.to_dict('records')
    table_columns = [{"name": i, "id": i} for i in filtered_data.columns]

    # Display filtered graphs
    fig_1 = px.choropleth(
        data_frame=filtered_data,
        locations="alpha-3",
        color="avg_temp_month",
        locationmode='ISO-3',
        color_continuous_scale=px.colors.sequential.Jet,
        hover_name="country",
        animation_frame="month",
        projection='natural earth',
        title=f'Yearly Average Temperature Variations in {selected_city}'
    )

    fig_1 = fig_1.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", geo_bgcolor="#222222", font_color="White", width=1050, height=600,
        coloraxis_colorbar=dict(title='Average Temperature (°C)'),
        coloraxis=dict(cmin=filtered_data['avg_temp_month'].min(), cmax=filtered_data['avg_temp_month'].max()),
    )

    graph1 = dcc.Graph(id='graph1', figure=fig_1, style={'border': '3px solid #636EFA'})

    fig_2 = px.line(
        filtered_data, x='month', y='avg_temp_month', height=300,
        title=f'{selected_city} monthly average temperature overview', markers=True
    )

    fig_2 = fig_2.update_layout(plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="White")

    graph2 = dcc.Graph(id='graph2', figure=fig_2, style={'backgroundColor': 'black', 'border': '3px solid #636EFA'})

    return info_text, table_data, table_columns, fig_1, fig_2

if __name__ == '__main__':
    app.run_server(port=8089)



