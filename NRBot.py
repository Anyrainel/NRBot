import json
import os
import shutil
import shlex
import sys
import webbrowser
import subprocess
import logging
import time
from pathlib import Path
from datetime import datetime


logger = logging.getLogger('NRBot')


def init_logger():
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s',
        datefmt='%I:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def logtime():
    return datetime.now().strftime(r'%Y%m%d%H%M%S')


def run(command, name):
    logger.info("Starting job [%s]" % name)
    logger.debug("Command: %s" % command)
    process = subprocess.Popen(
        shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    rc = process.poll()
    output = process.stdout.readline().rstrip()
    while rc is None or output:
        if output and not output.startswith('[current_line]') and not '[DEBUG]' in output:
            print(output)
        rc = process.poll()
        output = process.stdout.readline().rstrip()


def get_settings():
    if not os.path.isfile('settings.jsonc'):
        logger.error(
            'Settings are missing. Copy settings.default.jsonc to settings.jsonc and adjust.')
        return None
    logger.info("Loading settings.jsonc.")
    with open('settings.jsonc', 'r') as txt:
        builder = ""
        # Naively remove comments to avoid depending on other lib
        for linestr in txt.readlines():
            line = linestr.strip()
            if not line.startswith('//'):
                builder += line
        settings = json.loads(builder)
    return settings


def get_log_dir(rootdir, settings):
    reportdir = os.path.join(rootdir, settings['LogReportDirectory'])
    logdir = os.path.join(reportdir, logtime())
    if settings['CleanUpLogBeforeRun'] and os.path.isdir(reportdir):
        shutil.rmtree(reportdir)
    os.makedirs(logdir, exist_ok=True)
    return logdir


def make_screenshot_dir(rootdir, settings):
    reset =settings['ScriptSettings']['ResetFarming']
    ssdir = os.path.join(rootdir, reset['ScreenshotPath'])
    if reset['SaveScreenshot'] and not os.path.isdir(ssdir):
        os.makedirs(ssdir, exist_ok=True)
    return


def get_script():
    if (len(sys.argv) < 2):
        logger.error(
            'Please provide a script name! e.g. resetfarming, darkdaily, dungeon.')
        return None
    script = str(sys.argv[1]).lower()
    if script not in ["resetfarming", "darkdaily", "dungeon"]:
        logger.error(
            'Script %s is not recognized. e.g. resetfarming, darkdaily, dungeon.' % script)
        return None
    return script


def main():
    init_logger()
    script = get_script()
    if script is None:
        return
    settings = get_settings()
    if settings is None:
        return

    rootdir = Path(__file__).parent.absolute()
    airtest = os.path.join(
        settings['AirtestIDEDirectory'], 'AirtestIDE.exe')
    device = settings['DeviceAdbUrl']
    params = '&&'.join([
        'cap_method=JAVACAP',
        'ori_method=MINICAPORI',
        'touch_method=MINITOUCH',
    ])
    main = os.path.join(rootdir, '%s.air' % script)
    logdir = get_log_dir(rootdir, settings)
    make_screenshot_dir(rootdir, settings)

    run_command = '"%s" runner "%s" ' % (airtest, main)
    run_command += ' --device "%s?%s" ' % (device, params)
    run_command += ' --log "%s" ' % (logdir)
    run(run_command, 'Runner')

    if settings['ShowLogReportAfterRun']:
        loghtml = os.path.join(logdir, 'log.html')
        report_command = '"%s" reporter "%s" ' % (airtest, main)
        report_command += ' --log_root "%s" ' % logdir
        report_command += ' --outfile "%s" ' % loghtml
        run(report_command, 'Reporter')
        if os.path.isfile(loghtml):
            webbrowser.open(loghtml, new=2)
        else:
            logger.warning(
                "Cannot find log HTML, runner or reporter has errors.")
    return


if __name__ == '__main__':
    main()
