from time import sleep

import pandas as pd
import plotly.express as px
from opcua import Client

from consts import YOUR_IP, CONN_PORT, URL, SERVER_NAME

def connect_client():
    """
    CONNECT THE CLIENT TO THE URL SERVER
    """
    client=Client(URL)
    client.connect()

    return client

def get_node_of_values(client):
    """
    CORRELATE TO THE NODE VALUES OF THOSE ELEMENTS IN THE SERVER SIDE
    """
    temperature_data = client.get_node("ns=2;i=2")
    humidity_data = client.get_node("ns=2;i=3")
    time = client.get_node("ns=2;i=4")

    return temperature_data, humidity_data, time

def main():
    """
    MOCK PROJECT APP WILL RECEIVE 15 VALUES FROM THE SERVER SIDE AND PLOT A PLOTLY GRAPH WITH IT
    """

    client = connect_client()
    temperature_data, humidity_data, time = get_node_of_values(client)

    data = []
    iterations = 0

    while iterations < 15:
        _temperature_data = temperature_data.get_value()
        _humidity_data = humidity_data.get_value()
        _time = time.get_value()

        sleep(2)
        data.append(dict(
                    Time=_time.strftime("%Y-%m-%d %H:%M:%S"), Variavel='Temperatura', Valor=_temperature_data))
        data.append(dict(
                    Time=_time.strftime("%Y-%m-%d %H:%M:%S"), Variavel='Umidade', Valor=_humidity_data))
        iterations += 1
    
    df = pd.DataFrame(data)

    fig = px.line(df, x="Time", y="Valor", color="Variavel", title="layout.hovermode='x'")
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x")

    fig.write_html(f"Correlation_Temperature_Humidity.html")

if __name__ == "__main__":
    main()
