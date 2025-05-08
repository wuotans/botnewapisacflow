from priority_classes.ssw.ssw import SswRequest
import time
import logging

class Ssw014(SswRequest):
    def __init__(self):
        super().__init__()

    def _op014_upload_file(self, html, file_path, file_name, **kwargs):
        url = "https://sistema.ssw.inf.br/bin/ssw0475"

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            # "Content-Type": "application/pdf",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }

        data = {
            "t_nro_lote": "",
            "f5": "",  # (None, '', 'application/octet-stream'),
            "t_ser_ret_ind": "",
            "t_nro_ret_ind": "",
            "t_nro_nfse": "",
            "t_data_emi_nfse": "",
            "t_protocolo": "",
            "t_data_pes_ini": "",
            "t_data_pes_fin": "",
            "t_sit_pes": "",
            "t_ser_ret_pdf": 'cgn',
            "t_nro_ret_pdf": '020025',
            "act": "",
            "cidade": 'CUIABA',
            "uf": 'MT',
            "nro_tela_chamador": '2',
            "f14": "",
            "act": ""
        }
        logging.info(file_path)
        with open(file_path, 'rb') as f:
            file_ = f.read()
        files = {
            "f14": (file_name, file_, "application/pdf"),  # open(file_path,'rb')
            "f5": ('', file_, 'application/octet-stream')
        }
        time.sleep(1)
        query = self.convert_dict_to_query_url(data)
        data = self.update_query_values(html, query, 'name', act='', f14='', f5='', **kwargs)
        data = self.convert_query_url_to_dict(data, False)
        logging.info(data)
        response = self.session.post(url, headers=headers, data=data, files=files)
        logging.info('#' * 20, 'UPLOAD', '#' * 20)
        logging.info(response.text)

        response = self.session.post(url, headers=headers, data=data, files=files)

        # To check the response
        logging.info('#' * 20, 'UPLOAD', '#' * 20)
        logging.info(response.text)
        return response.text

    def op014(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - f14:
                - act:
                - f5: AssociarNFS-e:
                - t_ser_ret_pdf: Arquivo:
                - t_nro_ret_pdf: Arquivo:
                - cidade:
                - uf:
                - nro_tela_chamador:
                - file_path:
                - file_name:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '014'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0775", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        file_path = kwargs.pop('file_path')
        file_name = kwargs.pop('file_name')
        html = self._op014_upload_file(response.text, file_path, file_name, **kwargs)
        g14 = f"C:\fakepath\{file_name}"

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'RET_PDF'
        query = ("filename_qtd=&filename_ori1=&f14=&act=RET_PDF&f5=&t_ser_ret_pdf=cgn&t_nro_ret_pdf=&g14=C%3A"
                 "%5Cfakepath%5CCGN020024-7.pdf&cidade=CUIABA&uf=MT&nro_tela_chamador=2&dummy=1695147148577")
        query = self.update_query_values(response.text, query, 'name', act=act, g14=g14, f5='', f14='',
                                         dummy='1695147148577', **kwargs)
        logging.info(query)
        query_model = "filename_enc=&filename_ori="
        data = self.update_query_values(html, query_model, 'name', dummy='1695147148577', **kwargs)
        logging.info(data)
        data = self.convert_query_url_to_dict(data, False)
        logging.info(data)
        data = (query
                .replace('filename_ori1=', f"filename_ori1={data['filename_ori']}")
                .replace('f14=', f"f14={data['filename_enc']}")
                .replace('filename_qtd=', f"filename_qtd=2"))
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw2234", headers=self.headers, data=data)

        # showing results
        logging.info('#' * 20, 'LAST', '#' * 20)
        logging.info(response.text)
        return response

        # self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw014() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op014()
