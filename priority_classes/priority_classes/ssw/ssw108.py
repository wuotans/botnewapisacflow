from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw108(SswRequest):
    def __init__(self):
        super().__init__()

    def op108(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:'PES_OCO', 'PES_SEM'
                - t_sem_instr: sem instrução (s/n) -> PES_SEM
                - t_codigo: codigo ocorrencia
                - login_resp: Usuário
                - t_data_ini_ult: data inicial da ocorrencia
                - t_data_fim_ult: data final da ocorrencia
                - t_sel_atrasados: (A-atrasados,T-todos)
                - t_vid_rel: (V-vídeo,R-relatório,E-excelocor+instr,X-excelocorrências)
                - seq_ctrc:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '108'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0118", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'PES_OCO'
        query_model = ("act=PES_OCO&t_sem_instr=n&t_codigo=91&login_resp=botcvl&t_data_ini_ult=010122&t_data_fim_ult"
                       "=240823&t_sel_atrasados=T&t_vid_rel=e&seq_ctrc=0&web_body=&dummy=1692906821032")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0118", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw108() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op108(t_codigo='33')
