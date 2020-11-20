$Env:DJANGO_DEBUG          = 'True'
$Env:DJANGO_ALLOWED_HOST   = 'localhost'
$Env:B2C_TENANT_NAME    = 'findexdatascience'
$Env:B2C_POLICY_NAME    = 'B2C_1_signup_findex_datascience'
$Env:B2C_APP_ID         = '763e9334-9fdc-489b-824d-f58bedaa22f2'
$Env:B2C_REPLY_URL      = 'http://localhost:8080'

$Env:PBI_AUTHENTICATION_MODE = 'ServicePrincipal'
$Env:PBI_CLIENT_ID = '85fc0dc8-72f7-41a7-b55b-5c8a34439b5d'
$Env:PBI_CLIENT_SECRET = '3-Rmv~.m5_lRZv.qG8q0xWf~BatevfF0-6'
$Env:PBI_AUTHORITY_URL = 'https://login.microsoftonline.com/'
$Env:PBI_MASTER_USER = ''
$Env:PBI_MASTER_PASS = ''
$Env:PBI_TENANT_ID = 'b48a9eab-75aa-4a5b-9fd7-f39223245c1a'
$Env:PBI_SCOPE = 'https://analysis.windows.net/powerbi/api/.default'

$Env:DEFAULT_DBENGINE="sql_server.pyodbc"
$Env:DEFAULT_DBHOST = "sql01-datascience-dev-sqldb.database.windows.net"
$Env:DEFAULT_DBUSER = "DSAccessWrite"
$Env:DEFAULT_DBNAME = "access_level"
$Env:DEFAULT_DBPASS = "D6QRh%gdJX3Zd4&r!kVx"
$Env:DEFAULT_DBPORT = "1433"
$Env:DEFAULT_DRIVER = "SQL Server Native Client 11.0"

$Env:EXTERNAL_DBENGINE="sql_server.pyodbc"
$Env:EXTERNAL_DBHOST = "sql01-datascience-dev-sqldb.database.windows.net"
$Env:EXTERNAL_DBUSER = "DSPublicRead"
$Env:EXTERNAL_DBNAME = "public_data"
$Env:EXTERNAL_DBPASS = "RKmWLCwrBi&W*aLIt*uK"
$Env:EXTERNAL_DBPORT = "1433"
$Env:EXTERNAL_DRIVER = "SQL Server Native Client 11.0"

$Env:STUDENT_DBENGINE="sql_server.pyodbc"
$Env:STUDENT_DBHOST = "sql01-datascience-dev-sqldb.database.windows.net"
$Env:STUDENT_DBUSER = "DSStudentRead"
$Env:STUDENT_DBNAME = "student_profile"
$Env:STUDENT_DBPASS = "ZSnLG0FV%iUoW0k3O7hY"
$Env:STUDENT_DBPORT = "1433"
$Env:STUDENT_DRIVER = "SQL Server Native Client 11.0"

$Env:DOWNLOAD_ENVIRONMENT       = "local"
$Env:DOWNLOAD_STORAGE_ACCOUNT   = "batchdatasciencedev"
$Env:DOWNLOAD_STORAGE_KEY       = "G6VcEwo2mFVPhBNIE0domk6Kwm5KyTW496t+dTLawwZYHVrflvegNI3TFL9u14OpBVUkJ6TBAf7yWMEW+KMC/g=="
$Env:DOWNLOAD_LOG_TABLE         = "batchtaskslogsdev"
$Env:INVITE_USERMAIL_TABLE      = "usermailtabledev"

$Env:SECRET_KEY  = "^sj6_uyj%3#hzh*vc09+es=jb(^$%)*wh)qq=32#-$kgg_*v$u"

$Env:B2C_TENANT_ID = '9ce05797-b466-4be5-a471-81aefe74e431'

$Env:AZURE_ACCOUNT_NAME = 'devportalaps'
$Env:AZURE_ACCOUNT_KEY = 'Z2kB3mV+aIz+6F5pghdaOUxWaToxkFkSqn92119SRJl8xwUp2xq+iJYGE1hBpVsKwMAGa7R+bUR0ymqKoavvfw=='
$Env:AZURE_CUSTOM_DOMAIN = 'devportalaps.blob.core.windows.net'
$Env:AZURE_LOCATION = '$web'
$Env:AZURE_CONTAINER = '$web'
