from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw381(SswRequest):
    def __init__(self):
        super().__init__()

    def op381(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f2:
                - t_aut_pes: (S/N)
                - t_aut_cub: (S/N)
                - t_aut_rec: (S/N)
                - t_aut_pac: (S/N)
                - t_aut_bar: (S/N)
                - t_aut_conf: (S/N)
                - t_aut_comple: (S/N)
                - t_imp_comp_ent: (S/N)
                - t_imp_comp_ent_fob_2vias: (S/N)
                - t_emi_ctrc_col: (S/N)
                - seq_cliente:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '381'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1844", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = "act=ENV&f2=03007331016579&dummy=1710444020388"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1844", headers=self.headers, data=data)
        logging.info(response.text)

        act = kwargs.pop('act') if 'act' in kwargs else 'EN2'
        query_model = "act=EN2&t_emi_ctrc_col=S&t_agrup_manual_lote=N&t_aut_pes=S&t_aut_cub=S&t_aut_rec=S&t_aut_pac=S&t_aut_bar=S&t_aut_conf=S&t_aut_comple=S&t_imp_comp_ent=S&t_imp_comp_ent_fob_2vias=S&seq_cliente=537076&dummy=1715800676673"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1844", headers=self.headers, data=data)
        logging.info(response.text)
        if '<!--CloseMe-->' in  response.text:
            return True
        return False
        #self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
