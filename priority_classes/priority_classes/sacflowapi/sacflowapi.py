import requests
import logging
import os

class SacflowErrorResponse(Exception):...

class Sacflow:

    def __init__(self):
        """
        A class for interacting with the Sacflow API to send WhatsApp messages.
        """
        self.url = "https://api.sacflow.io/api/send-text"
        self.headers = {
            "cookie": "connect.sid=s%253AV_jt6endHFeX9Jsl-RjtakaBSJOGBcDJ.D6bTeuL%252FqpCa4jwU3ky0E4VBvxdZ13KK5DHcBsh31a0",
            "authorization": os.getenv('SACFLOW_API_TOKEN'),
            "Content-Type": "application/json"
        }

        self.payload = {
            "from": "Botcvl",
            "accountId": 2,
            "tagId": 947,
            "queueId": 553,
            "whatsappId": 102,  # id whatsapp proc.qualidade
            "message": "",
            "contact": {
                "name": "Bot",
                "phone": "556584455091"
            },
            "isPrivate": False,
            "messageTimeout": 120,
            "document": {
                "url": '',
                "fileName": "report",
                "caption": "file"
            }

        }

    def send_msg_to_number(self, number, msg, whatsappId: int = 102, tagId: int = 947, queueId: int = 553,
                           file_url: str = ''):
        """
        Send a WhatsApp message to the specified number.

        :param number: The recipient's phone number.
        :type number: str
        :param msg: The message to be sent.
        :type msg: str
        :param whatsappId: The WhatsApp ID, defaults to 102.
        :type whatsappId: int, optional
        :return: True if the message was successfully added to the queue, False otherwise.
        :rtype: bool
        """
        self.payload.update({'tagId': tagId})
        self.payload.update({'queueId': queueId})
        self.payload.update({'message': msg})
        self.payload.update({'whatsappId': whatsappId})
        self.payload.update({'contact': {
            "name": "Bot",
            "phone": str(number)
        }})
        self.payload.update({'document': {
            "url": file_url,
            "fileName": "report",
            "caption": "file"
        }})
        logging.info(self.payload)
        response = requests.request("POST", self.url, json=self.payload, headers=self.headers)
        ret = response.json()
        logging.info(ret)
        if 'error' in ret:
            raise SacflowErrorResponse(
                f"Ocorreu um error na requisição: {ret}"
            )
        return ret


if __name__ == '__main__':
    sac = Sacflow()
    sac.send_msg_to_number('5565984455091',
                           "hi there! What's up?"
                           )
