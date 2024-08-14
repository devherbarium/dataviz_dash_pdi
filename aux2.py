from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import yaml
from yaml.loader import SafeLoader
from io import BytesIO
from PIL import Image
import pandas as pd


def open_img_from_blob(account_key,blob_name):
    """
    """

    account_name = 'hlbdatalake'
    container_name = 'pdi-dashboard'

    # Conectar ao Blob Service Client
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net",
                                            credential=account_key)

    # Obter o cliente do contêiner
    container_client = blob_service_client.get_container_client(container_name)

    # Obter o cliente do blob
    blob_client = container_client.get_blob_client(blob_name)

    # Baixar o blob como um stream
    blob_data = blob_client.download_blob()
    image_stream = BytesIO(blob_data.readall())

    return image_stream

def img_base_pth():
    """
    Function to retrieve the image and base path for the codes.
    :return:
    """
    # img_path = r"C:\Users\anna.silva\Documents\Entrega_Final_Sprint4\Codigos\0-Dashboard_Final\Imagens"
    img_path = "C:\\Users\\anna.silva\\Documents\\Entrega_Final_Sprint4\\Codigos\\0-Dashboard_Final\\Imagens"
    # base_path = r"C:\Users\anna.silva\Documents\Entrega_Final_Sprint4\Codigos\0-Dashboard_Final\Base_dados"
    base_path ="C:\\Users\\anna.silva\\Documents\\Entrega_Final_Sprint4\\Codigos\\0-Dashboard_Final\\Base_dados"

    return img_path,base_path


def read_yaml_from_blob(container_name, blob_name,storage_account_key):
    """
    Lê um arquivo YAML de um blob no Azure Blob Storage.

    :param container_name: Nome do contêiner no Azure Blob Storage.
    :param blob_name: Nome do blob no Azure Blob Storage.
    :param key_file_path: Caminho para o arquivo de texto contendo a chave de armazenamento. Default é 'storage_key.txt'.
    :return: O conteúdo do arquivo YAML como um dicionário, ou None se houver um erro.
    """


    # Defina o nome da conta de armazenamento
    storage_account_name = "hlbdatalake"

    # Criar a connection string
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

    # Conectar ao BlobServiceClient usando a connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Criar o ContainerClient
    container_client = blob_service_client.get_container_client(container_name)

    # Criar o BlobClient
    blob_client = container_client.get_blob_client(blob_name)

    # Baixar o arquivo YAML do blob e carregar o conteúdo
    try:
        download_stream = blob_client.download_blob()
        yaml_content = download_stream.readall()
        config = yaml.load(yaml_content, Loader=SafeLoader)
        return config
    except Exception as e:
        print(f"Erro ao ler o arquivo YAML do blob: {e}")
        return None


def read_storage_key(key_file_path):
    # Ler a chave de armazenamento do arquivo de texto
    with open(key_file_path, 'r') as file:
        storage_account_key = file.read().strip()

    return storage_account_key


def read_excel_from_blob(connection_string, container_name, blob_name,cols=None):
    """
    Lê um arquivo Excel de um contêiner blob do Azure e retorna um DataFrame do pandas.

    :param connection_string: String de conexão ao Azure Blob Storage.
    :param container_name: Nome do contêiner do blob.
    :param blob_name: Nome do arquivo blob.
    :return: DataFrame do pandas com os dados do arquivo Excel.
    """
    # Conectar ao serviço de blob
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Baixar o blob
    blob_client = container_client.get_blob_client(blob_name)
    stream_downloader = blob_client.download_blob()
    blob_data = stream_downloader.readall()

    # Ler o conteúdo do blob como um DataFrame do pandas
    df = pd.read_excel(BytesIO(blob_data), engine='openpyxl', names=cols)

    return df


def read_csv_from_blob(connection_string, container_name, blob_name):
    """
    Lê um arquivo Excel de um contêiner blob do Azure e retorna um DataFrame do pandas.

    :param connection_string: String de conexão ao Azure Blob Storage.
    :param container_name: Nome do contêiner do blob.
    :param blob_name: Nome do arquivo blob.
    :return: DataFrame do pandas com os dados do arquivo Excel.
    """
    # Conectar ao serviço de blob
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Baixar o blob
    blob_client = container_client.get_blob_client(blob_name)
    stream_downloader = blob_client.download_blob()
    blob_data = stream_downloader.readall()

    # Ler o conteúdo do blob como um DataFrame do pandas
    df = pd.read_csv(BytesIO(blob_data))

    return df
