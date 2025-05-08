from priority_classes.ssw.ssw_v2 import SswRequest
from urllib.parse import unquote, urlencode
import logging

class Ssw457(SswRequest):
    def __init__(self,name_instance='ssw_', **kwargs):
        super().__init__(name_instance=name_instance,**kwargs)
        self.html_content = None
        self.html_text = None
        self.name_instance = name_instance

    def op457(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = 'op457'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'NRO'
        query_model = ("act=NRO&t_nro_fatura=2201338&t_data_pes_ini=310823&t_data_pes_fin=291123&t_nao_liqui1=X"
                       "&t_liqui1=X&t_nao_liqui2=X&t_liqui2=X&t_nao_liqui3=X&t_liqui3=X&sequencia=457&dummy"
                       "=1701259227781")
        
        html = unquote(response.text)
        data = self.update_query_values(html,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.html_text = response.text
        # self.handle_download(response.text)
        return self
    
    def instrucoes(self, *args, **kwargs):
        logging.info(f"\n\n\n -------------------------------------- INSTRUCOES ")
        
        # query filters to request record
        query_model = ("act=INS&sequencia=457&ler_arq_morto=S&data0_ini=01012000&data0_fin=31122090&parcelada"
                       "=&seq_fatura=2461743&local=Q&dummy=1701259345588")
        
        html = unquote(self.html_text)
        data = self.update_query_values(html,
                                        query_model,
                                        'name',
                                        act="INS",
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        logging.info(response.text)
        self.html_text = response.text
        return self

    def select_instrucao(self, *args, **kwargs):
        '''act = I87, I86...'''
        act = kwargs.pop("act") if "act" in kwargs else "I87"
        logging.info(f"\n\n\n -------------------------------------- SELECIONANDO INSTRUCAO ")
        
        # query filters to request record
        query_model = "act=I87&sequencia=457&seq_fatura=2763137&ler_arq_morto=S&dummy=1722366478589"
        
        html = unquote(self.html_text)
        data = self.update_query_values(html,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        logging.info(response.text)
        self.html_text = response.text
        return self
    
    def lanca_87(self, *args, **kwargs):
        '''
        act = G87
        f1=1%2C23
        f2=textomotivo'''
        logging.info(f"\n\n\n -------------------------------------- LANCA 87")
        
        # query filters to request record
        query_model = "act=G87&f1=1%2C23&f2=bot&sequencia=457&seq_fatura=2763137&ler_arq_morto=&dummy=1722368901324"
        
        html = unquote(self.html_text)
        data = self.update_query_values(html,
                                        query_model,
                                        'name',
                                        act="G87",
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        logging.info(response.text)
        self.html_text = response.text
        return self

    def lanca_86(self, *args, **kwargs):
        '''
        act = G86
        f1=1%2C23
        f2=textomotivo'''
        logging.info(f"\n\n\n -------------------------------------- LANCA 86")
        
        # query filters to request record
        query_model = "act=G86&f1=1%2C23&f2=bot&sequencia=457&seq_fatura=2763137&ler_arq_morto=&dummy=1722368901324"
        
        html = unquote(self.html_text)
        data = self.update_query_values(html,
                                        query_model,
                                        'name',
                                        act="G86",
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        logging.info(response.text)
        self.html_text = response.text
        return self

    def lanca_85(self, *args, **kwargs):
        '''
        act = I85
        inp_85=250824'''
        logging.info(f"\n\n\n -------------------------------------- LANCA 85")
        
        # query filters to request record
        query_model = ("act=I85&sequencia=457&seq_fatura=2763879&ler_arq_morto=&sequencia=457"
                       "&inp_85=250824&seq_fatura=2763879&ler_arq_morto=&dummy=1722517653817&remember=1&useri=12345678909&ssw_dom=OTC"
                       "&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjI1OTU5ODEsInB4eSI6IjE3Mi4zMS41My4yNDcifQ.wg7g40YSDWCHrJAG8AjlfmwYeYTaV9rWG_h5DB3p1As&dummy=1722517671929")
        
        html = unquote(self.html_text)
        data = self.update_query_values(html,
                                        query_model,
                                        'name',
                                        act="I85",
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        logging.info(response.text)
        self.html_text = response.text
        return self

    



if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
