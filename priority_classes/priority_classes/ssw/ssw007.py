import time

from priority_classes.ssw.ssw import SswRequest
from priority_classes.decorators.decorators import time_out
import logging

class Ssw007(SswRequest):
    def __init__(self):
        super().__init__()

    def _op007_open_rejecteds(self):
        script="""
        ajaxEnvia('REJEITADOS', 1)
        """
        self.driver.execute_script(script)
    @time_out(3)
    def _op007_get_list_ctrcs(self):
        script="""
        var ctrcs = document.querySelectorAll('a[class="sra"]')
        return ctrcs
        """
        return self.driver.execute_script(script)
    @time_out(3,raise_exception=False)
    def _op007_click_ctrc(self,ctrc):
        ctrc.click()
    @time_out(3)
    def _op007_click_change_ctrc(self):
        script="""
        concluindo('N')
        """
        return self.driver.execute_script(script)
    def _op007_click_submit_substitute(self,**kwargs):
        script = """
        calculafrete(this);return false;
        """
        self.driver.execute_script(script)
    @time_out()
    def _op007_skip_email(self,**kwargs):
        script = """
        goEmailPagPassa();
        """
        self.driver.execute_script(script)
    @time_out(3)
    def _op007_save_substitute(self,**kwargs):
        try:
            script = """
            concluindo('C');
            """
            self.driver.execute_script(script)
        except Exception as e:
            logging.exception(e)
            script = """
            continuaResumo();
            """
            self.driver.execute_script(script)
            raise  e
    def _op007_update_ctrcs(self,ctrcs):
        logging.info(ctrcs)
        for ctrc in ctrcs:
            self._op007_click_ctrc(ctrc)
            self.next_window(2)
            self._op007_click_change_ctrc()
            self._op007_click_submit_substitute()
            time.sleep(1)
            self._op007_skip_email()
            time.sleep(1)
            self._op007_save_substitute()
            time.sleep(3)
            self.next_window(1)
    def _op007_update_rejected(self):
        self.driver.get('https://sistema.ssw.inf.br/bin/ssw0767')
        self._op007_open_rejecteds()
        self.next_window(1)
        time.sleep(3)
        ctrcs = self._op007_get_list_ctrcs()
        self._op007_update_ctrcs(ctrcs)


    def op007(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '007'

        if 'update_rejected' in args:
            self._op007_update_rejected()



if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
