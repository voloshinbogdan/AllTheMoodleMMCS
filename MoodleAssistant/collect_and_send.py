import moodle
from moodle import click_text, go_to
import os
import json
from os.path import join
import argparse
import pandas as pd
import glob
import time
from selenium.webdriver.common.action_chains import ActionChains

parser = argparse.ArgumentParser(description='Send')
parser.add_argument('path', type=str,
                    help='Folder with data to send')

args = parser.parse_args()

path = args.path

with open(join(path, 'assign.json'), 'r', encoding='utf-8-sig') as f:
    params = json.load(f)

# Collect
table = pd.read_csv(join(path, 'score.csv'), sep=',', index_col='Идентификатор')
table['Отзыв в виде комментария'] =  table['Отзыв в виде комментария'].astype(str)
table['Отзыв в виде комментария'] = ""
 
submissions = list(filter(lambda x: 'assignsubmission' in x, glob.glob(join(path, '*'), recursive = False)))

for p in submissions:
    scp = join(p, 'score.json')
    if os.path.exists(scp):
        with open(scp, 'r', encoding='utf-8-sig') as f:
            sc = json.load(f)
        if not 'git' in os.path.basename(p):
            ident = 'Участник' + list(filter(lambda x: x != '', os.path.basename(p).split('_')))[-3]
            table.loc[ident, 'Оценка'] = sc['score']
            table.loc[ident, 'Отзыв в виде комментария'] = sc['comment']
        else:
            name = ' '.join(os.path.basename(p).split('_')[1:-3])
            index = table[table["Полное имя"] == name].index.min()
            table.at[index, 'Оценка'] = sc['score']
            table.at[index, 'Отзыв в виде комментария'] = sc['comment']

table.to_csv(join(path, 'score_tmp.csv'), sep=',', encoding='utf-8-sig')

# Send
web = moodle.open_login(None, None)
go_to(web, moodle.UPLOAD_GRADES.format(params['lesson_id']))

time.sleep(0.5)
click_text(web, ' Разрешить обновление записей, которые были изменены в Moodle раньше, чем в ведомости.')
time.sleep(0.5)
click_text(web, 'Выберите файл')
time.sleep(0.5)
inps = web.find_element_by_name('repo_upload_file')
time.sleep(0.5)
inps.send_keys(join(path, 'score_tmp.csv'))
time.sleep(0.5)
click_text(web, 'Загрузить этот файл')
time.sleep(0.5)
submit_btn = web.find_element_by_xpath(f"//*[@name='submitbutton']")
ActionChains(web).move_to_element(submit_btn).perform()
submit_btn.click()
