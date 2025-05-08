from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw441(SswRequest):
    def __init__(self):
        super().__init__()

    def op441(self, *args, **kwargs):
        """
        :param kwargs:
        Possible keys include:
            - act:
            - rel_sin_fg_data: (E-emissão,V-vencimento,L-liquidação,X-cancelamento)
            - rel_sin_per_pesq_ini: a
            - rel_sin_per_pesq_fin: Empresa:
            - rel_sin_classificacao: (F-filial,P-pordatade)
            - rel_sin_sit_fat: (P-pendente,L-liquidada,E-perdida,C-cancelada,T-todas)
            - rel_sin_fg_fat_desc: (I-Incluir,E-Excluir,S-Somentedescontadas)
            - tp_arquivo: (F-listafaturas,C-listafaturascomCTRCs)
            - rel_ana_fg_data: (E-emissão,V-vencimento,L-liquidação,X-cancelamento,C-créditonocaixa)
            - rel_ana_per_pesq_ini: a
            - rel_ana_per_pesq_fin: Empresa:
            - rel_ana_class_nro_fat: Situaçãodafatura:
            - rel_ana_sit_fat: (P-pendente,L-liquidada,E-perdida,C-cancelada,T-todasmenoscancelados)
            - rel_ana_crit_adc: (P-protesto,C-cartório,R-Serasa/Equifax,S-SPC,O-Opc480,T-todas)
            - rel_ana_fg_fat_desc: (I-Incluir,E-Excluir,S-Somentedescontadas)
            - rel_ana_fg_lista_ocor: (S-sim,N-não)
            - rel_ana_fg_ctrc_fob_dir: (S-sim,N-nãoverifica)
            - tp_cobranca: (B-banco,C-carteira,A-ambas)
            - rel_ana_vlr_max_fat: Vendedor:
            - rel_ana_periodicidade: (M-mensal,Q-quinzenal,D-dezenal,S-semanal,I-diário,T-todos)
            - rel_ana_arq_excel:
        :type kwargs: dict
        :return: None
        """
        self.last_opssw = '441'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3=441&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01",
                          headers=self.headers,
                          data=data)

        # second query post
        data = "sequencia=441&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0049",
                                     headers=self.headers,
                                     data=data)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ANA'
        query_model = ("act=ANA&rel_sin_fg_data=E&rel_sin_per_pesq_ini=260623&rel_sin_per_pesq_fin=260623"
                       "&rel_sin_classificacao=F&rel_sin_sit_fat=T&rel_sin_fg_fat_desc=I&tp_arquivo=F&rel_ana_fg_data"
                       "=E&rel_ana_per_pesq_ini=260623&rel_ana_per_pesq_fin=260623&rel_ana_class_nro_fat=X"
                       "&rel_ana_sit_fat=T&rel_ana_crit_adc=T&rel_ana_fg_fat_desc=I&rel_ana_fg_lista_ocor=N"
                       "&rel_ana_fg_ctrc_fob_dir=N&tp_cobranca=A&rel_ana_vlr_max_fat=9.999.999%2C99"
                       "&rel_ana_periodicidade=T&rel_ana_arq_excel=s&web_body=&dummy=1687779949807")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy='1687779949807',
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0049",
                                     headers=self.headers,
                                     data=data)

        self.handle_download(response.text)


if __name__ == '__main__':
    ssw = Ssw441()
    ssw.init_browser()
    ssw.login()
    ssw.op441()
