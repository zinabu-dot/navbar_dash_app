import dash
import dash_html_components as html
import dash_core_components as dcc

from navbar import Navbar

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

nav = Navbar()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def contact_us():
    layout = html.Div([ nav,
        html.Img(src='https://image.shutterstock.com/image-photo/ethiopian-handmade-habesha-baskets-sold-600w-498019927.jpg'),
        html.Div(dcc.Input(id='input-email', type='email', placeholder="input your {}".format('email'))),
        html.Div(dcc.Input(id='input-on-submit', type='text', placeholder="input your {}".format('message'))),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic',
                children='Enter a value and press submit')
    ])
    return layout

app.layout = contact_us()

@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')],
    [dash.dependencies.State('input-email', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


if __name__ == '__main__':
    app.run_server(debug=True)