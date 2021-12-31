#Importing neccessary Libraries
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

#Stocks Dataset is used
df = px.data.stocks()
# df.head()

#Mapping stocks to it's corresponding Company
dic={
    'GOOG':'Google',
    'AAPL':'Apple',
    'AMZN':'Amazon',
    'FB':'Facebook',
    'NFLX':'Netflix',
    'MSFT':'Microsoft'
}
# print(dic)

#Function that returns maximum stock price of given company
def max_price(data,company):
    return max(data[company])

#Function that returns minimum stock price of given company
def min_price(data,company):
    return min(data[company])

#Different Stocks Available
# df.columns[1:]

#Function generates and returns a line graph of stock pricing for given company
def fig_company_trend(company):
    data=df
    fig = px.line(data, y=company, x=data.date, title='Monthly trend for {}'.format(dic[company]),height=600,color_discrete_sequence =['maroon'])
    fig.update_layout(title_x=0.5,plot_bgcolor='#F2DFCE',paper_bgcolor='#F2DFCE',xaxis_title="Month",yaxis_title=dic[company])
    return fig

#Bootstrap is used as the External stylesheet
external_stylesheets = [dbc.themes.BOOTSTRAP]

#initialising dash app(dashboard)
dashboard = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Title for our DashBoard
dashboard.title = 'Stock Pricing Dashboard'

#Color scheme for Dashboard
colors = {
    'background': '#111111',
    'bodyColor':'#F2DFCE',
    'text': '#7FDBFF'
}


#Function to set heading style
def get_page_heading_style():
    return {'backgroundColor': colors['background']}
# get_page_heading_style()

#Function to set Title
def get_page_heading_title():
    return html.H1(
        children='Stock Pricing Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    )
# get_page_heading_title()

#Function to set Sub title
def get_page_heading_subtitle():
    return html.Div(
        children='Visualize Stock pricing generated from sources all over the world.',
        style={
            'textAlign':'center',
            'color':colors['text']
        }
    )
# get_page_heading_subtitle()

#Function to generate header
def generate_page_header():
    main_header =  dbc.Row(
        [
            dbc.Col(get_page_heading_title(),md=12)
        ],
        align="center",
        style=get_page_heading_style()
    )
    subtitle_header = dbc.Row(
        [
            dbc.Col(get_page_heading_subtitle(),md=12)
        ],
        align="center",
        style=get_page_heading_style()
    )
    header = (main_header,subtitle_header)
    return header
# generate_page_header()

#Function to create Dropdown menu/list
def create_dropdown_list(company_list):
    dropdown_list = []
    for company in sorted(company_list):
        tmp_dict = {'label':dic[company],'value':company}
        dropdown_list.append(tmp_dict)
    return dropdown_list
# create_dropdown_list(df.columns[1:])

#Function to create Dropdown
def get_company_dropdown(id):
    return html.Div(
        [
            html.Label('Select Company'),
            dcc.Dropdown(
                id='my-id'+str(id),
                options=create_dropdown_list(df.columns[1:]),
                value='GOOG'
            ),
            html.Div(id='my-div'+str(id))
        ]
    )
# get_company_dropdown(1)

#Function to create Graph for Dashboard
def graph1():
    return dcc.Graph(id='graph1',figure=fig_company_trend('GOOG'))
# graph1()

#Function to generate content to be dislayed on cards
def generate_card_content(card_header,card_value):
    card_head_style = {'textAlign':'center','fontSize':'150%'}
    card_body_style = {'textAlign':'center','fontSize':'200%'}
    card_header = dbc.CardHeader(card_header,style=card_head_style)
    card_body = dbc.CardBody(
        [
            html.H5("{:.2f}".format(card_value), className="card-title",style=card_body_style)
        ]
    )
    card = [card_header,card_body]
    return card

#Function to generate cards for Dashboard
def generate_cards(company='GOOG'):
    mx=max_price(df,company)
    mn=min_price(df,company)
    current=df[company].iloc[-1]
    cards = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(generate_card_content("Maximum Price",mx), color="success", inverse=True),md=dict(size=2,offset=3)),
                    dbc.Col(dbc.Card(generate_card_content("Minimum Price",mn), color="warning", inverse=True),md=dict(size=2)),
                    dbc.Col(dbc.Card(generate_card_content("Current Price",current),color="dark", inverse=True),md=dict(size=2)),
                ],
                className="mb-4",
            ),
        ],id='card1'
    )
    return cards

#Function to generate layout for our Dashboard
def generate_layout():
    page_header = generate_page_header()
    layout = dbc.Container(
        [
            page_header[0],
            page_header[1],
            html.Hr(),
            generate_cards(),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(get_company_dropdown(id=1),md=dict(size=4,offset=4))                    
                ]
            
            ),
            dbc.Row(
                [                
                    
                    dbc.Col(graph1(),md=dict(size=6,offset=3))
        
                ],
                align="center",

            ),
        ],
        fluid=True,
        style={'backgroundColor': colors['bodyColor']}
    )
    return layout

#Creating layout for our Dashboard
dashboard.layout = generate_layout()

@dashboard.callback(
    [
        Output(component_id='graph1',component_property='figure'), #line chart
        Output(component_id='card1',component_property='children') #number on the card
    ],
    [
        Input(component_id='my-id1',component_property='value')
    ]
)

#function to update dashboard
def update_output_div(input_value1):
    return fig_company_trend(input_value1),generate_cards(input_value1)

#Running the server on localhost with port number assigned as 8051
dashboard.run_server(host= '127.0.0.1', port=8051)

# http://127.0.0.1:8051/
