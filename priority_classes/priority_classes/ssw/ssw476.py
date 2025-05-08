from priority_classes.ssw.ssw import SswRequest
from urllib.parse import urlencode, unquote
import pandas as pd
import logging


class Ssw476(SswRequest):
    def __init__(self):
        super().__init__()

    def op476(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f5: num lançamento
                - cod_emp_ctb: Unidade:
                - f12: Períododepagamento:
                - filial2: Períododepagamento:
                - f13: a
                - f14: Períododeinclusão:
                - f21: Imprimircheque(S/N):
                - f22:
                - aprov_cent:
                - vlr_parcela: Datavencimento:
                - id_vlr_juro: Valordedesconto:
                - id_vlr_desconto: ValorLíquido:
                - id_vlr_liquido: À vista:
                - nro_banco_0: Agendadopara:
                - nro_agen_0: Agendadopara:
                - dig_agen_0: Agendadopara:
                - nro_cc_0: Agendadopara:
                - dig_cc_0: Agendadopara:
                - id_av_bompara: Valor:
                - id_av_vlr: Tipodecrédito:
                - id_av_tp_cred: (D-doc,T-ted,R-transferência,I-dinheiro)
                - nro_banco_1: Banco/ag/ccor(DVopc):
                - nro_agen_1: Banco/ag/ccor(DVopc):
                - dig_agen_1: Banco/ag/ccor(DVopc):
                - nro_cc_1: Banco/ag/ccor(DVopc):
                - dig_cc_1: Banco/ag/ccor(DVopc):
                - nro_banco_2: Banco/ag/ccor(DVopc):
                - nro_agen_2: Banco/ag/ccor(DVopc):
                - dig_agen_2: Banco/ag/ccor(DVopc):
                - nro_cc_2: Banco/ag/ccor(DVopc):
                - dig_cc_2: Banco/ag/ccor(DVopc):
                - nro_banco_3: Banco/ag/ccor(DVopc):
                - nro_agen_3: Banco/ag/ccor(DVopc):
                - dig_agen_3: Banco/ag/ccor(DVopc):
                - nro_cc_3: Banco/ag/ccor(DVopc):
                - dig_cc_3: Banco/ag/ccor(DVopc):
                - nro_banco_4: Banco/ag/ccor(DVopc):
                - nro_agen_4: Banco/ag/ccor(DVopc):
                - dig_agen_4: Banco/ag/ccor(DVopc):
                - nro_cc_4: Banco/ag/ccor(DVopc):
                - dig_cc_4: Banco/ag/ccor(DVopc):
                - nro_banco_5: Banco/ag/ccor(DVopc):
                - nro_agen_5: Banco/ag/ccor(DVopc):
                - dig_agen_5: Banco/ag/ccor(DVopc):
                - nro_cc_5: Banco/ag/ccor(DVopc):
                - dig_cc_5: Banco/ag/ccor(DVopc):
                - nro_banco_6: Banco/ag/ccor(DVopc):
                - nro_agen_6: Banco/ag/ccor(DVopc):
                - dig_agen_6: Banco/ag/ccor(DVopc):
                - nro_cc_6: Banco/ag/ccor(DVopc):
                - dig_cc_6: Banco/ag/ccor(DVopc):
                - nro_banco_7: Banco/ag/ccor(DVopc):
                - nro_agen_7: Banco/ag/ccor(DVopc):
                - dig_agen_7: Banco/ag/ccor(DVopc):
                - nro_cc_7: Banco/ag/ccor(DVopc):
                - dig_cc_7: Banco/ag/ccor(DVopc):
                - nro_banco_8: Banco/ag/ccor(DVopc):
                - nro_agen_8: Banco/ag/ccor(DVopc):
                - dig_agen_8: Banco/ag/ccor(DVopc):
                - nro_cc_8: Banco/ag/ccor(DVopc):
                - dig_cc_8: Banco/ag/ccor(DVopc):
                - nro_banco_9: Banco/ag/ccor(DVopc):
                - nro_agen_9: Banco/ag/ccor(DVopc):
                - dig_agen_9: Banco/ag/ccor(DVopc):
                - nro_cc_9: Banco/ag/ccor(DVopc):
                - dig_cc_9: Banco/ag/ccor(DVopc):
                - nro_banco_10: ImprimirosCheques(S/N):
                - nro_agen_10: ImprimirosCheques(S/N):
                - dig_agen_10: ImprimirosCheques(S/N):
                - nro_cc_10: ImprimirosCheques(S/N):
                - dig_cc_10: ImprimirosCheques(S/N):
                - id_imp_cheque: ChequeNominal(S/N):
                - id_chq_nominal: ImpressoraCHRONOS/Bematech(S/N):
                - id_imp_cheque_pronto: Por PEF:
                - id_pef_adm_codigo:
                - id_pef_vlr:
                - aprov_cent:
                - seq_desp_parcela:
                - ctrb:
                - seq_ficha_frete:
                - chamador:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '476'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0095", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'PES1'
        query_model = "act=PES1&f5=578287&cod_emp_ctb=01&f12=MTZ&filial2=CARVALIMA%20TRANSPORTES&f13=130324&f14=130324&f21=N&f22=N&aprov_cent=S&dummy=1710336846516"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0095", headers=self.headers, data=data)

        logging.info(unquote(response.text))
        params = self.get_input_values_from_html(unquote(response.text))
        datas=[]
        if 'web_body' in params:
            data = params['web_body'].split('?')[1].split("',")[0]
            datas.append(data)
        else:
            table = self.get_table(response.text,14)
            table = table.drop(0).reset_index(drop=True)
            logging.info(table)
            ids = [id_.replace('>','') for id_ in table['<f13>']]
            datas = [f"act={id_}&chamador=&aprov_cent=S&imp_cheque=&dummy={self.get_dummy()}" for id_ in ids]

        logging.info(datas)
        ret=[]
        for data in datas:
            response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0095", headers=self.headers, data=data)
            logging.info(response.text)
            extracted = self.get_input_values_from_html(unquote(response.text))['vlr_parcela'].strip().replace('.','').replace(',','.')
            # extracted = self.extract_html_values(response.text,'Valor&nbsp;da&nbsp;despesa:</div>','">Empresa:</div>')
            # extracted = extracted.split('">R$')[1].split('</div>')[0].strip().replace('.','').replace(',','.')
            # logging.info(extracted)
            discount = str(float(extracted) - float(kwargs['id_vlr_liquido'].replace(',','.'))).replace('.',',')
            logging.info(discount)
            act = kwargs.pop('act') if 'act' in kwargs else 'LIQ'
            query_model = "act=LIQ&vlr_parcela=0%2C01&id_vlr_juro=0%2C00&id_vlr_desconto=0%2C00&id_vlr_liquido=0%2C01&nro_banco_0=999&nro_agen_0=09999&dig_agen_0=9&nro_cc_0=99999999&dig_cc_0=9%20&id_av_bompara=130324&id_av_vlr=0%2C01&id_av_tp_cred=i&nro_banco_1=341&nro_agen_1=01433&dig_agen_1=1&nro_cc_1=000024937&dig_cc_1=0&nro_banco_2=341&nro_agen_2=01433&dig_agen_2=1&nro_cc_2=000024937&dig_cc_2=0&nro_banco_3=341&nro_agen_3=01433&dig_agen_3=1&nro_cc_3=000024937&dig_cc_3=0&nro_banco_4=341&nro_agen_4=01433&dig_agen_4=1&nro_cc_4=000024937&dig_cc_4=0&nro_banco_5=341&nro_agen_5=01433&dig_agen_5=1&nro_cc_5=000024937&dig_cc_5=0&nro_banco_6=341&nro_agen_6=01433&dig_agen_6=1&nro_cc_6=000024937&dig_cc_6=0&nro_banco_7=341&nro_agen_7=01433&dig_agen_7=1&nro_cc_7=000024937&dig_cc_7=0&nro_banco_8=341&nro_agen_8=01433&dig_agen_8=1&nro_cc_8=000024937&dig_cc_8=0&nro_banco_9=341&nro_agen_9=01433&dig_agen_9=1&nro_cc_9=000024937&dig_cc_9=0&nro_banco_10=341&nro_agen_10=01433&dig_agen_10=1&nro_cc_10=000024937&dig_cc_10=0&id_imp_cheque=N&id_chq_nominal=N&id_imp_cheque_pronto=N&id_pef_adm_codigo=0&id_pef_vlr=0%2C00&aprov_cent=S&seq_desp_parcela=1238042&ctrb=&seq_ficha_frete=&chamador=&dummy=1710337006819"
            data = self.update_query_values(response.text,
                                            query_model,
                                            'name',
                                            act=act,
                                            id_vlr_desconto=discount,
                                            dummy=self.get_dummy(),
                                            **kwargs)
            logging.info(unquote(data))
            response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0095", headers=self.headers, data=data)
            logging.info(response.text)
            if '<!--CloseMe-->' in response.text:
                ret.append(str(True))
            else:
                ret.append(str(False))
        return  ';'.join(ret)


if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
