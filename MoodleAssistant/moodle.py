import json
import os
from webbot import Browser


login_link = 'https://edu.mmcs.sfedu.ru/login/index.php'
assign_options = 'https://edu.mmcs.sfedu.ru/course/modedit.php?update={0}&return=1'
download_answers = 'https://edu.mmcs.sfedu.ru/mod/assign/view.php?id={0}&group={1}&action=downloadall'
download_grades = 'https://edu.mmcs.sfedu.ru/mod/assign/view.php?id={0}&group={1}&plugin=offline&pluginsubtype=assignfeedback&action=viewpluginpage&pluginaction=downloadgrades'
upload_grades = 'https://edu.mmcs.sfedu.ru/mod/assign/view.php?id={0}&plugin=offline&pluginsubtype=assignfeedback&action=viewpluginpage&pluginaction=uploadgrades'

def open_login(username, password, credfile = 'credentials.json'):
  web = Browser()
  if username is None or password is None:
    if os.path.isfile(credfile):
      with open(credfile, 'tr', encoding='utf-8-sig') as f:
        cred = json.load(f)
        username = cred['username']
        password = cred['password']
    else:
      raise "Can't get credentials"
   
  web.go_to(login_link)
  web.type(username, into='Username')
  web.type(password, into='Password')
  web.click('Log in')
  return web


def find_elements_by_text(el, text):
  return el.find_elements_by_xpath(".//*[contains(text(),'"+text+"')]")


def get_open_assigns(web):
  rgm = web.driver.find_element_by_id('region-main')
  assigns = rgm.find_elements_by_class_name('assign')
  assigns_open = filter(lambda x: not x.find_elements_by_class_name('badge'), assigns)
  return list(assigns_open)


def get_assignm_id(web, lesson):
  rgm = web.driver.find_element_by_id('region-main')
  assigns = rgm.find_elements_by_class_name('assign')
  assigns_open = filter(lambda x: not x.find_elements_by_class_name('badge'), assigns)
  fa = list(filter(lambda x: find_elements_by_text(x, lesson), assigns_open))
  fa[0].get_attribute('data-id')
  return fa[0].get_attribute('data-id')
