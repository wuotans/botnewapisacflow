import logging
import time
import os

from priority_classes.ssw.ssw_v2 import SswRequest


class Ssw116(SswRequest):
    def __init__(self,name_instance='ssw_', **kwargs):
        super().__init__(name_instance=name_instance,**kwargs)
        self.html_content = None
        self.html_text = None
        self.name_instance = name_instance
    
    def _upload_file(self, file_path, **kwargs):
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
            "f3": "06347409006953",
            "_3": "SBF COMERCIO DE PRODUTOS ESPOR",
            "f4": "C",
            "f5": "P",
            "f6": "P",
            "f7": "A",
            "f8": "",
            "f9": "2",
            "f10": "164",
            "f11": "",
            "f12": "",
            "f13": "B",
            "f14": "C",
            "f15": "D",
            "f16": "",
            "f17": "",
            "f18": "",
            "f19": "",
            "f20": "",
            "f21": "",
            "f22": "",
            "f23": "",
            "f24": "",
            "f25": "",
            "f26": "",
            "f27": "",
            "f28": "",
            "f29": "",
            "f30": "E",
            "f31": "",
            "f32": "",
            "f33": "",
            "f34": "",
            "f35": "",
            "f36": "",
            "f37": "",
            "f38": "",
            "f39": "",
            "f40": "",
            "f41": "",
            "f42": "",
            "f43": "",
            "f44": "",
            "f45": "",
            "f46": "",
            "f47": "",
            "f48": "",
            "f49": "",
            "f50": "",
            "f51": "",
            "f52": "",
            "f53": "",
            "f54": "",
            "f55": "",
            "f56": "",
            "f57": "",
            "f58": "",
            "f59": "",
            "f60": "",
            "f61": "P",
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
            "f62": (filename, filebin,'text/csv'),
        }

        time.sleep(1)

        # convertendo o dicionario para um url encoder
        query = self.convert_dict_to_query_url(data)
        print(query)

        # atualiza os valores dos parametros da url com os valores informados em kwargs caso contrario com os valores encontrados na pagina html
        data = self.update_query_values(self.html_text,
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
        self.params_from_upload = self.get_input_values_from_html(response.text)
        logging.info(f'Params: {self.params_from_upload }')
        # # confirma a requisição post
        # response = self.session.post(url, headers=headers, data=data, files=files)

        # # To check the response
        # logging.info('#' * 20, 'UPLOAD', '#' * 20)
        # logging.info(f'Status code: {response.status_code}')
        # logging.info(response.text)
        return self
    
    def _download_report(self,**kwargs):
        """
            :param kwargs:
            Possible keys include:
                - f3: cnpj
                - f4: (C-cliente,G-grupo)
                - f5: (E-emitente,D-destinatário,P-pagador)
                - f6: (N-NotaFiscal,P-Pedido,C-CTRC,E-CTe,O-CTRCOrigem,V-VolumedoCliente)
                - f7: Colunadasérie(opc):
                - f8: Linhas:
                - f9: a
                - f10: Arquivoexportado:
                - f11: Horadaocorrência:
                - f12: Código:
                - f13: Descrição:
                - f14: Complemento:
                - f15: Datainclusãoocorrência:
                - f16: Horainclusãoocorrência:
                - f17: Usuárioinclusãoocorrência:
                - f18: Localizaçãoatual:
                - f19: CTRC:
                - f20: CTE:
                - f21: RecebedordoCTRC:
                - f22: PagadordoCTRC:
                - f23: Unidadededestino:
                - f24: Cidadedeentrega:
                - f25: CEPdeentrega:
                - f26: Código(DE/PARA):
                - f27: Descrição(DE/PARA):
                - f28: Valormercadoria:
                - f29: PrevisãodeEntrega:
                - f30: NúmeroPedido:
                - f31: Série/NúmeroNF:
                - f32: RemetentedoCTRC:
                - f33: Comprovantedeentrega:
                - f34: CódigodaMercadoria:
                - f35: Setordeentrega:
                - f36: DestinatáriodoCTRC:
                - f37: EndereçoDestinatário:
                - f38: BairroDestinatário:
                - f39: ArquivoEDIocorrência:
                - f40: Data/HoraEDIocorrência:
                - f41: ArquivoEDIembarcados:
                - f42: Data/HoraEDIembarcados:
                - f43: ProtocoloWebservice:
                - f44: Data/HoraAverbação:
                - f45: RetornoAverbação:
                - f46: MotoristaEntrega:
                - f47: NomearquivoEDI:
                - f48: RazãoSocialDestinatário:
                - f49: Cod.barrasvolcliente:
                - f50: Ocorrênciadeprimeiravisita:
                - f51: DatadaOcoprimeiravisita:
                - f52: DataemissãoCTRC:
                - f53: DataautorizaçãoCTe:
                - f54: ChaveCT-e:
                - f55: ChaveCT-econtratante:
                - f56: TipoDocumento:
                - f57: ChaveNf-e:
                - f58: NroNR:
                - f59: Fatura:
                - f60: Basededados:
                - f61: (P-principal,M-morto)
                - act:
            :type kwargs: dict
            :return: None
        """
        if not self.params_from_upload :
            raise ValueError(
                f'Is needle to upload the file first the get the correct params: {self.params_from_upload}'
            )
        act = kwargs.pop('act') if 'act' in kwargs else 'REC'
        query_model = "filename_ori=cnto.csv&f62=241024161948&act=REC&f3=06347409006953&_3=SBF COMERCIO DE PRODUTOS ESPOR&f4=C&f5=P&f6=P&f7=A&f8=&f9=2&f10=164&f11=&f12=&f13=B&f14=C&f15=D&f16=&f17=&f18=&f19=&f20=&f21=&f22=&f23=&f24=&f25=&f26=&f27=&f28=&f29=&f30=E&f31=&f32=&f33=&f34=&f35=&f36=&f37=&f38=&f39=&f40=&f41=&f42=&f43=&f44=&f45=&f46=&f47=&f48=&f49=&f50=&f51=&f52=&f53=&f54=&f55=&f56=&f57=&f58=&f59=&f60=&f61=P&g62=C%3A%5Cfakepath%5Ccnto.csv&dummy=1729797588091"
        data = self.update_query_values(self.html_text,
                                        query_model,
                                        'name',
                                        act=act,
                                        filename_ori=self.params_from_upload['filename_ori'],
                                        f62=self.params_from_upload['filename_enc'],
                                        g62=fr'C:\fakepath\{self.params_from_upload['filename_ori']}',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1095", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.html_text = response.text
        self.handle_download(response.text)


    def op116(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - file_path: The absolute path of the csv file to upload
                - f3: cnpj
                - f4: (C-cliente,G-grupo)
                - f5: (E-emitente,D-destinatário,P-pagador)
                - f6: (N-NotaFiscal,P-Pedido,C-CTRC,E-CTe,O-CTRCOrigem,V-VolumedoCliente)
                - f7: Colunadasérie(opc):
                - f8: Linhas:
                - f9: a
                - f10: Arquivoexportado:
                - f11: Horadaocorrência:
                - f12: Código:
                - f13: Descrição:
                - f14: Complemento:
                - f15: Datainclusãoocorrência:
                - f16: Horainclusãoocorrência:
                - f17: Usuárioinclusãoocorrência:
                - f18: Localizaçãoatual:
                - f19: CTRC:
                - f20: CTE:
                - f21: RecebedordoCTRC:
                - f22: PagadordoCTRC:
                - f23: Unidadededestino:
                - f24: Cidadedeentrega:
                - f25: CEPdeentrega:
                - f26: Código(DE/PARA):
                - f27: Descrição(DE/PARA):
                - f28: Valormercadoria:
                - f29: PrevisãodeEntrega:
                - f30: NúmeroPedido:
                - f31: Série/NúmeroNF:
                - f32: RemetentedoCTRC:
                - f33: Comprovantedeentrega:
                - f34: CódigodaMercadoria:
                - f35: Setordeentrega:
                - f36: DestinatáriodoCTRC:
                - f37: EndereçoDestinatário:
                - f38: BairroDestinatário:
                - f39: ArquivoEDIocorrência:
                - f40: Data/HoraEDIocorrência:
                - f41: ArquivoEDIembarcados:
                - f42: Data/HoraEDIembarcados:
                - f43: ProtocoloWebservice:
                - f44: Data/HoraAverbação:
                - f45: RetornoAverbação:
                - f46: MotoristaEntrega:
                - f47: NomearquivoEDI:
                - f48: RazãoSocialDestinatário:
                - f49: Cod.barrasvolcliente:
                - f50: Ocorrênciadeprimeiravisita:
                - f51: DatadaOcoprimeiravisita:
                - f52: DataemissãoCTRC:
                - f53: DataautorizaçãoCTe:
                - f54: ChaveCT-e:
                - f55: ChaveCT-econtratante:
                - f56: TipoDocumento:
                - f57: ChaveNf-e:
                - f58: NroNR:
                - f59: Fatura:
                - f60: Basededados:
                - f61: (P-principal,M-morto)
                - act:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '116'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1095", headers=self.headers, data=data)
        logging.info(response.text)
        self.html_text = response.text
        self._upload_file(kwargs.pop('file_path'))
        self._download_report(**kwargs)
        


if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
