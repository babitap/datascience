

from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    location = '$web'
    file_overwrite = False

# class AzureMediaStorage(AzureStorage):
#     account_name = 'devportalaps' # Must be replaced by your <storage_account_name>
#     account_key = 'Z2kB3mV+aIz+6F5pghdaOUxWaToxkFkSqn92119SRJl8xwUp2xq+iJYGE1hBpVsKwMAGa7R+bUR0ymqKoavvfw==' # Must be replaced by your <storage_account_key>
#     azure_container = '$web'
#     expiration_secs = None

# class AzureStaticStorage(AzureStorage):
#     account_name = 'devportalaps' # Must be replaced by your <storage_account_name>
#     account_key = 'Z2kB3mV+aIz+6F5pghdaOUxWaToxkFkSqn92119SRJl8xwUp2xq+iJYGE1hBpVsKwMAGa7R+bUR0ymqKoavvfw==' # Must be replaced by your <storage_account_key>
#     azure_container = '$web'
#     expiration_secs = None