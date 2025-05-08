from bs4 import BeautifulSoup
from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw571(SswRequest):
    def __init__(self):
        super().__init__()
    @staticmethod
    def _op571_get_acni_number1(html):
        soup = BeautifulSoup(html, "html.parser")
        last_acni = soup.find("a", id="15").text
        return last_acni

    def _op571_throw_transfers(self, html, **kwargs):
        # query filters to request record
        query_model = ("act=INCLUSAO&cod_emp_ctb=01&f3=341&f4=01433&f5=1&f6=000024937&f7=0&f8=300623&f9=valor&f10"
                       "=teste&dummy=1688135718822")
        data = self.update_query_values(html, query_model, 'name', act='INCLUSAO', dummy='1688135718822',
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1863", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1863", headers=self.headers, data=data)

        return self._op571_get_acni_number1(response.text)

    def _op571_delete_acni(self, html, **kwargs):
        # query filters to request record
        query_model = "act=EXCLUSAO&cod_emp_ctb=01&f3=341&f4=01433&f5=1&f6=000024937&f7=0&f8=290124&f19=1020293&dummy=1706535652607"
        data = self.update_query_values(html, query_model, 'name', act='EXCLUSAO', dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1863", headers=self.headers, data=data)

        logging.info(response.text)
        if '<!--GoBack-->' in response.text:
            return True

        return False


    def _op571_get_reports(self, html, **kwargs):
        # query filters to request record
        query_model = ("act=PENDENTES&cod_emp_ctb=01&f3=341&f4=01433&f5=1&f6=000024937&f7=0&f8=091023&f23=341&f24"
                       "=01433&f25=1&f26=24937&f27=0&f28=061023&f29=091023&dummy=1696875428932")
        data = self.update_query_values(html, query_model, 'name', act='PENDENTES', dummy='1688135718822',
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1863", headers=self.headers, data=data)
        logging.info(response.text)

        self.handle_download(response.text)

    def op571(self, *args, **kwargs):
        """
        :param args:
            'throw_transfers',
            'report',
            'delete'
        :param kwargs:
        Possible keys include:
            - act: 'INCLUSAO', 'PENDENTES', 'EXCLUSAO'
            - cod_emp_ctb: empresa:
            - f3: Banco:
            - f4: ag:
            - f5: dvag:
            - f6: ccor:
            - f7: dvccor:
            - f8: Datacrédito:
            - f9: Valordocrédito:
            - f10: Motivo:
            - f19: ACNI para excluir
            - f23: Banco
            - f24: ag
            - f25: dvag
            - f26: ccor
            - f27:dvccor
            - f28: data inicial
            - f29: data final
        :type kwargs: dict
        :return: None
        """
        self.last_opssw = '571'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1863", headers=self.headers, data=data)

        if 'throw_transfers' in args:
            return self._op571_throw_transfers(response.text, **kwargs)

        if 'report' in args:
            self._op571_get_reports(response.text, **kwargs)

        if 'delete' in args:
            return self._op571_delete_acni(response.text,**kwargs)


if __name__ == '__main__':
    with Ssw571() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op571('report',f28='301123',f29='301123')
