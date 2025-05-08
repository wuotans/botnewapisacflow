import pandas as pd
from priority_classes.ssw.ssw_v2 import SswRequest
import logging

class Ssw442(SswRequest):
    def __init__(self,name_instance='ssw442', **kwargs):
        super().__init__(name_instance=name_instance,**kwargs)
        self.html_content = None
        self.html_text = None
        self.name_instance = name_instance

    def op442(self, *args, **kwargs):
        """
             :param kwargs:
             Possible keys include:
                 - act:
                 - cod_emp_ctb: CTRC(comDV):
                 - f2: sigla ctrc
                 - f3: numero ctrc
                 - f9: a
                 - f10: Datacrédito/débito(opc):
             :type kwargs: dict
             :return: None
         """
        self.last_opssw = '442'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0145", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'CTR'
        query_model = "act=CTR&cod_emp_ctb=01&f2=cgb&f3=7212381&f9=220924&f10=221024&dummy=1729609453719"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0145", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.html_text = response.text
        return self

    def register_credit_debit(self,**kwargs)->pd.DataFrame:
        """
             :param kwargs:
             Possible keys include:
                 - f2: valor
                 - f3: tipo (C-crédito,D-débito)
                 - f4: descrição
             :type kwargs: dict
             :return: The dataframe with the registers
         """
        # query filters to request record
        query_model = "act=INC&f2=0%2C01&f3=c&f4=Liquida%E7%E3o%20interna&seq_ctrc=16492923&seq_fatura=0&dummy=1729613582573"
        data = self.update_query_values(self.html_text,
                                        query_model,
                                        'name',
                                        act='INC',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0145", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.html_text = response.text
        reg = self.get_table(self.html_text,7)
        return reg


if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
