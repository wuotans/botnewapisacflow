from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw435(SswRequest):
    def __init__(self):
        super().__init__()

    def op435(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '435'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0103", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'PES'
        query_model = "act=PES&cod_emp_ctb=01&t_data_ref_ini=010101&t_data_ref_fim=171223&t_tp_fil=C&t_tp_cliente=C&t_tp_cli_fat=T&t_situacao_ctrc=I&t_periodicidade=T&t_rel_lista=C&t_cons_bloqueados=N&t_cons_a_vista=N&t_tp_classificacao=F&t_excel=s&t_ler_morto=N&dummy=1702912851885"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0103", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
