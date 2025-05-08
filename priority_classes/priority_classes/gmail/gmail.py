import os
import re
import json
import logging
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from priority_classes.decorators.decorators import time_out
from datetime import datetime
import base64

class Gmail:

    def __init__(self):
        # Initialize the Drive v3 API
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.service = self._service_account_login()


    @time_out()
    def _service_account_login(self):
        """Get a service that communicates to a Google API."""
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('gmail.json', self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)
        return service

    def read_gmail_messages(self,query="has:attachment"):
        # Call the Gmail API
        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            logging.info(msg['snippet'])

    def search_messages(self, query):
        # Pesquisar e-mails com base na consulta (query)
        result = self.service.users().messages().list(userId='me', q=query).execute()
        messages = [ ]
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        return messages

    def get_message(self, msg_id):
        # Obter detalhes do e-mail
        message = self.service.users().messages().get(userId='me', id=msg_id).execute()
        return message

    def download_attachment(self, msg_id, attachment_id, filename):
        # Baixar o anexo
        attachment = self.service.users().messages().attachments().get(
            userId='me', messageId=msg_id, id=attachment_id).execute()
        
        file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
        
        with open(filename, 'wb') as f:
            f.write(file_data)
        logging.info(f'Arquivo {filename} baixado com sucesso.')

    def find_and_download_attachment(self, filename):
        # Pesquisa por e-mails com anexos
        query = f'has:attachment filename:{filename}'
        messages = self.search_messages(query)
        
        if not messages:
            logging.info(f'Nenhum e-mail encontrado com o anexo: {filename}')
            return
        
        for msg in messages:
            msg_id = msg['id']
            message = self.get_message(msg_id)
            
            for part in message['payload']['parts']:
                if part['filename'] and part['filename'] == filename:
                    attachment_id = part['body']['attachmentId']
                    self.download_attachment(msg_id, attachment_id, filename)
                    return


    def download_all_attachments(self,query="has:attachment",filter_partial_filenames=None,path_to_salve:str='attachments'):
        #query = "has:attachment after:2023/01/01"
        results = self.service.users().messages().list(userId='me', q=query).execute()
        logging.info(results)
        conter = 0
        while results.get('messages'):
            logging.info(conter)
            messages = results.get('messages', [])
            logging.info(messages)
            os.makedirs(path_to_salve, exist_ok=True)
            for i, message in enumerate(messages):
                try:
                    msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
                    for k, part in enumerate(msg['payload']['parts']):
                        logging.info('#'*20,f'I:{i} - K:{k}','#'*20)
                        try:
                            if part['filename'] \
                                    and '.' in part['filename'] \
                                    and filter_partial_filenames is not None \
                                    and any([partial_ for partial_ in filter_partial_filenames
                                                 if partial_ in part['filename']]):
                                
                                logging.info(part['filename'])
                                ext = part['filename'].split('.')[-1]
                                file_ = '_'.join(part['filename'].split('.')[:-1])
                                file_ = re.sub(r'\W+', '_', file_).strip()
                                path = f"{path_to_salve}/{file_}.{ext}"
                                if not os.path.exists(path):
                                    attachment_id = part['body']['attachmentId']
                                    attachment = self.service.users().messages().attachments().get(
                                        userId='me', messageId=message['id'], id=attachment_id).execute()

                                    data = attachment['data']
                                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                                    with open(path, 'wb') as f:
                                        f.write(file_data)
                                    logging.info(f"Attachment {part['filename']} saved to {path}")
                        except Exception as e:
                            logging.exception(e)
                except Exception as e:
                    logging.exception(e)
            # Check for next page
            if 'nextPageToken' in results:
                conter+=1
                logging.info('nextPageToken',results['nextPageToken'])
                results = self.service.users().messages().list(userId='me', q=query,
                                                           pageToken=results['nextPageToken']).execute()
            else:
                break


if __name__ == '__main__':
    gmail = Gmail()
    filename_to_search = '41240944914992003820570020152810441152810446_cte.xml'  # Nome do arquivo a ser pesquisado
    gmail.download_all_attachments()
    #gmail.find_and_download_attachment(filename_to_search)
