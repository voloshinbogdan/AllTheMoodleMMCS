from webbot import Browser
from selenium.webdriver.support.ui import Select
import argparse
import time
import json
import datetime
import moodle

parser = argparse.ArgumentParser(description='Change deadlines on Moodle')
parser.add_argument('lesson', type=str,
                    help='Lesson to change')
parser.add_argument('date',
                    type=lambda s: datetime.datetime.strptime(s, '%d.%m.%Y'),
                    help='Day.Month.Year')
parser.add_argument('json', type=str,
                    help='Deadline config')
parser.add_argument('-u', type=str, default=None,
                    help='User name')
parser.add_argument('-p', type=str, default=None,
                    help='Password')

args = parser.parse_args()
(d, m, y) = (str(args.date.day), args.date.strftime('%B'), str(args.date.year))		

course_data = None
with open(args.json, 'tr', encoding='utf-8-sig') as f:
    course_data = json.load(f)

web = moodle.open_login(args.u, args.p)

web.go_to(course_data['course'])
if args.lesson == "?":
    assigns = moodle.get_open_assigns(web)
    assigns_names = list(map(lambda x: x.find_elements_by_css_selector("*")[0].get_attribute("data-activityname"), assigns))
    for a in assigns_names:
        print(a)
    while args.lesson not in assigns_names:
        args.lesson = input('Choose task: ')

lid = moodle.get_assignm_id(web, args.lesson)

time.sleep(1.0)
web.go_to(moodle.assign_options.format(lid))
cns = web.driver.find_element_by_id('id_availabilityconditionsheader')
web.click('Ограничение доступа')
time.sleep(1.0)
l = list(map(lambda x: (x, Select(x)), cns.find_elements_by_xpath('.//select')))

gt = course_data['groups']

inum = -1
for e in l:
    if inum > -1:
        inum += 1
    if moodle.find_elements_by_text(e[0].find_element_by_xpath('../..'),'Группа') and e[1].first_selected_option.text in gt:
        group = e[1].first_selected_option.text
        print(group)
        inum = 0
    if inum == 2 or inum == 8:
        e[1].select_by_visible_text(d)
    if inum == 3 or inum == 9:
        e[1].select_by_visible_text(m)
    if inum == 4 or inum == 10:
        e[1].select_by_visible_text(y)
    if inum == 5:
        e[1].select_by_visible_text(gt[group]['hb'])
    if inum == 6:
        e[1].select_by_visible_text(gt[group]['mb'])
    if inum == 11:
        e[1].select_by_visible_text(gt[group]['he'])
    if inum == 12:
        e[1].select_by_visible_text(gt[group]['me'])
        inum = -1

input('press Enter..')
web.stop_client()        