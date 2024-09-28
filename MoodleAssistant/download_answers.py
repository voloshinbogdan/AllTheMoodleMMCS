import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import time
import zipfile
from os.path import join

import pandas as pd
from loguru import logger
from selenium.webdriver.common.action_chains import ActionChains

import moodle
import moss
from moodle import click_text, go_to


def get_downloaded_filename(driver, wait_time):
    """
    Open the Chrome downloads page and wait for the download to finish.

    Args:
        driver: Selenium WebDriver instance.
        wait_time: Maximum time to wait in seconds.

    Returns:
        The name of the downloaded file.

    """
    driver.execute_script("window.open()")
    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])
    # Navigate to chrome downloads
    driver.get('chrome://downloads')
    end_time = time.time() + wait_time
    while True:
        download_percentage = None
        try:
            # Get download percentage
            download_percentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot"
                ".querySelector('#downloadsList downloads-item').shadowRoot"
                ".querySelector('#progress').value")
        except Exception:
            pass
        try:
            if download_percentage == 100 or download_percentage is None:
                # Return the file name once the download is completed
                res = driver.execute_script(
                    "return document.querySelector('downloads-manager').shadowRoot"
                    ".querySelector('#downloadsList downloads-item').shadowRoot"
                    ".querySelector('div#content  #file-link').text")
                return res
        except Exception:
            pass
        time.sleep(1)
        if time.time() > end_time:
            break


def find_first_number_in_string(s):
    """
    Find the first number in a string.

    Args:
        s: Input string.

    Returns:
        The first number found in the string as an integer, or None if not found.
    """
    match = re.search(r'\d+', s)
    return int(match.group()) if match else None


def encode_lesson(s):
    """
    Encode the lesson name into a specific format.

    Args:
        s: Lesson name string.

    Returns:
        Encoded lesson name.
    """
    num = find_first_number_in_string(s)
    if "Бонус" in s:
        return f"b{num}"
    else:
        return f"{num}"


def parse_arguments():
    parser = argparse.ArgumentParser(description='Download')
    parser.add_argument('lesson', type=str, help='Lesson to change')
    parser.add_argument('json', type=str, help='Deadline config')
    parser.add_argument('-u', type=str, default=None, help='User name')
    parser.add_argument('-p', type=str, default=None, help='Password')
    parser.add_argument('--git', action='store_true', help='Download submissions from git')
    return parser.parse_args()


def load_json_config(filename):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        return json.load(f)


def open_moodle(args, course_data):
    web = moodle.open_login(args.u, args.p)
    go_to(web, course_data['course'])
    lid = moodle.get_assignm_id(web, args.lesson)
    args.lesson = args.lesson.replace(':', '')
    time.sleep(1.0)
    return web, lid


def load_credentials(credfile='credentials.json'):
    if os.path.isfile(credfile):
        with open(credfile, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    else:
        return {}


def download_and_extract(web, lid, course_data, cred, group, extract_to):
    """
    Download submissions for a group and extract them.

    Args:
        web: Selenium WebDriver instance.
        lid: Assignment ID.
        course_data: Course configuration data.
        cred: Credentials data.
        group: Group ID.
        extract_to: Directory to extract submissions to.
    """
    go_to(web, moodle.DOWNLOAD_ANSWERS.format(lid, group))
    downloaded_file = get_downloaded_filename(web, 12 * 3600)
    destination_file = join(course_data['data_folder'], downloaded_file)
    shutil.move(join(cred['download_folder'], downloaded_file), destination_file)
    with zipfile.ZipFile(destination_file, "r") as zip_ref:
        zip_ref.extractall(join(course_data['data_folder'], extract_to))
    os.remove(destination_file)


def download_submissions(args, web, lid, course_data, cred):
    """
    Download submissions for all groups.

    Args:
        args: Command-line arguments.
        web: Selenium WebDriver instance.
        lid: Assignment ID.
        course_data: Course configuration data.
        cred: Credentials data.
    """
    groups = course_data['groups']
    moss_loc = join(args.lesson, 'moss')
    logger.info('Downloading submissions...')
    if args.git:
        logger.info("Using git to download submissions.")
        # Build command to download from git
        lesson_code = encode_lesson(args.lesson)
        git_command_all = f'{cred["classroom_downloader"]} -s -n {lesson_code} -a 1 -o "{join(course_data["data_folder"], moss_loc)}" -p --no-new-path'
        logger.info(f"Executing: {git_command_all}")
        subprocess.call(git_command_all)

        git_command_my = f'{cred["classroom_downloader"]} -s -n {lesson_code} -a 3 -r Волошин -o "{join(course_data["data_folder"], args.lesson)}" -p --no-new-path'
        logger.info(f"Executing: {git_command_my}")
        subprocess.call(git_command_my)
    else:
        download_and_extract(web, lid, course_data, cred, '0', moss_loc)
        for g in groups:
            download_and_extract(web, lid, course_data, cred, groups[g]['group'], args.lesson)


def download_assignment_description(web, lid, course_data, lesson):
    """
    Download the assignment description and save it to task.html.

    Args:
        web: Selenium WebDriver instance.
        lid: Assignment ID.
        course_data: Course configuration data.
        lesson: Lesson name.
    """
    logger.info('Downloading assignment description...')
    go_to(web, moodle.ASSIGN_OPTIONS.format(lid))
    forms = [element.get_attribute("innerHTML") for element in web.find_elements_by_class_name("editor_atto_content")]
    with open('task_template.html', 'r', encoding='utf-8-sig') as f:
        task_template = f.read()
    task_content = task_template.format(''.join(forms))
    task_file = join(course_data['data_folder'], lesson, 'task.html')
    with open(task_file, 'w', encoding='utf-8-sig') as f:
        f.write(task_content)


def enable_offline_grading(web, lid):
    """
    Enable offline grading in the assignment settings.

    Args:
        web: Selenium WebDriver instance.
        lid: Assignment ID.
    """
    logger.info('Enabling offline grading...')
    go_to(web, moodle.ASSIGN_OPTIONS.format(lid))
    click_text(web, 'Развернуть всё')
    checker = web.find_element_by_name("assignfeedback_offline_enabled")
    actions = ActionChains(web)
    if not checker.is_selected():
        actions.move_to_element(checker).perform()
        checker.click()
    click_text(web, 'Сохранить и показать')


def download_grades(web, lid, course_data, cred, lesson):
    """
    Download grades for all groups and save them into a single CSV file.

    Args:
        web: Selenium WebDriver instance.
        lid: Assignment ID.
        course_data: Course configuration data.
        cred: Credentials data.
        lesson: Lesson name.
    """
    logger.info('Downloading grades...')
    groups = course_data['groups']
    files = []
    for g in groups:
        go_to(web, moodle.DOWNLOAD_GRADES.format(lid, groups[g]['group']))
        downloaded_file = get_downloaded_filename(web, 100)
        full_path = join(cred['download_folder'], downloaded_file)
        files.append(full_path)
    time.sleep(1)
    data_frames = [pd.read_csv(f, sep=',') for f in files]
    table = pd.concat(data_frames, ignore_index=True)
    table.sort_values(by=['Полное имя']).to_csv(
        join(course_data['data_folder'], lesson, 'score.csv'), sep=',', encoding='utf-8-sig', index=False)
    for f in files:
        os.remove(f)
    return table


def create_assign_config(course_data, table, lesson, lid):
    """
    Create assign.json configuration file.

    Args:
        course_data: Course configuration data.
        table: DataFrame containing grades.
        lesson: Lesson name.
        lid: Assignment ID.
    """
    logger.info('Creating assign configuration...')
    assign_cfg = {
        'max_score': float(table['Максимальная оценка'].iloc[0].replace(',', '.')),
        'IDE': course_data['IDE'],
        'lesson_id': lid,
    }
    assign_cfg_path = join(course_data['data_folder'], lesson, 'assign.json')
    with open(assign_cfg_path, 'w', encoding='utf-8-sig') as f:
        json.dump(assign_cfg, f)


def fix_names(course_data, lesson):
    """
    Replace spaces with underscores in filenames.

    Args:
        course_data: Course configuration data.
        lesson: Lesson name.
    """
    logger.info('Fixing names...')
    lesson_folder = join(course_data['data_folder'], lesson)
    files = list(glob.glob(join(lesson_folder, '**', '*'), recursive=True))[::-1]
    for f in files:
        fbase = os.path.basename(f)
        fparent = os.path.dirname(f)
        if fbase == lesson:
            continue
        new_name = fbase.replace(' ', '_')
        os.rename(f, join(fparent, new_name))


def extract_inner_archives(course_data, lesson):
    """
    Extract inner archives in the submissions.

    Args:
        course_data: Course configuration data.
        lesson: Lesson name.
    """
    logger.info('Extracting inner archives...')
    lesson_folder = join(course_data['data_folder'], lesson)
    archive_extensions = ['*.zip', '*.7z', '*.rar']
    archive_files = []
    for ext in archive_extensions:
        archive_files.extend(glob.glob(join(lesson_folder, '**', ext), recursive=True))
    logger.info('  Start extracting')
    for f in archive_files:
        logger.info(f'    Extracting {f}')
        destination_dir = os.path.splitext(f)[0]
        extract_command = ['7z', 'x', f'"{f}"', f'-o"{destination_dir}"', '-aou']
        subprocess.call(' '.join(extract_command), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)


def create_scripts(course_data, lesson, cred):
    """
    Create batch scripts for checking moodle submissions and collecting results.

    Args:
        course_data: Course configuration data.
        lesson: Lesson name.
        cred: Credentials data.
    """
    logger.info('Creating scripts...')
    check_moodle_script = (
        f'cd {os.path.dirname(cred["check_moodle"])}\n'
        f'{cred["check_moodle"]} "{join(course_data["data_folder"], lesson)}"'
    )
    check_moodle_script = check_moodle_script.replace('/', '\\')
    with open(join(course_data['data_folder'], lesson, 'check_moodle.bat'), 'w', encoding='cp866') as f:
        f.write(check_moodle_script)

    collect_and_send_script = (
        f'cd {os.path.abspath(".")}\n'
        f'python {os.path.abspath("./collect_and_send.py")} "{join(course_data["data_folder"], lesson)}"'
    )
    collect_and_send_script = collect_and_send_script.replace('/', '\\')
    with open(join(course_data['data_folder'], lesson, 'collect_and_send.bat'), 'w', encoding='cp866') as f:
        f.write(collect_and_send_script)


def prepare_moss_submissions(course_data, moss_loc):
    """
    Prepare submissions for moss analysis.

    Args:
        course_data: Course configuration data.
        moss_loc: Path to moss submissions.
    """
    logger.info('Preparing moss submissions...')
    for fext in course_data['fexts']:
        moss_folder = join(course_data['data_folder'], moss_loc)
        student_dirs = glob.glob(join(moss_folder, '*\\'))
        for sub_dir in student_dirs:
            output_file = join(sub_dir, 'moss_to_send' + os.path.splitext(fext)[1])
            text = ''
            program_files = glob.glob(join(sub_dir, '**', fext), recursive=True)
            for prog in program_files:
                if os.path.isfile(prog):
                    try:
                        with open(prog, 'r', encoding='utf-8-sig') as f:
                            code = f.read()
                    except UnicodeDecodeError:
                        with open(prog, 'r', encoding='cp1251') as f:
                            code = f.read()
                    text += '>' * 10 + '\n'
                    text += f'>>> {prog}\n'
                    text += code + '\n'
            with open(output_file, 'w', encoding='utf-8-sig') as f:
                f.write(text)


def run_moss_analysis(course_data, moss_loc, lesson):
    """
    Run moss plagiarism detection and process results.

    Args:
        course_data: Course configuration data.
        moss_loc: Path to moss submissions.
        lesson: Lesson name.
    """
    logger.info('Running moss...')
    moss_args = moss.load_args()
    logger.debug(f'Moss args: {moss_args}')

    moss_args['files'] = [
        join(course_data['data_folder'], moss_loc, '*', 'moss_to_send' + os.path.splitext(f)[1])
        for f in course_data['fexts']
    ]
    moss_args['l'] = course_data['l']
    logger.debug(f'Changed moss args: {moss_args}')
    url = moss.call_moss(**moss_args)
    logger.debug(f'Moss url: {url}')
    logger.info('Sorting moss results...')
    page, sorted_table = moss.sort_moss(url)
    logger.info('done.')
    logger.info('Creating moss report...')
    moss.report_moss(page, sorted_table, url)
    moss_report_path = join(course_data['data_folder'], moss_loc, moss.report())
    shutil.move(moss.report(), moss_report_path)
    logger.info('Moss report created.')

    # Process moss results
    sources = [x.split() for x in sorted_table['Source'].values]
    compared = [x.split() for x in sorted_table['Compared'].values]
    urls = list(sorted_table['URL'].values)
    plags = list(zip(sources, urls)) + list(zip(compared, urls))

    plagiarism_data = {}
    for ([filename, percent], url) in plags:
        if filename not in plagiarism_data:
            plagiarism_data[filename] = {'percent': -1, 'url': ''}
        percent_value = int(percent[1:-2])
        if percent_value > plagiarism_data[filename]['percent']:
            plagiarism_data[filename]['percent'] = percent_value
            plagiarism_data[filename]['url'] = url

    # Save moss results into moss.json per student
    lesson_folder = join(course_data['data_folder'], lesson)
    for filename, data in plagiarism_data.items():
        student_dir = join(lesson_folder, filename)
        if os.path.isdir(student_dir):
            moss_json_path = join(student_dir, 'moss.json')
            with open(moss_json_path, 'w') as f:
                json.dump(data, f)


def run_check_moodle(course_data, lesson):
    """
    Run the check_moodle.bat script.

    Args:
        course_data: Course configuration data.
        lesson: Lesson name.
    """
    logger.info('Running check_moodle script...')
    script_path = join(course_data['data_folder'], lesson, 'check_moodle.bat')
    subprocess.call(script_path)


def main():
    args = parse_arguments()
    course_data = load_json_config(args.json)
    cred = load_credentials()
    web, lid = open_moodle(args, course_data)

    download_submissions(args, web, lid, course_data, cred)
    download_assignment_description(web, lid, course_data, args.lesson)
    enable_offline_grading(web, lid)
    table = download_grades(web, lid, course_data, cred, args.lesson)
    create_assign_config(course_data, table, args.lesson, lid)
    fix_names(course_data, args.lesson)
    extract_inner_archives(course_data, args.lesson)
    create_scripts(course_data, args.lesson, cred)

    moss_loc = join(args.lesson, 'moss')
    prepare_moss_submissions(course_data, moss_loc)
    run_moss_analysis(course_data, moss_loc, args.lesson)
    run_check_moodle(course_data, args.lesson)
    web.quit()


if __name__ == "__main__":
    main()
