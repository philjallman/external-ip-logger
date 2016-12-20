from ipgetter import ipgetter
import config
import httplib2
import os
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = config.client_secret_file
APPLICATION_NAME = 'Google Sheets External IP Logger'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = config.credential_dir
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'google-sheets-external-ip-logger.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """
    Logs the current external IP to a Google Sheet
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = config.sheet_id
    rangeName = 'LogHeader'
    # result = service.spreadsheets().values().get(
    #    spreadsheetId=spreadsheetId, range=rangeName).execute()
    logs = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range='IP Log!A:B').execute()
    last_ip = logs['values'][-1][1]
    current_ip = ipgetter.myip()
    update_time =  time.strftime('%m/%d/%Y %H:%M:%S')
    if current_ip != last_ip:
        body = {
            'valueInputOption': 'USER_ENTERED',

            'data': [{
                'range': 'IP Log!A' + str(len(logs['values']) + 1),
                'values': [[update_time]]
                      },
                {
                    'range': 'IP Log!B' + str(len(logs['values']) + 1),
                    'values': [[current_ip]]
                },
                {
                    'range': 'IP Log!D1',
                    'values': [[current_ip]]
                }
                ]

        }

        print body

        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheetId,body=body
        ).execute()
    else:
        print 'No IP Change'

if __name__ == '__main__':
    main()