import os
import sys

try:
    from .settings import *
except SystemError:
    from scripts.settings import *


supervisor_config_dir = 'supervisor_include'

current_path = sys.path[0]

script_file = os.path.join(current_path, 'exo_script.py')

exo_engine_log_directory = ''
exo_script_log_value = 'AUTO'  # AUTO, NONE or path to directory

supervisor_conf_template = """
[program:EXO_{instrument}]
command=python3.5 {script_file} --debug={log_directory} {instrument}
stdout_logfile={log_value}
directory={current_path}
"""


# Create supervisor config dir
if not os.path.exists(os.path.join(current_path, supervisor_config_dir)):
    os.mkdir(os.path.join(current_path, supervisor_config_dir))

for instr in INSTRUMENTS_LIST:
    file_contents = supervisor_conf_template.format(**{
            'instrument': instr,
            'script_file': script_file,
            'log_directory': exo_engine_log_directory,
            'log_value': exo_script_log_value,
            'current_path': current_path,
        }
    )

    file_name = 'exo_{0}.conf'.format(instr).lower()
    with open(os.path.join(current_path, supervisor_config_dir, file_name), 'w') as fh:
        fh.write(file_contents)
    print(file_contents)
