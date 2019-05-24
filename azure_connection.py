import pandas as pd
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings


def get_token(file_path):
    with open(file_path) as file:
        token = file.read()
    return token


accountkey = get_token("tokens/azure_token.txt")
accountname = "siteparsing"


def download_to_azure(sita_data_csv, accountkey=accountkey,
                      accountname=accountname):

    block_blob_service = BlockBlobService(account_name=accountname, account_key=accountkey)
    block_blob_service.create_container('sitedata')

    block_blob_service.create_blob_from_path(
        'sitedata',
        'sitedata.csv',
        'site_data.csv',
        content_settings=ContentSettings(content_type='application/CSV'))


def get_site_data_azure(accountkey=accountkey, accountname=accountname):

    block_blob_service = BlockBlobService(account_name=accountname, account_key=accountkey)
    block_blob_service.get_blob_to_path('sitedata', 'sitedata.csv', 'out-data.csv')

    site_data = pd.read_csv("out-data.csv")

    return site_data
