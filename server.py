"""
SERVIDOR OPC-UA E MOCK DE ENVIO DE DADOS (TEMPERATURA, UMIDADE E TEMPO) PARA O MESMO
PROJETO DE DISCIPLINA DE SISTEMAS DISTRIBUÍDOS DO IFSC/CAMPUS FLORIANÓPOLIS - ENGENHARIA MECATRÔNICA - 2020/2
OPC-UA SERVER
AUTHORS: PAULO VINICIUS MASNIK & PABLO MEDEIROS PENNA
"""

from datetime import datetime
from random import randint
from time import sleep
from opcua import Server

from consts import CONN_PORT, SERVER_NAME, URL, YOUR_IP


def generate_server():
    """
    GERANDO SERVIDOR - NOME, URL E IP
    """
    server = Server()
    server.set_endpoint(URL)
    addspace = server.register_namespace(SERVER_NAME)

    return server, addspace

def generate_server_params(server, addspace):
    """
    GERA AS VARIAVEIS DE PARAMETRO PARA O SERVIDOR RECEBÊ-LAS
    """

    #Buscando as variáveis OBJECT do servidor
    node = server.get_objects_node()
    #Adicionando objeto parametros que irá conter as variáveis de informações
    Param = node.add_object(addspace, "Parameters")


    temperature_data = Param.add_variable(addspace, "Temperature", 0)
    humidity_data = Param.add_variable(addspace, "Humidity", 0)
    time = Param.add_variable(addspace, "Time", datetime.now())

    for variable in [temperature_data, humidity_data, time]:
        variable.set_writable()
    
    return temperature_data, humidity_data, time
    

def run_server(server):
    """
    GENERATE THE SERVER ON THE DESIRED URL
    """
    server.start()
    print(f"Server started at {URL}")

def mock_data_to_server(temperature_data, humidity_data, time):
    """
    MOCK DE DADOS ALEATÓRIOS PARA O SERVIDOR
    """

    while True:
        temperature_data.set_value(randint(10, 35))
        humidity_data.set_value(randint(30, 80))
        time.set_value(datetime.now())

        print(f'SENT')
        sleep(2)

def main():
    """
    MAIN CODE
    """
    server, addspace = generate_server()
    temperature_data, humidity_data, time = generate_server_params(server, addspace)
    run_server(server)
    mock_data_to_server(temperature_data, humidity_data, time)


if __name__ == "__main__":
    main()
