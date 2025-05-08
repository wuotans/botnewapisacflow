from bs4 import BeautifulSoup
from urllib.parse import unquote
from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw600(SswRequest):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _op600_get_seq_data(html):
        """
        Builds the URL to download a file from the 156 system.

        :param html: The HTML content containing the required values.
        :type html: str
        :return: The URL to download the file.
        :rtype: str
        """
        # Parse the HTML input
        soup = BeautifulSoup(html, "html.parser")
        web_body_value = soup.find("input", id="web_body")["value"]

        # Extract the required values from the web_body value
        decoded_text = unquote(web_body_value)
        logging.info(decoded_text)
        params = decoded_text.split("'")[3].split('?')[1]
        data = f'{params}&dummy=1695922682318'
        logging.info(data)
        return data

    def _op600_download_edi(self, html, name_file):
        key_ini = 'ssw0432?'
        key_fim = '"'
        index_ini = html.find(key_ini)
        index_fim = html[index_ini:].find(key_fim)

        if -1 not in (index_ini, index_fim):
            link = "https://sistema.ssw.inf.br/bin/" + html[index_ini:index_ini + index_fim]
            logging.info(link)
            self.request_download(link, name_file)

    def _op600_edi(self, *args, **kwargs):
        # query filters to request record
        cod_edi = kwargs.pop('cod_edi')
        data = f"act=ENV&f1={cod_edi}&dummy=1695922682221"
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0868", headers=self.headers, data=data)
        logging.info(response.text)

        data = self._op600_get_seq_data(response.text)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0778", headers=self.headers, data=data)
        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = ("&f2=280923&f3=280923&f7=N&f8=E&f9=D&f10=C&f11=F&f12=M&f13=A&f14=P&f15=T&f16=R&f17=H&f18=G&f19"
                       "=Z&tp_oper=")
        data2 = self.update_query_values(response.text,
                                         query_model,
                                         'name',
                                         act=act,
                                         **kwargs)
        logging.info(data2)
        data = data + data2
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0778", headers=self.headers, data=data)
        logging.info(response.text)

        name_file = kwargs.pop('name_file') if 'name_file' in kwargs else str(cod_edi) + '.txt'
        self._op600_download_edi(response.text, name_file)

    def op600(self, *args, **kwargs):
        """
            :param args:
                - 'info','edi','cnpj'
            :param kwargs:
            Possible keys include:
                - act:
                - cod_edi: codigo edi
                - f1: tipo cliente
                - f2: data ini
                - f3: data fim
                - f7: TodososCNPJs:
                - f8: TodososCNPJs:
                - f9: TodososCNPJs:
                - f10: TodososCNPJs:
                - f11: TodososCNPJs:
                - f12: TodososCNPJs:
                - f13: TodososCNPJs:
                - f14: TodososCNPJs:
                - f15: TodososCNPJs:
                - f16: TodososCNPJs:
                - f17: TodososCNPJs:
                - f18: TodososCNPJs:
                - f19: TodososCNPJs:
                - tp_oper:
                - name_file: the name of the file with its extention like 'filename.txt'
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '600'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0868", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        if 'edi' in args:
            self._op600_edi(*args, **kwargs)
        if 'info' in args:
            return self.get_table(response.text, 10)


if __name__ == '__main__':
    with Ssw600() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op600('info')
