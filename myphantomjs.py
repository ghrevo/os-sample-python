from selenium.webdriver import phantomjs
from selenium.webdriver.common import utils
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#https://stackoverflow.com/questions/38044476/using-python-selenium-and-phantomjs-on-openshift-socket-binding-permission-den
class MyPhantomJSService(phantomjs.service.Service):
    def __init__(self, executable_path, port=0, service_args=None, log_path=None, ip=None):
        if ip is None:
            self.ip = '0.0.0.0'
        else:
            self.ip = ip
        phantomjs.service.Service.__init__(self, executable_path, port, service_args, log_path)

    def command_line_args(self):
        return self.service_args + ["--webdriver=%s:%d" % (self.ip, self.port)]

    def is_connectable(self):
        return utils.is_connectable(self.port, host=self.ip)

    @property
    def service_url(self):
        return "http://%s:%d/wd/hub" % (self.ip, self.port)


class MyPhantomWebDriver(RemoteWebDriver):

    def __init__(self, executable_path="phantomjs",
                 ip=None, port=0, desired_capabilities=DesiredCapabilities.PHANTOMJS,
                 service_args=None, service_log_path=None):

        self.service = MyPhantomJSService(
            executable_path,
            port=port,
            service_args=service_args,
            log_path=service_log_path,
            ip=ip)
        self.service.start()

        try:
            RemoteWebDriver.__init__(
                self,
                command_executor=self.service.service_url,
                desired_capabilities=desired_capabilities)
        except Exception:
            self.quit()
            raise

        self._is_remote = False

    def quit(self):

        try:
            RemoteWebDriver.quit(self)
        except Exception:
            # We don't care about the message because something probably has gone wrong
            pass
        finally:
            self.service.stop()