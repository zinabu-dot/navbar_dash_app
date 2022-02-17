## Ethiopian Coronavirus cases reporting dashborad

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime,date

USERNAME_PASSWORD_PAIRS = [
    ['', ''],['', '']  # changes as desired (inplace of 'JamesBond' put user name, and inplace of '0.007' password)
]

app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server  # this should be added


# create data
np.random.seed(42)
random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,100)

# Retriving Dataset
df_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
df_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
df_recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

etc=df_confirmed[df_confirmed['Country/Region']=='Ethiopia']
Confirmed = etc.iloc[:,-1].tolist()

etd=df_deaths[df_deaths['Country/Region']=='Ethiopia']
Death = etd.iloc[:,-1].tolist()

etr=df_recovered[df_recovered['Country/Region']=='Ethiopia']
Recovered = etr.iloc[:,-1].tolist()

nem=['Confirmed','Death','Recovered']
df=pd.DataFrame([Confirmed,Death,Recovered], index=nem)

df.reset_index(level=0, inplace=True)

df.columns=['Case','Freq']

#plt.bar(df['Case'],df['Freq'])
case_nums_eth = df_confirmed[df_confirmed['Country/Region']=='Ethiopia'] #.sum().drop(['Lat','Long'],axis =1).apply(lambda x: x[x > 0].count(), axis =0)
cne=case_nums_eth.iloc[:,4:].transpose()
cne = cne.rename(columns={104:'cases'})

d = [datetime.strptime(date,'%m/%d/%y').strftime("%d %b") for date in cne.index]
num=cne['cases'].tolist()


dfg = df.transpose()
dfg.columns= dfg.iloc[0]
g = dfg.drop(dfg.index[0])
g.insert(3,'lat',etd['Lat'].tolist())
g.insert(4,'long',etd['Long'].tolist())

fig = px.scatter_mapbox(g, lat='lat', lon='long', hover_name=etd['Country/Region'], hover_data=["Confirmed",'Death', "Recovered"],
                        color_discrete_sequence=["red"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})




app.layout = html.Div([html.H1('Reporting Dash: Daily Coronavirus Cases in Ethiopia', style={'backgroundColor':'purple'}),
                        html.H3('by Zinabu T.'),
                     html.H3('Summary Table'),
                       dash_table.DataTable(
                                 id='table',
                                  columns=[{"name": i, "id": i} for i in df.columns],
                                    data=df.to_dict('records')),

                     dcc.Graph(id='Bar Plot',
                     figure = {'data':[
                             go.Bar(
                             x=df['Case'],
                             y=df['Freq'],
                             #mode='markers'
                             )
                     ],
                     'layout':go.Layout(title=' Bar Plot of Number of Confirmed, Death and Recovered Cases')}
                     ),


                  dcc.Graph(figure=fig
                           ),


                     dcc.Graph(id='Scatter Plot',
                                figure = {'data':[
                                    go.Scatter(
                                    x=d, y=num,
                                        mode='lines+markers',
                             marker = {
                             'size':5, 'line':'-',
                             'color': 'rgb(51,204,153)',
                             'symbol':'pentagon',
                             'line': {'width':4}
                             }
                                    )],
                            'layout':go.Layout(title=' Commulative Number of Confirmed Cases per Day',
                                              xaxis={'title':'Date'},yaxis={'title':'Number of Cases in Ethiopia'})})
        ])


if __name__ == '__main__':
     app.run_server()
