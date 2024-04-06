from webbot import Browser
from selenium.webdriver.support.ui import Select
import argparse
import time
import json
import datetime
import moodle
from os.path import join
import os
import shutil
import zipfile
import moss
import glob
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import subprocess
from loguru import logger
import builtins

# Save the original print function
original_print = print

# Override the print function
def print(*args, **kwargs):
    # Convert the print arguments into a string
    output = ' '.join(str(arg) for arg in args)
    # Use logger.info to log the message
    logger.opt(depth=1).info(output)

# Replace the built-in print with your custom function
builtins.print = print

def getDownLoadedFileName(web, waitTime):
    driver = web.driver
    driver.execute_script("window.open()")
    # switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    # navigate to chrome downloads
    driver.get('chrome://downloads')
    # define the endTime
    endTime = time.time()+waitTime
    while True:
        downloadPercentage = None
        try:
            # get downloaded percentage
            downloadPercentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
        except:
            pass
        try:
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100 or downloadPercentage is None:
                # return the file name once the download is completed
                res = driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
                return res
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break

def find_first_number_in_string(s):
    import re
    match = re.search(r'\d+', s)
    return int(match.group()) if match else None

def encode_lesson(s):
    num = find_first_number_in_string(s)
    if "Бонус" in s:
        return f"b{num}"
    else:
        return f"{num}"

parser = argparse.ArgumentParser(description='Download')
parser.add_argument('lesson', type=str,
                    help='Lesson to change')
parser.add_argument('json', type=str,
                    help='Deadline config')
parser.add_argument('-u', type=str, default=None,
                    help='User name')
parser.add_argument('-p', type=str, default=None,
                    help='Password')
parser.add_argument('--git', action='store_true',
                    help='Download submitions from git')

args = parser.parse_args()

course_data = None
with open(args.json, 'tr', encoding='utf-8-sig') as f:
    course_data = json.load(f)

web = moodle.open_login(args.u, args.p)

web.go_to(course_data['course'])
lid = moodle.get_assignm_id(web, args.lesson)
args.lesson = args.lesson.replace(':', '')
time.sleep(1.0)

credfile = 'credentials.json'
if os.path.isfile(credfile):
  with open(credfile, 'tr', encoding='utf-8-sig') as f:
    cred = json.load(f)

groups = course_data['groups']

print('Download submissions..')
def download_and_extract(group, ex_to):
    web.go_to(moodle.download_answers.format(lid, group))
    df = getDownLoadedFileName(web, 12*3600)
    df_t = join(course_data['data_folder'], df)
    shutil.move(join(cred['download_folder'], df), df_t)
    with zipfile.ZipFile(df_t,"r") as zip_ref:
        zip_ref.extractall(join(course_data['data_folder'], ex_to))
    os.remove(df_t)

moss_loc = join(args.lesson, 'moss')

if args.git:
    print("Using git")
    
    download_git_all = f'{cred["classroom_downloader"]} -s -n {encode_lesson(args.lesson)} -a 1 -o \"{join(course_data["data_folder"], moss_loc)}\" -p --no-new-path'
    print(download_git_all)
    subprocess.call(download_git_all)
    
    download_git_my = f'{cred["classroom_downloader"]} -s -n {encode_lesson(args.lesson)} -a 3 -r Волошин -o \"{join(course_data["data_folder"], args.lesson)}\" -p --no-new-path'
    print(download_git_my)
    subprocess.call(download_git_my)
else:
    download_and_extract('0', moss_loc)

    for g in groups:
        download_and_extract(groups[g]['group'], args.lesson)

print('Download assign..')
web.go_to(moodle.assign_options.format(lid))
forms = list(map(lambda x: x.get_attribute("innerHTML") , web.driver.find_elements_by_class_name("editor_atto_content")))
with open('task_template.html', 'r', encoding='utf-8-sig') as f:
    tt = f.read()
with open(join(course_data['data_folder'], args.lesson, 'task.html'), 'w', encoding='utf-8-sig') as f:
    f.write(tt.format(''.join(forms)))
    
print('Set offline grading to on..')
web.click('Развернуть всё')
checker = web.driver.find_element_by_name("assignfeedback_offline_enabled")
actions = ActionChains(web.driver)
if not checker.is_selected():
    actions.move_to_element(checker).perform()
    checker.click()
web.click('Сохранить и показать')

# Download grades
print('Download grades..')
files = []
for g in groups:
    web.go_to(moodle.download_grades.format(lid, groups[g]['group']))
    df = getDownLoadedFileName(web, 100)
    join(cred['download_folder'], df)
    files.append(df)

table = pd.concat(list(map(lambda x: pd.read_csv(join(cred['download_folder'], x), sep=','), files)), ignore_index=True)
table.sort_values(by=['Полное имя']).to_csv(join(course_data['data_folder'], args.lesson, 'score.csv'), sep=',', encoding='utf-8-sig', index=False)
for df in files:
    os.remove(join(cred['download_folder'], df))

# Assign cfg
print('Create assign cfg..')
assign_cfg = {}
assign_cfg['max_score'] = float(table['Максимальная оценка'][0].replace(',', '.'))
assign_cfg['IDE'] = course_data['IDE']
assign_cfg['lesson_id'] = lid
with open(join(course_data['data_folder'], args.lesson, 'assign.json'), 'w', encoding='utf-8-sig') as f:
    json.dump(assign_cfg, f)

# Fix names
print('Fix names..')

for f in list(glob.glob(join(course_data['data_folder'], args.lesson, '**/', '*'), recursive = True))[::-1]:
    fbase = os.path.basename(os.path.abspath(f))
    fparent = os.path.abspath(join(f, '..'))
    if fbase == args.lesson:
        continue
    os.rename(f, join(fparent, fbase.replace(' ', '_')))

web.driver.quit()

# Extract inner archs
print('Extract inner archs..')
archs = list(glob.glob(join(course_data['data_folder'], args.lesson, '**\\*.zip'), recursive = True)) + list(glob.glob(join(course_data['data_folder'], args.lesson, '**\\*.7z'), recursive = True)) + list(glob.glob(join(course_data['data_folder'], args.lesson, '**\\*.rar'), recursive = True))
for f in archs:
    d = os.path.splitext(f)[0]
    subprocess.call(' '.join(['7z', 'x', '"' + f + '"', '-o"' + d + '"']), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

# Create Scripts
print('Create Scripts..')
cmd = 'cd ' + os.path.dirname(cred['check_moodle']) + "\n" + cred['check_moodle'] + ' "' + join(course_data['data_folder'], args.lesson) + '"'
cmd = cmd.replace('/', '\\')
with open(join(course_data['data_folder'], args.lesson, 'check_moodle.bat'), 'w', encoding='cp866') as f:
    f.write(cmd)

cmd = 'cd ' + os.path.abspath('.') + "\npython " + os.path.abspath('.\\collect_and_send.py') + ' "' + join(course_data['data_folder'], args.lesson) + '"'
cmd = cmd.replace('/', '\\')
with open(join(course_data['data_folder'], args.lesson, 'collect_and_send.bat'), 'w', encoding='cp866') as f:
    f.write(cmd)

# Prepare Moss
for fext in course_data['fexts']:
    mfp = join(course_data['data_folder'], moss_loc)
    for subd in glob.glob(join(mfp, '*\\')):
        outpf = join(subd, 'moss_to_send' + os.path.splitext(fext)[1])
        text = ''
        for prog in glob.glob(join(glob.escape(subd), '**', fext), recursive=True):
            if os.path.isfile(prog):
                try:
                    with open(prog, 'r', encoding='utf-8-sig') as f:
                        text += '>' * 10 + '\n'
                        text += '>>> ' + prog + '\n'
                        text += f.read() + '\n'
                except:
                    with open(prog, 'r', encoding='cp1251') as f:
                        text += '>' * 10 + '\n'
                        text += '>>> ' + prog + '\n'
                        text += f.read() + '\n'
        with open(outpf, 'w', encoding='utf-8-sig') as f:
            f.write(text)

# Moss

print('Running moss...')
moss_args = moss.load_args()
logger.debug(f'Moss args: {moss_args}')

moss_args['files'] = [join(course_data['data_folder'], moss_loc, '*', 'moss_to_send' + os.path.splitext(f)[1]) for f in course_data['fexts']]
moss_args['l'] = course_data['l']
logger.debug(f'Changed moss args: {moss_args}')
url = moss.call_moss(**moss_args)
logger.debug(f'Moss url: {url}')
print('Sorting...')
page, sortedtable = moss.sort_moss(url)
print('done.')
print('Creating report')
moss.report_moss(page, sortedtable, url)
shutil.move(moss.report(), join(course_data['data_folder'], moss_loc, moss.report()))
print('done')
print(os.path.abspath(join(moss_loc, moss.report())))

sources = list(map(lambda x: x.split(), sortedtable['Source'].values))
compared = list(map(lambda x: x.split(), sortedtable['Compared'].values))
urls = list(sortedtable['URL'].values)
sources = list(zip(sources, urls))
compared = list(zip(compared, urls))
plags = sources + compared

d = {}
for ([f, p], url) in plags:
    if f not in d:
        d[f] = { 'percent': -1, 'url': ''}
    if f in d:
        v = int(p[1:-2])
        if v > d[f]['percent']:
            d[f]['percent'] = v
            d[f]['url'] = url

for k in d:
    tod = join(course_data['data_folder'], args.lesson, k)
    if os.path.isdir(tod):
        tof = join(tod, 'moss.json')
        with open(tof, 'w') as f:
            json.dump(d[k], f)

subprocess.call(join(course_data['data_folder'], args.lesson, 'check_moodle.bat'))
