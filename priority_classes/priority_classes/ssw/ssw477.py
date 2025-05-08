from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw477(SswRequest):
    def __init__(self):
        super().__init__()


    def _op477_get_report(self,html_text,*args,**kwargs):
        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ARQ'
        query_model = ("act=ARQ&cod_emp_ctb=00&nro_lancto=1&nro_nf=2&chave_cte_nfe=3&cod_barras_boleto=4"
                       "&cgc_fornecedor=5&fornecedor=LUPA%20CONTAB%2CIMOBIL%20E%20ADVOCIA&nro_lancto_rel=6&nro_nf_rel"
                       "=7&vlr_nf=8%2C00&unid_pgto=9&gru_evento=01&evento_grupo=DESPESA%20COM%20PESSOAL%20%20%20%20"
                       "%20%20%20%20%20%20%20&cod_evento=02&mod_doc_fis=03&cfop_ent=04&bco=05&nro_banco_desp=06"
                       "&nro_cheque=07&placa=08&data_ini_emissao_nota_fiscal=090623&data_fin_emissao_nota_fiscal"
                       "=010623&data_ini_entrada_doc_fiscal=010623&data_fin_entrada_doc_fiscal=280623"
                       "&data_ini_inclusao_despesa=010623&data_fin_inclusao_despesa=010623&data_ini_pagamento_parcela"
                       "=010623&data_fin_pagamento_parcela=010623&data_ini_vencimento_parcela=010623"
                       "&data_fin_vencimento_parcela=010623&data_ini_caixa=010623&data_fin_caixa=010623&mes_comp=0623"
                       "&sit_desp=x&sit_arq=t&sequencia=477&dummy=1687964642754")
        data = self.update_query_values(html_text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0099", headers=self.headers, data=data)

        self.handle_download(response.text)

    def _op477_get_info(self,html_text,*args,**kwargs):
        act = kwargs.pop('act') if 'act' in kwargs else 'PES_CHAVE'
        query_model = ("act=PES_CHAVE&cod_emp_ctb=00&chave_cte_nfe=51230103128979001148550010000473321005861453&sit_desp=X&sit_arq=T&sequencia=477&dummy=1710883048350")
        data = self.update_query_values(html_text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0099", headers=self.headers, data=data)
        logging.info(response.text)
        df  =self.get_table(response.text,15)
        df.to_excel('ssw.xlsx')
        logging.info(df)
        if len(df)>1:
            df = df[(df['<f12>']!='>Cancelada') & (df['<f12>'].str.len()>0)].reset_index(drop=True)
            logging.info(df)
            seq = df.loc[0,'<f14>'].split('>')[1]
            logging.info(seq)
            data = f"act={seq}&sequencia=477&dummy={self.get_dummy()}"
            response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0099", headers=self.headers, data=data)
            logging.info(response.text)

        return  response.text

    def op477(self, *args, **kwargs):
        """
            :param args:
                 - 'report'
            :param kwargs:
            Possible keys include:
                - act:
                - cod_emp_ctb:
                - nro_lancto: NotaFiscal:
                - nro_nf: ChaveNF-e/CT-e:
                - chave_cte_nfe: Códbarrasboleto:
                - cod_barras_boleto: CNPJFornecedor:
                - cgc_fornecedor: Númerodolançamento:
                - fornecedor: Númerodolançamento:
                - nro_lancto_rel: NotaFiscal:
                - nro_nf_rel: Valordodocfiscal:
                - vlr_nf: Unidadepagamento:
                - unid_pgto: GrupodeEventos:
                - gru_evento: Evento:
                - evento_grupo: Evento:
                - cod_evento: Modelodocfiscal:
                - mod_doc_fis: CFOPEntrada:
                - cfop_ent: Banco:
                - bco: Banco/ag/ccor(DVopc):
                - nro_banco_desp: Númerodocheque:
                - nro_cheque: Placadoveículo:
                - placa: Períododeemissãonotafiscal:
                - data_ini_emissao_nota_fiscal: a
                - data_fin_emissao_nota_fiscal: Períododeentradadodocfiscal:
                - data_ini_entrada_doc_fiscal: a
                - data_fin_entrada_doc_fiscal: Períododeinclusãodespesa:
                - data_ini_inclusao_despesa: a
                - data_fin_inclusao_despesa: Períododepagamentoparcela:
                - data_ini_pagamento_parcela: a
                - data_fin_pagamento_parcela: Períododevencimentoparcela:
                - data_ini_vencimento_parcela: a
                - data_fin_vencimento_parcela: Períododocaixa(extrato):
                - data_ini_caixa: a
                - data_fin_caixa: Mêscompetência:
                - mes_comp: Sítuaçãodadespesa:
                - sit_desp: (P-pendente,L-liquidada,C-cancelada,T-todasmenoscanceladas,X-todas)
                - sit_arq: (B-enviadaabanco,C-cancelada,A-agendada,L-liquidada,D-excetoagendadas,T-todas)
                - sequencia:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '477'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1687963616301"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1687963616439"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0099", headers=self.headers, data=data)

        if 'report' in args:
            self._op477_get_report(response.text,*args,**kwargs)

        if 'info' in args:
            return self._op477_get_info(response.text,*args,**kwargs)



if __name__ == '__main__':
    with Ssw477() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op477(data_ini_inclusao_despesa='011223',data_fin_inclusao_despesa='011223')
