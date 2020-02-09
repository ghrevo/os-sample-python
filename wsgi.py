from flask import Flask
from flask import request
import json
import os
from selenium.webdriver import phantomjs
from selenium.webdriver.common import utils
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#https://realpython.com/absolute-vs-relative-python-imports/
#from . import MyPhantomWebDriver
import platform
import glob
import socket
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
			
application = Flask(__name__)

@application.route("/", methods=['POST'])
def scrapper():
	selector = request.values.get('selector')
	url = request.values.get('url')
	custom_trigger_param = request.values.get('custom_trigger_param')
	try:
		if selector is None:
			return json.dumps({"data": "1 - not ValidQuery Folk!"})
		elif url is None:
			return json.dumps({"data": "2 - not ValidQuery Folk!"})
		elif custom_trigger_param is None:
			return json.dumps({"data": "3 - not ValidQuery Folk!"})
		else:
			
			dcap = dict(DesiredCapabilities.PHANTOMJS)
			dcap["phantomjs.page.settings.userAgent"] = (
				"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
				"(KHTML, like Gecko) Chrome/15.0.87"
			)
			path_phantom = r'H:\phantomjs\bin\phantomjs.exe'
			path_phantom2 = r'/usr/libexec/s2i/assemble/phantomjs-1.1.4'
			path_phantom3 = r"/usr/bin/phantomjs"
			path_phantom4 = os.path.join('./phantomjs.exe')
			path_phantom5 = os.path.join('/opt/app-root/src/phantomjs/bin/phantomjs')
			os.chmod('/opt/app-root/src/phantomjs/bin/phantomjs', 755)
			port = 0
			hostname = socket.gethostname() 
			ip = socket.gethostbyname(hostname)
			#ip = 'http://10.130.16.26'
			#oc rsync C:\path to where is phantomjs file folder in\ os-sample-python-85cd747f5-pmfpx:/app-root/ --no-perms
			driver = MyPhantomWebDriver(executable_path=path_phantom5, ip=ip, port=port, desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true'])

			#driver = webdriver.PhantomJS(executable_path=path_phantom4, service_args=['--ignore-ssl-errors=true'],desired_capabilities=dcap)
#phantomPath: require('path').dirname(process.env.PHANTOMJS_EXECUTABLE) + '/'
			#url='https://www.oddsportal.com/basketball/germany/bbl/results/'

			driver.get(url)
			timeout = 10;
			wait = WebDriverWait(driver, timeout)
			if selector.find('#') > -1:
				selector = selector.replace('#','[@id="')+'"]';
			
			mensaje = 'scrapper ' + selector + ' in ' + url + ' ! '
			print('mensaje '+mensaje)
			result = wait.until(EC.presence_of_element_located((By.XPATH, '//'+selector)))
			#print(result.get_attribute("outerHTML"))
			return json.dumps([{"data": str(result.get_attribute("outerHTML"))}])
	except Exception as e:
		return json.dumps([{"error": str(e)}])
		
@application.route("/", methods=['GET'])
def hello():
	try:
		#ip = socket.gethostbyname(hostname)
		hostname = socket.gethostname() 
		ip = socket.gethostbyname(hostname)
		message = os.path.abspath(__file__)
		message += ' '+platform.system()+' '+platform.release()+' Hostname: '+ hostname+ '\n' 'IP: '+ ip+' |||||||   '
		dirpath = os.getcwd()
		path = "../"
		#message = " - "
		for root,d_names,f_names in os.walk(path):
			for f in f_names:
				message +=os.path.join(root, f)+" ............"+ os.linesep

		#path = "/"#root of C
		#foldername = os.path.basename(dirpath)
		return message
		#return message+" current directory is : " + dirpath+ " Directory name is : " + foldername
	except Exception as e:
		return json.dumps([{"error": str(e)}])
	
if __name__ == "__main__":
    application.run()

#oc rsh os-sample-python-85cd747f5-pmfpx
#oc rsync ./files os-sample-python-85cd747f5-pmfpx:/src
#oc rsync C:\Users\IVAN\Documents\PythonPrograms\openshift\os-sample-python\files os-sample-python-85cd747f5-pmfpx:/src
#oc rsync --token=Yad_spcjq_U6_Tps4NYs0TR5jhKnds4JHqUJvWjaKaI C:\Users\IVAN\Documents\PythonPrograms\openshift\os-sample-python\files\ os-sample-python-85cd747f5-pmfpx:/ --no-perms
#oc rsync --insecure-skip-tls-verify=true --token=Yad_spcjq_U6_Tps4NYs0TR5jhKnds4JHqUJvWjaKaI C:\Users\IVAN\Documents\PythonPrograms\openshift\os-sample-python\files\ os-sample-python-85cd747f5-pmfpx:/ --no-perms
#oc rsync  --no-perms --insecure-skip-tls-verify=true --token=Yad_spcjq_U6_Tps4NYs0TR5jhKnds4JHqUJvWjaKaI C:\Users\IVAN\Documents\PythonPrograms\openshift\os-sample-python\phantomjs\bin\ os-sample-python-d4686d8ff-9rqh7:/opt/app-root/phantomjs/bin/
