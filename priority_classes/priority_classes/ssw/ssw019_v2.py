from priority_classes.ssw.ssw_v2 import SswRequest
import logging

class Ssw019(SswRequest):
    def __init__(self,name_instance='ssw019', **kwargs):
        super().__init__(name_instance=name_instance,**kwargs)
        self.html_content = None
        self.html_text = None
        self.name_instance = name_instance

    def op019(self, *args, **kwargs):
        """
        :param kwargs:
        Possible keys include:
            - l_siglas_familia: PARA
            - uf_dest_1: (opcional)
            - data_prev_man: (opcional)
            - hora_prev_man: (opcional)
            - data_emit_ctrc: (opcional)
            - hora_emit_ctrc: (opcional)
            - status_ctrc: (P-pré-CTRC,C-CTRC,S-segregados)
            - ctrc_pendente: (S-sempendência,C-compendência,T-todos)
            - lista_pendencias: (S/N)
            - apenas_descarregados: (S-sim,I-iniciado,T-todos)
            - lista_reversa: (N-semReversa,S-sóReversa,T-Todos)
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
        self.last_opssw = '019'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0036", headers=self.headers, data=data)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = ("act=ENV&l_siglas_familia=CGB&uf_dest_1=pa&data_prev_man=270623&hora_prev_man=0518"
                       "&data_emit_ctrc=260623&hora_emit_ctrc=1718&status_ctrc=C&ctrc_pendente=T&lista_pendencias=N"
                       "&apenas_descarregados=T&lista_reversa=T&apenas_prioritarios=T&id_tp_produto=T&fg_enderecados"
                       "=T&relacionar_produtos=N&relatorio_excel=s&button_env_enable=ENV&button_env_disable=btn_envia"
                       "&dummy=1687810826606")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0036", headers=self.headers, data=data)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw019() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op019()
