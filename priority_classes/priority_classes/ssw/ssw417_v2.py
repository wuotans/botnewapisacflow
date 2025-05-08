import logging
import os, time


from priority_classes.ssw.ssw_v2 import SswRequest


class Ssw417(SswRequest):
    def __init__(self,name_instance='ssw417', **kwargs):
        super().__init__(name_instance=name_instance,**kwargs)
        self.html_content = None
        self.html_text = None
        self.name_instance = name_instance

    def _goto_importation_link(self,response,**kwargs):
        # query filters to request record
        query_model = "act=IMPORTAR&dummy=1731091029432"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act='IMPORTAR',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1591", headers=self.headers, data=data)
        return response
    
    def upload_table(self,response, file_path, **kwargs):
        response = self._goto_importation_link(response)

        url = "https://sistema.ssw.inf.br/bin/ssw0475"

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
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
        "act": ""
        }

        logging.info(file_path)

        # Le o arquivo binario
        with open(file_path, 'rb') as f:
            filebin = f.read()

        # Pegando do nome do arquivo
        filename = os.path.basename(file_path)
        logging.info(f'Filename: {filename}')

        files = {
            "f1": (filename, filebin,'text/csv'),
        }

        time.sleep(1)

        # convertendo o dicionario para um url encoder
        query = self.convert_dict_to_query_url(data)
        print(query)

        # atualiza os valores dos parametros da url com os valores informados em kwargs caso contrario com os valores encontrados na pagina html
        data = self.update_query_values(response.text,
                                        query,
                                        'name',
                                        act='',
                                        **kwargs)
        
        # converte a url para dict novamente
        data = self.convert_query_url_to_dict(data, False)
        logging.info(data)

        # realiza a requisição post
        response = self.session.post(url, headers=headers, data=data, files=files)
        logging.info('#' * 20, 'UPLOAD', '#' * 20)
        logging.info(f'Status code: {response.status_code}')
        logging.info(response.text)
        return response
    
    def submit_table(self,response,*args,**kwargs):
        self.params_from_upload = self.get_input_values_from_html(response.text)
        logging.info(f'Params: {self.params_from_upload }')
        # query filters to request record
        query_model = "filename_ori=Importacao%20CNH%20CGB.csv&f1=081124153912&act=IMPORTA2&g1=C%3A%5Cfakepath%5CImportacao%20CNH%20CGB.csv&dummy=1731091152083"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act='IMPORTA2',
                                        filename_ori=self.params_from_upload['filename_ori'],
                                        f1=self.params_from_upload['filename_enc'],
                                        g1=fr"C:\fakepath\{self.params_from_upload['filename_ori']}",
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1591", headers=self.headers, data=data)
        logging.info(response.text)
        return response

    def op417(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '417'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1591", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        return response


if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
