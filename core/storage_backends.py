from storages.backends.azure_storage import AzureStorage
import os


class StaticAzureStorage(AzureStorage):
    """
    Custom Azure Storage backend for static files
    """
    account_name = os.getenv('AZURE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_ACCOUNT_KEY')
    azure_container = os.getenv('AZURE_CONTAINER', 'static')
    expiration_secs = None
    azure_ssl = True
    azure_auto_sign = True
    azure_access_policy_expiry = 3600  # 1 hour
    azure_access_policy_permission = 'r'


class MediaAzureStorage(AzureStorage):
    """
    Custom Azure Storage backend for media files
    """
    account_name = os.getenv('AZURE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_ACCOUNT_KEY')
    azure_container = os.getenv('AZURE_MEDIA_CONTAINER', 'media')
    expiration_secs = None
    azure_ssl = True
    azure_auto_sign = True
    azure_access_policy_expiry = 3600  # 1 hour
    azure_access_policy_permission = 'r'
