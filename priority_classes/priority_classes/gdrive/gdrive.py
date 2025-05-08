import os
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


class Gdrive:

    def __init__(self):
        # Initialize the Drive v3 API
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
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
                flow = InstalledAppFlow.from_client_secrets_file('drive.json', self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('drive', 'v3', credentials=creds)
        return service

    @time_out(time_out=3)
    def create_folder(self, folder_name):
        """Create a folder in Google Drive and return its ID."""

        # Metadata for the folder
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        folder = self.service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        # logging.info(f"Folder '{folder_name}' created. ID: {folder_id}")
        return folder_id

    @time_out(time_out=3)
    def folder_exists(self, folder_name):
        """Check if a folder with the given name exists in Google Drive. Return its ID if it does, else return None."""

        # Search for folders with the specified name
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get('files', [])

        # Return the ID of the first folder found (if any)
        if folders:
            # logging.info(f"Folder '{folder_name}' already exists. ID: {folders[0]['id']}")
            return folders[0]['id']
        return None

    def create_folder_if_not_exists(self, folder_name):
        """Create a folder in Google Drive if it doesn't already exist. Return its ID."""
        existing_folder_id = self.folder_exists(folder_name)
        if existing_folder_id:
            return existing_folder_id
        else:
            return self.create_folder(folder_name)

    @time_out(time_out=3)
    def get_shareable_link(self, file_id,link_format:str='download'):
        """
        Make the file publicly viewable and return its link
        """
        # Make the file viewable by 'anyone with the link'
        self.service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'},
            fields='id'
        ).execute()

        if link_format == 'share':
            link = f"https://drive.google.com/uc?id={file_id}"
        elif link_format == 'download':
            link = f"https://drive.google.com/uc?export=download&id={file_id}"

        return link

    @time_out(time_out=3)
    def delete_file(self, file_id):
        """
        Delete the file from Google Drive
        """
        self.service.files().delete(fileId=file_id).execute()
        logging.info(f"Deleted file with ID: {file_id}")

    def delete_all_files_and_folders(self):
        """Delete all files and folders in Google Drive."""
        while self.list_all_files():
            [self.delete_file(item['id']) for item in self.list_all_files()]
        logging.info(f"All files deleted...")

    @time_out(time_out=3)
    def list_all_files(self):
        """List all files and folders in Google Drive."""
        results = self.service.files().list().execute()
        items = results.get('files', [])
        return items

    @time_out(time_out=3,raise_exception=False)
    def upload_to_drive(self, filename,
                        folder_name=None,
                        link_format:str='download',
                        mimetype:str='application/pdf',
                        **kwargs):
        file_metadata = {
            'name': os.path.basename(filename),
            'supportsAllDrives': True,
        }
        # If a folder_id is provided, set it as the parent folder for the uploaded file.
        if folder_name:
            folder_id = self.create_folder_if_not_exists(folder_name)
            file_metadata['parents'] = [folder_id]

        if 'drive_id' in kwargs:
            logging.info(kwargs['drive_id'])
            file_metadata['driveId'] = kwargs['drive_id']
            folder_id = self.find_folder_in_shared_drive(folder_name,kwargs['drive_id'])
            file_metadata['parents'] = [folder_id]

        media = MediaFileUpload(filename, mimetype=mimetype, resumable=True)

        try:
            file_ = self.service.files().create(body=file_metadata,
                                                media_body=media,
                                                supportsAllDrives=True,
                                                fields='id').execute()
            file_id = file_.get('id')
            # logging.info(f'File ID: {file_id}')

            # Get shareable link
            link = self.get_shareable_link(file_id,link_format)
            logging.info(f'Shareable link: {link}')

            return link
        except HttpError as error:
            logging.info(f'An error occurred: {error}')

    @time_out(time_out=3)
    def file_exists_in_folder(self, file_name, folder_id=None):
        """Check if a file with the given name exists in the specified folder. Return its ID if it does, else return None."""

        # Search for files with the specified name in the given folder
        query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])

        # Return the ID of the first file found (if any)
        if files:
            # logging.info(f"File '{file_name}' already exists in folder ID: {folder_id}. File ID: {files[0]['id']}")
            return files[0]['id']
        return None

    def upload_file_if_not_exists(self,
                                  file_path,
                                  folder_name,
                                  link_format:str='download',
                                  mimetype:str='application/pdf',
                                  **kwargs):
        file_name = os.path.basename(file_path)

        folder_id = self.create_folder_if_not_exists(folder_name) if folder_name else None

        existing_file_id = self.file_exists_in_folder(file_name, folder_id)
        if existing_file_id:
            return existing_file_id
        else:
            return self.upload_to_drive(file_path, folder_name,link_format,mimetype,**kwargs)

    def list_shared_drives(self):
        """
        Lists all shared drives available to the authenticated user or service account.
        """
        try:
            # Initial call to retrieve shared drives
            result = self.service.drives().list(pageSize=10).execute()
            drives = result.get('drives', [])

            while 'nextPageToken' in result:
                # Retrieve next page of shared drives
                page_token = result['nextPageToken']
                result = self.service.drives().list(pageSize=10, pageToken=page_token).execute()
                drives.extend(result.get('drives', []))

            for drive in drives:
                logging.info(f"Drive ID: {drive['id']}, Drive Name: {drive['name']}")
            return drives
        except Exception as e:
            logging.info(f"An error occurred: {e}")
            return None

    def find_folder_in_shared_drive(self, folder_name, drive_id):
        """
        Finds a folder within a specific shared drive by name.

        :param folder_name: Name of the folder to find.
        :param drive_id: ID of the shared drive where to search for the folder.
        :return: The ID of the found folder or None if not found.
        """
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        try:
            response = self.service.files().list(q=query,
                                                 spaces='drive',
                                                 corpora='drive',
                                                 driveId=drive_id,
                                                 includeItemsFromAllDrives=True,
                                                 supportsAllDrives=True,
                                                 fields='files(id, name)').execute()
            folders = response.get('files', [])

            # Assuming the first matching folder is the one you want
            if folders:
                folder = folders[0]
                logging.info(f"Folder ID: {folder['id']}, Folder Name: {folder['name']}")
                return folder['id']
            else:
                logging.info("No folder found with the specified name.")
                return None
        except Exception as e:
            logging.info(f"An error occurred: {e}")
            return None


if __name__ == '__main__':
    logging.info(os.getcwd())
    drive = Gdrive()
    drive.upload_file_if_not_exists('pdf_3550217-22.pdf', 'unidades')
