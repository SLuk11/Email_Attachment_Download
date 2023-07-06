import time
import controllers
import logger as log
from configs import read_config as config


if __name__ == '__main__':
    ## performance counter timing parts
    tic = time.perf_counter()

    # read config
    config.read_config()

    log.logs_dir_check(config.shipping_mail['log_dir'])
    log.write_log('bulk_mail: process start')

    # Directory check
    controllers.dir_check(config.shipping_mail['downloads_dir'], config.shipping_mail['data_dir'])

    ## read email and Excel file
    attachment_data = controllers.get_email_attachment(config.Azure_app['tenant_id']
                                                       , config.Azure_app['app_id']
                                                       , config.Azure_app['app_secret']
                                                       , config.Azure_app['app_scope']
                                                       , config.Azure_app['mail_user']
                                                       , config.Azure_app['api_endpoint']
                                                       , config.Azure_app['request_params']
                                                       , config.shipping_mail['sender_email_lsit']
                                                       , config.shipping_mail['subject_key']
                                                       , config.shipping_mail['downloads_dir'])

    ## write json data file
    if len(attachment_data) > 0:
        controllers.write_json_data(attachment_data, config.shipping_mail['data_dir'])

    else:
        log.write_log('create_data_json: Do NOT have attachment data')

    ## performance counter timing parts
    toc = time.perf_counter()
    log.write_log(f'bulk_mail: process end in {toc - tic:0.4f} seconds')
