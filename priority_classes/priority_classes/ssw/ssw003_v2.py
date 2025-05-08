from priority_classes.ssw.ssw_v2 import SswRequest
import logging

class Ssw003(SswRequest):
    def __init__(self,name_instance='ssw601', **kwargs):
        super().__init__(name_instance=name_instance,**kwargs)
        self.html_content = None
        self.html_text = None
        self.name_instance = name_instance

    def op003_cancel_collect(self,*args,**kwargs):
        query_model = "act=CAN&nro_coleta=CGB%20099685&fld_data_lim=090724&fld_hora_lim=1800&fld_vlr_merc=0%2C00&fld_qtde_vol=8&fld_peso=15%2C000&fld_cub=0%2C0000&fld_peso_calc=15%2C000&cuba1=0%2C0000&cuba2=0%2C0000&cuba3=0%2C0000&cuba4=0%2C0000&cuba5=0%2C0000&cuba6=0%2C0000&cuba7=0%2C0000&cuba8=0%2C0000&cuba9=0%2C0000&cuba10=0%2C0000&cuba11=0%2C0000&cuba12=0%2C0000&cuba13=0%2C0000&cuba14=0%2C0000&cuba15=0%2C0000&cuba16=0%2C0000&cuba17=0%2C0000&cuba18=0%2C0000&cuba19=0%2C0000&cuba20=0%2C0000&cubatot=%23cubatot%23&data_local=050724&hora_local=1030&seq_coleta=3036604&col_fil=44&nro_coleta=99685&nro_romaneio=0&tipoFoto=coleta&nomeFoto=DTIMDMF&extraFoto=CGB%2F%20%20%20%20%20%20%20&nomeFotoUsed=&autorizado_por=&gr_informado=&gr_codigos=&act_old=&seq_cidade_coleta_h=2124&cep_coleta_h=78065000&cgc_pag_especie=&placa=&dummy=1720186264417"
        data = self.update_query_values(self.html_text,
                                        query_model,
                                        'name',
                                        act='CAN',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0018", headers=self.headers, data=data)

        query_model = "act=CAN&seq_coleta=3036604&col_fil=44&nro_coleta=99685&nro_romaneio=0&tipoFoto=coleta&nomeFoto=DTIMDMF&extraFoto=CGB%2F%20%20%20%20%20%20%20&nomeFotoUsed=&autorizado_por=&gr_informado=&gr_codigos=&act_old=&seq_cidade_coleta_h=2124&cep_coleta_h=78065000&cgc_pag_especie=&placa=&seq_coleta=3036604&nro_coleta=99685&btn_1=S&fld_data_lim=090724&fld_hora_lim=1800&fld_vlr_merc=0,00&fld_qtde_vol=8&fld_peso=15,000&fld_cub=0,0000&fld_peso_calc=15,000&cuba1=0,0000&cuba2=0,0000&cuba3=0,0000&cuba4=0,0000&cuba5=0,0000&cuba6=0,0000&cuba7=0,0000&cuba8=0,0000&cuba9=0,0000&cuba10=0,0000&cuba11=0,0000&cuba12=0,0000&cuba13=0,0000&cuba14=0,0000&cuba15=0,0000&cuba16=0,0000&cuba17=0,0000&cuba18=0,0000&cuba19=0,0000&cuba20=0,0000&cubatot=#cubatot#&data_local=050724&hora_local=1030&col_fil=44&nro_romaneio=0&tipoFoto=coleta&nomeFoto=DTIMDMF&extraFoto=CGB/       &nomeFotoUsed=&autorizado_por=&gr_informado=&gr_codigos=&act_old=&seq_cidade_coleta_h=2124&cep_coleta_h=78065000&cgc_pag_especie=&placa=&dummy=1720186264417&remember=1&ssw4importa=S&lastcnpj_cotacao=&useri=12345678909&permissao=&ssw_dom=OTC&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjAyNjc0MTMsInB4eSI6IjE3Mi4zMS41My4yNDcifQ.hFwDZq0kI4sfNMOr9_JlFuhuiF-RleY_CGyxP_9pa5E&dummy=1720186269936"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act='CAN',
                                        btn_1='S',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0018", headers=self.headers, data=data)

        logging.info(response.text)

        if '<!--CloseMe-->' in response.text:
            return True

        return False


    def op003(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f1: Porveículo,data:
                - f4: Númerodacoleta:
                - f7: Porcódigodebarras:
                - f13: Reimprimirfaixa(númerosemDV):
                - f21: Reimprimirfaixa(númerosemDV):
            :type kwargs: dict
            :return: None
        """

        self.last_opssw = '003'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0018", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'CCN'
        query_model = "act=CCN&f1=050724&f4=050724&f7=1026&f13=050724&f21=050724&dummy=1720185277666"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0018", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.html_text = response.text

        return self




if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
