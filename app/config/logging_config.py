# %%
# import modules
import datetime
import logging
import json
import pathlib
import sys


# %%
# format timestamp for log record
def format_timestamp_for_log(ts: float):
    return datetime.datetime.fromtimestamp(
        ts,
        datetime.UTC
    ).strftime('%Y-%m-%dT%H:%M:%S.%f%z')


# create stdout formatter class
class StdOutFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):

        log_li = [
            format_timestamp_for_log(record.created),
            'logger: ' + record.name,
            'module: ' + record.module,
            'function: ' + record.funcName,
            record.levelname,
            record.getMessage()
        ]

        log_str = ' - '.join(log_li)

        if hasattr(record, 'details'):
            log_str += '\n\n' + json.dumps(record.details, indent=4)

        if record.exc_info is not None:
            log_str += '\n\n' + self.formatException(record.exc_info)

        if record.stack_info is not None:
            log_str += '\n\n' + self.formatStack(record.stack_info)

        return log_str


# %%
# create json formatter class
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):

        log_dl = {
            'time': format_timestamp_for_log(record.created),
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'level': record.levelname,
            'message': record.getMessage()
        }

        if hasattr(record, 'details'):
            log_dl['details'] = record.details

        if record.exc_info is not None:
            log_dl['exception_info'] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            log_dl['stack_info'] = self.formatStack(record.stack_info)

        log_json = json.dumps(log_dl)

        return log_json


# %%
# create logs folder
def create_logs_folder(app_name_str):

    logs_folder = pathlib.Path().home().joinpath(f'.{app_name_str}', 'logs')

    # if statement is not required since exist_ok=True
        # mkdir will not overwrite when exist_ok=True
    if not logs_folder.exists():
        logs_folder.mkdir(parents=True, exist_ok=True)

    return logs_folder


# %%
# create log filename
def create_log_filename(log_name_str, log_dt):
    log_dt_str = log_dt.strftime('%Y-%m-%d_%H-%M-%S%z')

    return f'{log_name_str}_{log_dt_str}.log.jsonl'


# %%
# create file handler
def create_file_handler(logs_folder, log_filename, formatter):

    file_handler = logging.FileHandler(
        filename=logs_folder.joinpath(log_filename),
        mode='a',
        encoding='utf8'
    )

    file_handler.setFormatter(formatter)

    return file_handler


# %%
# remove old logs
def remove_old_logs(logs_folder, logs_count_limit):
    logs_li = list(logs_folder.glob('*.log*'))

    over_limit_count = len(logs_li) - logs_count_limit

    if over_limit_count > 0:
        logs_li.sort()
        for log_file in logs_li[0:over_limit_count]:
            log_file.unlink()


# %%
# configure logging
def configure_logging(app_name_str, log_name_str, log_dt):
    # stdout
    stdout_formatter = StdOutFormatter()
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(stdout_formatter)

    # log file
    json_formatter = JsonFormatter()
    logs_folder = create_logs_folder(app_name_str)
    log_filename = create_log_filename(log_name_str, log_dt)
    file_handler = create_file_handler(logs_folder, log_filename, json_formatter)
    remove_old_logs(logs_folder,4)

    # root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(file_handler)

    # app logger
    app_logger = logging.getLogger('app')
    app_logger.setLevel(logging.DEBUG)


# %%
