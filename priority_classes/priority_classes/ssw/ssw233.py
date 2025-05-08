from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw233(SswRequest):
    def __init__(self):
        super().__init__()

    def op233_upload_file(self, html, file_path, file_name, **kwargs):
        url = "https://sistema.ssw.inf.br/bin/ssw0475"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "iframe",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }

        data = {
            "t_ref_ini": "",
            "t_ref_fin": "",
            "t_prev_ini": "",
            "t_prev_fin": "",
            "t_orig": "",
            "unidade_orig": "",
            "t_dest": "",
            "unidade_dest": "",
            "t_cgc_pag": "",
            "t_nome": "",
            "t_oco_atual": "",
            "descricao_atual": "",
            "t_codigo": "99",
            "descricao_info": "CORRECAO DE INFORMACOES",
            "t_comple": "teste",
            "t_tp_data": "2",
            "t_data_ocor": "230823",
            "t_hora_ocor": "1003",
            "retira_rom": "0",
            "act": ""
        }

        query = self.convert_dict_to_query_url(data)
        data = self.update_query_values(html, query, 'name', act='', f5='', **kwargs)

        data = self.convert_query_url_to_dict(data, False)
        logging.info(data)

        # Ensure the file path is correct
        files = {
            "f5": (file_name, open(file_path, "rb"), "text/csv")
        }

        response = self.session.post(url, headers=headers, data=data, files=files)

        logging.info(response.text)
        return response.text

    def op233(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - filename_ori: name file csv
                - f5: date and hour now
                - act:
                - t_prev_ini: data autorizacao ini
                - t_prev_fin: data autorizacao fim
                - g5: fake file path 'C:\fakepath\AGA.csv'
                - t_codigo: codigo ocorrencia
                - t_comple: mensagem complementar
                - t_tp_data: (1-Previsãodeentrega,2-arquivo/abaixo)
                - t_data_ocor: data da ocorrencia
                - t_hora_ocor: hora da ocorrencia
                - retira_rom: (0-Nãoretira,1-Retira)
                - file_path: full path file
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '233'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw2333", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        file_path = kwargs.pop('file_path')
        file_name = kwargs.pop('filename_ori')
        g5 = f'C:\fakepath\{file_name}'

        html = self.op233_upload_file(response.text, file_path, file_name, **kwargs)

        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = ("act=ENV&g5=&t_prev_ini=220823&t_prev_fin=220823&f5=&t_codigo=99&descricao_info=CORRECAO%20DE"
                       "%20INFORMACOES&t_comple=teste&t_tp_data=2&t_data_ocor=220823&t_hora_ocor=1649&retira_rom=0"
                       "&dummy=1692737423688")
        data = self.update_query_values(response.text, query_model, 'name', act=act, f5='', g5=g5,
                                        dummy='1692737423688',
                                        **kwargs)
        logging.info(data)

        data2 = "filename_ori=AGA.csv&filename_enc=230823110402"
        data2 = self.update_query_values(html, data2, 'name')
        data2 = data2.replace('filename_ori', 'filename_ori').replace('filename_enc', 'f5')
        data = data2 + "&" + data.replace('f5=', '')
        logging.info(data)

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw2333",
                                     headers=self.headers,
                                     data=data)
        logging.info(response.text)

        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = ("btn_999=B&remember=1&useri=12345678909&lastcnpj_cotacao=&ssw_dom=OTC&token"
                       "=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTI4NzkzMzAsInB4eSI6IjE3Mi4zMS4zOC4yMzYifQ"
                       ".s-6XNr-3FDsbXxLjwLt9rnntvOL_wRMUxSLujcDWnm4&dummy=1692809504156")
        data3 = self.update_query_values(response.text,
                                         query_model,
                                         'name',
                                         btn_999='B',
                                         dummy='1692809504156',
                                         **kwargs)

        data = data + "&" + data3
        logging.info(data)

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw2333",
                                     headers=self.headers,
                                     data=data)

        # showing results

        logging.info(response.text)
        query_model = ("act=&t_prev_ini=220823&t_prev_fin=100923&t_oco_atual=17&descricao_atual=CHEGADA%20NA%20UNIDADE"
                       "%20DESTINO%2C%20AGUARDANDO%20DESCARGA&t_codigo=99&descricao_info=CORRECAO%20DE%20INFORMACOES"
                       "&t_comple=teste&t_tp_data=2&t_data_ocor=230823&t_hora_ocor=1251&retira_rom=0&web_body=abrir"
                       "%28%27botcvl_CRITICAS_135146%2Etxt%27%2C%20%27ssw2333_erro%2Esswweb%27%2C%201%2C%201%2C%20%27"
                       "%27%2C%205%29&msgx=Processamento%2520conclu%2526iacute%253Bdo%252E%252001%2520CTRC%2528s%2529"
                       "%2520receberam%2520ocorr%2526ecirc%253Bncia&dummy=1692809505067")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        dummy='1692809505067',
                                        **kwargs)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw2333",
                                     headers=self.headers,
                                     data=data)

        # showing results

        logging.info(response.text)


if __name__ == '__main__':
    with Ssw233() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op233()
