from flask import Flask
from flask import request
import json
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import glob

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
			driver = webdriver.PhantomJS(executable_path=path_phantom2, service_args=['--ignore-ssl-errors=true'],desired_capabilities=dcap)
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
		dirpath = os.getcwd()
		path = "./"
		message = " - "
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
