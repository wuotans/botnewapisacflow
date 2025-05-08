from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw493(SswRequest):
    def __init__(self):
        super().__init__()

    def op493(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act: 
                - p_ati_ini: a
                - p_ati_fin: Períododevencimento(opc):
                - tp_tabela: (N-normal,D-dirigida,A-ambas)
                - cli_class: (E-especial,C-comum,A-ambas)
                - situacao: (A-ativa,I-inativa,T-todas)
                - tp_arq: (E-Excel,T-texto)
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '493'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1625", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = "act=ENV&p_ati_ini=010122&p_ati_fin=310122&tp_tabela=A&cli_class=A&situacao=A&tp_arq=e&dummy=1707940886585"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1625", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
