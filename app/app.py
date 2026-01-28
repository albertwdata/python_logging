# %%
# import modules
import logging
import config.logging_config as l_cfg
import datetime


# %%
# run main
def main():

    startup_dt = datetime.datetime.now()

    # configure logging
    l_cfg.configure_logging(
        app_name_str='app',
        log_name_str='app_main_log',
        log_dt=startup_dt
    )

    # call app logger
    app_logger = logging.getLogger('app')

    # test levels
    app_logger.debug('debug message')
    app_logger.info('info message')
    app_logger.warning('warning message')
    app_logger.error('error message')
    app_logger.critical('critical message')

    # test extra details
    details_dl = {
        'detail1': 'value1',
        'detail2': 'value2'
    }

    app_logger.critical('critical message with details', extra={'details': details_dl})

    # test exception and stack info
    try:
        raise ValueError('test value error')
    except ValueError:
        app_logger.exception('exception message', stack_info=True)

    # test extra details exception and stack info
    try:
        raise ValueError('test value error')
    except ValueError:
        app_logger.exception('exception message with details', stack_info=True, extra={'details':details_dl})

if __name__ == '__main__':
    main()


# %%
