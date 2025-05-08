from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw903(SswRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_text = None

    def get_current_html(self):
        return self.html_text

    def op903_select_freight(self):
        data=f"dummy={self.get_dummy()}"
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1958", headers=self.headers, data=data)
        logging.info(response.text)
        self.html_text = response.text
        return self

    def op903_update_freight(self,*args,**kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f1: (S/N)
                - f2: (S/N)
                - f3: (S/N)
                - pis_cofins: (S/N)
                - f4: (S/N)
                - f5: (dias)
                - f6: (dias)
                - f7: (dias)
                - f8: (D-DescNTC,C-RC,N-nãobloquear)
                - f9: (D-DescNTC,C-RC,I-propostainicial,N-nãobloquear)
                - f10: %
                - f11: %
                - t_perc_adic_aplica_sob: (C-comum,E-Especial,T-Todos)
                - f12: R$
                - f13: R$
                - f14: R$
                - f15: R$
                - f16: R$
                - f17: R$
                - f18: B:
                - f19: C:
                - f20: Distrib.percent.acumuladanomês-dia01a10:
                - f21: dia11a20:
                - f22: dia11a20:
                - f23: dia11a20:
                - f24: dia11a20:
                - f25: dia11a20:
                - f26: dia11a20:
                - f27: dia11a20:
                - f28: dia11a20:
                - f29: dia11a20:
                - f30: dia11a20:
                - f31: dia21a31:
                - f32: dia21a31:
                - f33: dia21a31:
                - f34: dia21a31:
                - f35: dia21a31:
                - f36: dia21a31:
                - f37: dia21a31:
                - f38: dia21a31:
                - f39: dia21a31:
                - f40: dia21a31:
                - f41:
                - f42:
                - f43:
                - f44:
                - f45:
                - f46:
                - f47:
                - f48:
                - f49:
                - f50:
                - f51:
                - back_ssw0013:
                - aprov_central_tab:
                - perc_adic_frete:
                - perc_adic_aplica_sob:
                - prazo_tabela:
                - bloqueio_tab_vencida:
                - inativa_tab_venc:
                - exclui_tab_venc:
                - vlr_ped_exp:
                - vlr_pedagio:
                - vlr_frt_cortesia:
                - vlr_max_merc_cortesia:
                - vlr_max_merc_averb:
                - frt_inf_comimposto:
                - imposto_natabela:
                - pis_cofins_natabela:
                - bloqueia_frete:
                - bloqueia_frete_cotado:
                - perc_desc_prop_ini:
                - vlr_maximo_frete:
                - curva_abc_a:
                - curva_abc_b:
                - curva_abc_c:
                - perc_distrib01:
                - perc_distrib02:
                - perc_distrib03:
                - perc_distrib04:
                - perc_distrib05:
                - perc_distrib06:
                - perc_distrib07:
                - perc_distrib08:
                - perc_distrib09:
                - perc_distrib10:
                - perc_distrib11:
                - perc_distrib12:
                - perc_distrib13:
                - perc_distrib14:
                - perc_distrib15:
                - perc_distrib16:
                - perc_distrib17:
                - perc_distrib18:
                - perc_distrib19:
                - perc_distrib20:
                - perc_distrib21:
                - perc_distrib22:
                - perc_distrib23:
                - perc_distrib24:
                - perc_distrib25:
                - perc_distrib26:
                - perc_distrib27:
                - perc_distrib28:
                - perc_distrib29:
                - perc_distrib30:
                - perc_distrib31:
            :type kwargs: dict
            :return: None
        """

        self.op903_select_freight()
        act = kwargs.pop('act') if 'act' in kwargs else 'FRE2'
        query_model = "act=FRE2&f1=N&f2=S&f3=N&pis_cofins=S&f4=N&f5=360&f6=090&f7=180&f8=D&f9=I&f10=0%2C01&f11=0%2C00000&t_perc_adic_aplica_sob=C&f12=5%2C50&f13=0%2C00&f14=0%2C01&f15=0%2C00&f16=0%2C00&f17=15.000%2C00&f18=70&f19=20&f20=10&f21=03&f22=06&f23=09&f24=12&f25=16&f26=20&f27=23&f28=26&f29=29&f30=32&f31=35&f32=38&f33=42&f34=45&f35=48&f36=52&f37=55&f38=58&f39=62&f40=66&f41=69&f42=72&f43=76&f44=79&f45=81&f46=85&f47=89&f48=91&f49=95&f50=98&f51=100&back_ssw0013=S&aprov_central_tab=N&perc_adic_frete=%20%200%2C00000&perc_adic_aplica_sob=C&prazo_tabela=360&bloqueio_tab_vencida=N&inativa_tab_venc=090&exclui_tab_venc=180&vlr_ped_exp=5%2C50&vlr_pedagio=0%2C00&vlr_frt_cortesia=0%2C01&vlr_max_merc_cortesia=0%2C00&vlr_max_merc_averb=0%2C00&frt_inf_comimposto=S&imposto_natabela=N&pis_cofins_natabela=S&bloqueia_frete=D&bloqueia_frete_cotado=I&perc_desc_prop_ini=%20%200%2C01&vlr_maximo_frete=%20%20%20%2015000%2C00&curva_abc_a=70&curva_abc_b=20&curva_abc_c=10&perc_distrib01=03&perc_distrib02=06&perc_distrib03=09&perc_distrib04=12&perc_distrib05=16&perc_distrib06=20&perc_distrib07=23&perc_distrib08=26&perc_distrib09=29&perc_distrib10=32&perc_distrib11=35&perc_distrib12=38&perc_distrib13=42&perc_distrib14=45&perc_distrib15=48&perc_distrib16=52&perc_distrib17=55&perc_distrib18=58&perc_distrib19=62&perc_distrib20=66&perc_distrib21=69&perc_distrib22=72&perc_distrib23=76&perc_distrib24=79&perc_distrib25=81&perc_distrib26=85&perc_distrib27=89&perc_distrib28=91&perc_distrib29=95&perc_distrib30=98&perc_distrib31=100&dummy=1718141349565"
        data = self.update_query_values(self.html_text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1958", headers=self.headers, data=data)
        logging.info(response.text)
        self.html_text = response.text

    def op903(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: self
        """
        self.last_opssw = '903'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0013", headers=self.headers, data=data)
        logging.info(response.text)
        self.html_text = response.text
        return self

if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
