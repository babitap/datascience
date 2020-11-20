import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from django.conf import settings
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import pytz
import datetime
from access_control.models import *
import re

def send_invite(email):
    # This function will write an entry to userMailTable with all the necessary information regarding the invitation
    #  and next the logic app will detect the new entry in userMailTable and send out the mail accordingly

    # 0, setup the environment
    table_storage_client = TableService(
        account_name=settings.STORAGE_ACCOUNT,
        account_key=settings.STORAGE_KEY )

    my_timezone = pytz.timezone('Australia/Melbourne')
    current_datetime = datetime.datetime.now( tz = my_timezone )
    current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # 1, write the entry to the userMailTable
    mail_entry = {
        'PartitionKey'  : 'USER_INVITATION',
        'RowKey'        : current_datetime_str,
        'Environment'   : settings.ENVIRONMENT,
        'To'            : email, 
        'SignUpURL'     : settings.RETURN_URL,
        'Status'        : 'Pending'
    }

    table_storage_client.insert_entity( settings.USERMAIL_TABLE, mail_entry)

    """
    #Structure email
    msg=MIMEMultipart()
    msg['From'] = 'temptest20200501@gmail.com'
    msg['To'] = email
    msg['Subject'] = 'Welcome to the Findex Data Science Portal'

    #Create body text
    body = '''
    You have been invited to join the Findex Data Science portal.\n
    Please use the following link to register for an acoount by clicking "Sign In" button.
    '''

    #url = '''
    #\n\nhttps://findexdatascience.b2clogin.com/findexdatascience.onmicrosoft.com/oauth2/v2.0/authorize?p=B2C_1_signup_findex_datascience&client_id=14fe7f8c-1918-45a2-b63e-b09cbfa4136c&nonce=defaultNonce&redirect_uri={returnURL}&scope=openid%20https%3A%2F%2Ffindexdatascience.onmicrosoft.com%2Fapi%2Fuser_impersonation&response_type=id_token%20token&prompt=login
    #'''.format(returnURL=settings.RETURN_URL)
    
    
    url = f'{settings.RETURN_URL} \n'
    
    #Url
    body += url
    #Email
    body += '''
    You must sign up with this email address to properly access the portal:
    '''
    body += email
    msg.attach(MIMEText(body))
    
    #Send email
    try:
    	#Set up server
    	server = smtplib.SMTP("smtp.gmail.com", 587)
    	server.starttls()
    	server.login('temptest20200501@gmail.com', 'googleisthebest')

    	#Send mail
    	server.sendmail(msg['From'], msg['To'], msg.as_string())
    	print ('Email sent!')
    except Exception as e:  
        print ('Something went wrong...')
        print (str(e))
    finally:
    	server.quit()
    """
    	
def checkRequiredParams(params,req):
    """
    Returns true if required parameter is mising
    """
    for r in req:
        if r not in params:
            return True
    return False


def concatName(user_id):

    given_name = User.objects.get(id=user_id).given_name 
    family_name = User.objects.get(id=user_id).family_name
    label = ''
    label += given_name if given_name is not None else ''
    label += ' ' if given_name is not None else ''
    label += family_name if family_name is not None else ''

    return label


def userFullName(given_name=None, family_name=None):

    if given_name is None and family_name is None:
        return ''
    elif given_name is not None and family_name is not None:
        return f'{given_name} {family_name}'
    else:
        if given_name is not None:
            return given_name
        else:
            return family_name

def getUserByEmail(email):

    user = None

    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        pass

    return user

def checkEmailString(emailString):
    #regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  #this regex does not allow @westpac.co.nz
    regex = '[^@]+@[^@]+\.[^@]+'
    
    if(re.search(regex,emailString)):  
        if( all(x.isalpha() or x.isdigit() or ( x in ('_', '-', '@', '.') ) for x in emailString ) ):
            print( emailString + " is Valid Email")  
            return True
        else: 
            return False 
    else:  
        print(emailString + " is Invalid Email")    
        return False  

def checkStringHasOnlyAlphaAndSpace(input_string):
    if all(x.isalpha() or x.isspace() for x in input_string):
        return True 
    else:
        return False

def checkStringHasOnlyAlphaNumberDashAndSpace(input_string):
    if all(x.isalpha() or x.isdigit() or x.isspace() or ( x in ('_', '-') ) for x in input_string):
        return True 
    else:
        return False        