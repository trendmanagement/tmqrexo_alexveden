from flexx import app, ui, event
from backtester.swarms.swarm import Swarm
import importlib
import os
import inspect
import io
import subprocess
from datetime import datetime


def get_import_string(obj):
    m = inspect.getmodule(obj)
    if m is None or m.__name__ == 'builtins':
        return None

    if inspect.isclass(obj):
        return {'class_name': obj.__name__,
                'module': m.__name__,
                'import': "from {0} import {1}".format(m.__name__, obj.__name__)}


def dump_value(obj):
    if isinstance(obj, str):
        return "'" + obj + "'", None
    if inspect.isclass(obj):
        # Dump class instance and do imports
        return obj.__name__, get_import_string(obj)
    elif inspect.isfunction(obj):
        # Quick stub for rebalancing functions
        if 'SwarmRebalance' in obj.__qualname__:
            return obj.__qualname__, {'class_name': 'SwarmRebalance',
                                      'import': 'from backtester.swarms.rebalancing import SwarmRebalance',
                                      'module': 'backtester.swarms.rebalancing'
                                      }
        else:
            raise NotImplementedError("Only SwarmRebalance class supported for rebalance_time_function")

    elif inspect.isclass(type(obj)):
        return str(obj), get_import_string(type(obj))

    return obj, None


def context_dump(strategy_context, nrecusrion=0, key='', buff=None, strategy_suffix=''):
    imp = {}

    if buff is None:
        buff = io.StringIO()

    if isinstance(strategy_context, list):
        # Parse opt params list
        print('    ' * nrecusrion + "'" + key + "': [", file=buff)
        for v in strategy_context:
            dvalue, imports = dump_value(v)
            if imports is not None:
                imp.update({imports['class_name']: imports['import']})
            print('    ' * (nrecusrion + 1) + '{0}, '.format(dvalue), file=buff)
        print('    ' * nrecusrion + "],", file=buff)
    else:
        if key != '':
            print('    ' * nrecusrion + "'" + key + "': {", file=buff)
        else:
            print('    ' * nrecusrion + '{', file=buff);
        for k, v in strategy_context.items():
            if k == 'exo_storage':
                continue
            if isinstance(v, dict):
                imp.update(context_dump(v, nrecusrion + 1, key=k, buff=buff))
            elif isinstance(v, list):
                imp.update(context_dump(v, nrecusrion + 1, key=k, buff=buff))
            else:
                dvalue, imports = dump_value(v)
                if imports is not None:
                    imp.update({imports['class_name']: imports['import']})
                print('    ' * (nrecusrion + 1) + "'{0}': {1},".format(k, dvalue), file=buff)
        if nrecusrion == 0:
            print('    ' * nrecusrion + '}', file=buff)
        else:
            print('    ' * nrecusrion + '},', file=buff)

    if nrecusrion == 0:
        sourcebuff = io.StringIO()
        sourcebuff.write("#\n#\n#  Automatically generated file \n#        Created at: {0}\n#\n".format(datetime.now()))

        for k, v in imp.items():
            if k == '__source':
                continue
            print(v, file=sourcebuff)



        sourcebuff.write('\n\nSTRATEGY_NAME = {0}.name'.format(strategy_context['strategy']['class'].__name__))

        sourcebuff.write('\n\nSTRATEGY_SUFFIX = "{0}"'.format(strategy_suffix))

        sourcebuff.write('\n\nSTRATEGY_CONTEXT = ')
        sourcebuff.write(buff.getvalue())

        source_code = sourcebuff.getvalue()
        sourcebuff.close()
        buff.close()
        #print(source_code)
        return source_code
    return imp


class AlphaDeployer(ui.Widget):
    def __init__(self, *init_args, **kwargs):
        strategy_context = kwargs.pop('strategy_context', None)
        if strategy_context is None:
            raise ValueError("You must pass 'strategy_context' kwarg to AlphaDeployer() init.")

        self.TMQRPATH = os.getenv("TMQRPATH", '')

        if self.TMQRPATH == '':
            raise ValueError(
                "TMQRPATH environment variable is not set, add this variable and point to the path witm TMQR framework packages")

        self.strategy_suffix = kwargs.pop('strategy_suffix', '')

        self.strategy_context = strategy_context

        super().__init__(*init_args, **kwargs)

    def init(self):
        #
        # Confirmation type, if confirm dialog shown
        #
        self.confirm_type = ''

        with ui.HBox():
            with ui.VBox(flex=1):
                with ui.VBox():
                    with ui.GroupWidget(title='Deployment options'):

                        self.alphaname_label = ui.Label(text=Swarm.get_name(self.strategy_context,
                                                                            suffix=self.strategy_suffix),
                                                        )

                    with ui.VBox(style='background-color: #ff8787;') as self.confirm_panel:
                        self.confirm_label = ui.Label(text='We need your confirmation')
                        with ui.HBox():
                            self.confirm_ok = ui.Button(text='OK')
                            self.confirm_cancel = ui.Button(text='Cancel')
                    self.confirm_panel.style = 'display: none;'

                    self.btnrun = ui.Button(text='Deploy',
                                            style='display: inline;')

                ui.Widget(flex=1)

            with ui.VBox(flex=3):
                with ui.GroupWidget(flex=3, title='Deployment progress information'):
                    self.log_message = ui.Label(wrap=True,
                                                text='',
                                                style='''overflow-y: scroll;
                                                         height: 500px;
                                                         padding: 10px;
                                                         ''')

        self.btnrun.visible = False


    def _custom_alpha_filename(self):
        alpha_name = self.strategy_context['strategy']['class'].name
        direction_name = Swarm.get_direction(self.strategy_context)[1]
        return 'alpha_{0}_{1}{2}'.format(alpha_name, direction_name, self.strategy_suffix).replace('-', '_').replace(
            '.', '_').lower() + '.py'

    def _check_context_duplicates(self, exo_name, module_name):
        m = importlib.import_module('scripts.alphas.{0}.{1}'.format(exo_name, module_name.replace('.py', '')))

        existing_name = Swarm.get_name(m.STRATEGY_CONTEXT, m.STRATEGY_SUFFIX)
        current_name = Swarm.get_name(self.strategy_context, self.strategy_suffix)

        if existing_name.lower() == current_name.lower():
            self._log(
                "Alpha strategy with similar name ('{0}') already exists, try to check code of the {1} for duplicates or change STRATEGY_SUFFIX.".format(
                    existing_name,
                    'scripts.alphas.{0}.{1}'.format(exo_name, module_name)))
            return False

        self._log('Processing {0}... OK'.format(module_name))
        return True



    def _confirmation_ask(self, question, confirm_type, ok_btn_text='OK'):
        self.btnrun.style = 'display: none;'
        self.confirm_label.text = question
        self.confirm_type = confirm_type
        self.confirm_panel.style = 'display: block;'

    def _confirmation_hide(self):
        self.btnrun.style = 'display: inline;'
        self.confirm_label.text = ''
        self.confirm_panel.style = 'display: none;'

    @event.connect('confirm_ok.mouse_down')
    def _confirmation_ok_click(self, *events):
        self._confirmation_hide()
        if self.confirm_type == 'confirm_overwrite':
            exo_name = self.strategy_context['strategy']['exo_name']
            filename = os.path.join(self.TMQRPATH, 'scripts', 'alphas', exo_name.lower(), self._custom_alpha_filename())
            self._log("Rewriting the file")
            # Deleting existing file
            os.remove(filename)

            # Rerun deployment process
            self._run_deployment(*events)

    @event.connect('confirm_cancel.mouse_down')
    def _confirmation_cancel_click(self, *events):
        self.confirm_type = ''
        self._confirmation_hide()
        self._log('Cancelled.')

    def _check_errors(self):
        exo_name = self.strategy_context['strategy']['exo_name']
        filename = os.path.join(self.TMQRPATH, 'scripts', 'alphas', exo_name.lower(), self._custom_alpha_filename())
        if os.path.exists(filename):
            self._log("Script {0} with the same name already exists, overwrite?".format(self._custom_alpha_filename()))

            # Display confirmation dialog with specific action type
            self._confirmation_ask("Overwrite existing script?", 'confirm_overwrite')
            return False

        self._log("Checking custom alpha deployment for issues")

        #
        # Check if scripts directory exists
        #
        if os.path.exists(os.path.join(self.TMQRPATH, 'scripts')):
            self._log("'scripts' directory exists... OK")
        else:
            self._log("'scripts' directory not exists... FAILED")
            return False

        #
        # Check if scripts/alphas directory exists
        #
        if os.path.exists(os.path.join(self.TMQRPATH, 'scripts', 'alphas')):
            self._log("'scripts/alphas' directory exists... OK")
        else:
            self._log("'scripts/alphas' directory not exists... FAILED")
            return False

        #
        # Check if scripts/alphas/{EXO_NAME} directory exists
        #
        exo_name = self.strategy_context['strategy']['exo_name']
        if os.path.exists(os.path.join(self.TMQRPATH, 'scripts', 'alphas', exo_name.lower())):
            self._log("'scripts/alphas/{0}' directory exists... OK".format(exo_name.lower()))
            file_name = self._custom_alpha_filename()

            #
            #  Check duplicates in alpha names, which is already exists in the directory modules
            #
            for module in os.listdir(os.path.join(self.TMQRPATH, 'scripts', 'alphas', exo_name.lower())):
                # Don't check for duplicates for existing alpha file
                if module == file_name:
                    continue

                if 'alpha_' in module and '.py' in module:
                    if not self._check_context_duplicates(exo_name.lower(), module):
                        return False
            self._log("Checking existing modules for duplicates... OK")

        else:
            self._log("'scripts/alphas/{0}' directory not exists, creating....".format(exo_name.lower()))
            os.mkdir(os.path.join(self.TMQRPATH, 'scripts', 'alphas', exo_name.lower()))
            # Create empty '__init__.py' to mark new directory as python package
            open(os.path.join(self.TMQRPATH, 'scripts', 'alphas', exo_name.lower(), '__init__.py'), 'a').close()
            self._log("WARNING: You are deploying custom alpha for new SmartEXO asset, "
                      "you need manually run 'install.py' script on the server after deployment to make alphas available.")

        self._log("Sanity checks PASSED")
        return True

    def _log(self, msg):
        self.log_message.text += msg + '<br>'

    @event.connect('btnrun.mouse_down')
    def _run_deployment(self, *events):

        if self._check_errors():
            exo_name = self.strategy_context['strategy']['exo_name']
            filename = os.path.join(self.TMQRPATH, 'scripts', 'alphas', exo_name.lower(), self._custom_alpha_filename())

            #
            #  Dumping strategy setting to .py file
            #
            self._log('Writing strategy settings to: ' + os.path.join('scripts', 'alphas', exo_name.lower(),
                                                                      self._custom_alpha_filename()))
            with open(filename, 'w') as fh:
                fh.write(context_dump(self.strategy_context, strategy_suffix=self.strategy_suffix))

            #
            # Running basic syntax checks
            #
            run_result = subprocess.run(['python3.5', '-m', 'py_compile', filename],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)
            if run_result.returncode == 0:
                self._log('Checking file for syntax errors... OK')
            else:
                self._log('Syntax errors found:')
                self._log(run_result.stdout.decode().replace('\n', '<br>'))
                self._log('Checking file for syntax errors... FAILED')
                self._log("Deleting the file to avoid system corruption")
                os.remove(filename)
                return

            #
            # Running alpha rebalancer script for single file
            #
            self._log('Launching alpha rebalancing process...')
            exo_name = self.strategy_context['strategy']['exo_name']
            alpha_rebalancer_script = os.path.join(self.TMQRPATH, 'scripts', 'alpha_rebalancer_single.py')
            alpha_package = os.path.join('scripts', 'alphas', exo_name.lower(), self._custom_alpha_filename())

            run_result = subprocess.run(['python3.5', alpha_rebalancer_script, alpha_package],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)
            if run_result.returncode == 0:
                self._log(run_result.stdout.decode().replace('\n', '<br>'))
                self._log('Alpha rebalancing script finished... OK')
                self._log('Deployment completed.')
            else:
                self._log('Errors during alpha rebalancing process:')
                self._log(run_result.stdout.decode().replace('\n', '<br>'))
                self._log('Alpha rebalancing script... FAILED')
                self._log("Deleting the file to avoid system corruption")
                os.remove(filename)
                return