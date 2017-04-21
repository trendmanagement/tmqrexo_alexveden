import os
import subprocess
import zipfile
from datetime import datetime
from slackclient import SlackClient

OUT_DIR = '/var/data/reports/'

REPORT_SETTINGS = {
    'All_Production_Campaign': {
        'work_dir': '/var/data/notebooks/tools',
        'notebook': 'All_Production_Campaign_Settlements-Email_template.ipynb',
        'slack_channel_id': 'G4W4CEDHC',  # 'reports' channel of TMQREXO Slack
        'slack_token': "xoxb-118049439075-QjwhoyTBZlqLjJRmnjM0uT3B",
        'email_list': None,
        'type': 'html'
    },
}
"""
    'TestReport': {
            'work_dir': '/home/ubertrader/Dropbox/tmqrexo/notebooks/tools',
            'notebook': 'test_report.ipynb',
            'slack_channel_id': 'G4W4CEDHC',
            'slack_token': "xoxb-118049439075-QjwhoyTBZlqLjJRmnjM0uT3B", # Place custom BOT token here
            'email_list': None,
            'type': 'html'
        },
"""



class ReportGenerator:
    def __init__(self, settings, outdir):
        self.settings = settings
        self.out_dir = outdir

        if not os.path.exists(self.out_dir):
            raise FileNotFoundError("Output directory not exists: {0}".format(self.out_dir))



    def run_nbconvert(self, name, notebook_file, work_dir, report_type):
        if report_type == 'html':
            no_code_template_file = 'nocode.tpl'

            if not os.path.exists(work_dir):
                raise FileNotFoundError("Working directory is not exists: {0}".format(work_dir))

            notebook_file_path = os.path.join(work_dir, notebook_file)
            if not os.path.exists(notebook_file_path):
                raise FileNotFoundError("Could'n find notebook: {0}".format(notebook_file_path))

            if not os.path.exists(os.path.join(work_dir, no_code_template_file)):
                raise FileNotFoundError("Template file {0} is not found in {1}".format(no_code_template_file, work_dir))

            # Changing working directory
            os.chdir(work_dir)

            report_out_file_name = "{0}_{1}.html".format(name, datetime.now().strftime("%Y-%m-%d"))
            command = ['jupyter', 'nbconvert', '--execute', '--to=html',
                                     '--template={0}'.format(no_code_template_file),
                                     '--output-dir={0}'.format(self.out_dir),
                                     '--output={0}'.format(report_out_file_name),
                                     notebook_file]
            # Running NB convert
            result = subprocess.run(command, stderr=subprocess.PIPE)

            # Check if 'nbconvert' finished OK
            if not os.path.exists(os.path.join(self.out_dir, report_out_file_name)) or result.returncode != 0:
                raise Exception("Failed during 'jupyter nbconvert' execution. \n NBConvert output: \n{0}".format(result.stderr.decode()))

            # Changing to out directory
            os.chdir(self.out_dir)

            # Archiving file
            zip_file_name = report_out_file_name.replace('html', 'zip')
            with open(zip_file_name, 'wb') as zipfh:
                with zipfile.ZipFile(zipfh, 'w', compression=zipfile.ZIP_DEFLATED) as myzip:
                    myzip.write(report_out_file_name)

            # Removing html file
            os.remove(report_out_file_name)
            return zip_file_name
        else:
            raise NotImplementedError("Only 'html' report type supported, given: {0}".format(report_type))
        pass



    def process_reports(self):
        for rep_name, rep_dict in self.settings.items():

            try:
                print("Processing: {0}".format(rep_name))
                report_fn = self.run_nbconvert(rep_name, rep_dict['notebook'], rep_dict['work_dir'], rep_dict['type'])

                if rep_dict['slack_channel_id'] is not None:
                    slack_client = SlackClient(rep_dict['slack_token'])
                    if not slack_client.rtm_connect():
                        print("Slack: Connection Failed, invalid token?")
                        continue
                    else:
                        print("Slack: Slack engine connected")
                        slack_client.api_call(
                            "files.upload",
                            channels=rep_dict['slack_channel_id'],
                            filename=report_fn,
                            file=open(os.path.join(self.out_dir, report_fn), 'rb')
                        )
                print('Done: {0}'.format(rep_name))
            except Exception as exc:
                print("Exceptions occurred: ")
                print(str(exc))

if __name__ == '__main__':
    rg = ReportGenerator(REPORT_SETTINGS, OUT_DIR)
    rg.process_reports()