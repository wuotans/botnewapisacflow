from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw081(SswRequest):
    def __init__(self):
        super().__init__()

    def op081(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - data_prev_man: (opcional)
                - hora_prev_man: (opcional)
                - tp_cliente_pag: (A,B,C,T-todos)
                - tp_pessoa_dest: (J-jurídica,F-física,A-ambas)
                - status_ctrc: (P-pré-CTRC,C-CTRC,S-segregados)
                - ent_dificil: (S-sim,N-não,T-todos)
                - ctrc_pendente: (S-sempendência,C-compendência,T-todos)
                - lista_pendencias: (S/N)
                - lista_descarregados: (S-sim,I-iniciado,T-todos)
                - unid_dest_final: (M-minhaunidade,P-parceiros,T-todos)
                - lista_reversa: (N-semReversa,S-sóReversa,T-Todos)
                - a_so_agend_obrig: (S-sim,N-não,T-todos)
                - apenas_prioritarios: (S-sim,N-não,T-todos)
                - id_tp_produto: (P-perigoso,A-Anvisa,R-perecível,V-vacina,T-todos)
                - fg_enderecados: (S-sim,N-não,T-todos)
                - relacionar_produtos: (S/N)
                - relatorio_excel: (S/N)
                - button_env_enable:
                - button_env_disable:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '081'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0052", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = ("act=ENV&data_prev_man=171123&hora_prev_man=2206&tp_cliente_pag=T&tp_pessoa_dest=A&status_ctrc"
                       "=C&ent_dificil=T&ctrc_pendente=T&lista_pendencias=N&lista_descarregados=T&unid_dest_final=T"
                       "&lista_reversa=T&a_so_agend_obrig=T&apenas_prioritarios=T&id_tp_produto=T&fg_enderecados=s"
                       "&relacionar_produtos=N&relatorio_excel=s&button_env_enable=ENV&button_env_disable=btn_envia"
                       "&dummy=1700226512840")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0052", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw081() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op081()
