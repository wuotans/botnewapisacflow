from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw264(SswRequest):
    def __init__(self):
        super().__init__()
        self.method = 'selenium'

    def op264(self, *args, **kwargs):
        """
        This method goes to ssw op 264 and get the plates showed there

        :return: List of plates
        """
        self.last_opssw = '264'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        self.driver.get("https://sistema.ssw.inf.br/bin/ssw2138")

        script = """
        var plates = document.querySelectorAll('div[class="data"]')
        let data = []
        for (let i=0; i < plates.length;i++){
            data.push(plates[i].innerText)
        }
        return data
        """
        plates = self.driver.execute_script(script)
        return plates


if __name__ == '__main__':
    with Ssw264() as ssw:
        ssw.init_browser(method='selenium')
        ssw.login()
        ssw.credentials[4] = 'cgb'
        logging.info(ssw.op264())
