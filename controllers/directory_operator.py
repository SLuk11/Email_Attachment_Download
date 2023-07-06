import os
import uuid
import json
import datetime
import logger as log


def dir_check(downloads_dir, data_dir):
    try:
        # Check if downloads_dir folder exist or not, if not create a new one
        if not os.path.exists(downloads_dir):
            os.mkdir(downloads_dir)

        # Check if data_dir folder exist or not, if not create a new one
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

    except Exception as e:
        log.write_log('dir_check: {}'.format(e.args[0]))


def create_batch_id():
    return uuid.uuid4()


def write_json_data(attachment_data, data_dir):
    try:
        # Create attachment dictionary
        xlsx_dict = []
        pdf_dict = []

        for file in attachment_data: #[Sender, 'Subject', 'OriginalFileName', 'FileName', 'Extension', 'Size', 'ReceiveDate', 'Created']
            # Create attachment data dictionary
            data_dict = {
                'Sender': file[0],
                'Subject': file[1],
                'OriginalFileName': file[2],
                'FileName': file[3],
                'Extension': file[4],
                'Size': file[5],
                'ReceiveDate': file[6],
                'Created': file[7]
            }
            if data_dict['Extension'] == 'xlsx':
                xlsx_dict.append(data_dict)
            elif data_dict['Extension'] == 'pdf':
                pdf_dict.append(data_dict)

        # write xlsx data json file
        xlsx_obj = json.dumps(xlsx_dict, indent=8)
        now = datetime.datetime.now()
        with open("{}/XLSX_{}.json".format(data_dir,
                                           now.strftime('%Y%m%d%H%M%S')), "a") as outfile:
            outfile.write(xlsx_obj)

        # write paf data json file
        pdf_obj = json.dumps(pdf_dict, indent=8)
        now = datetime.datetime.now()
        with open("{}/PDF_{}.json".format(data_dir,
                                          now.strftime('%Y%m%d%H%M%S')), "a") as outfile:
            outfile.write(pdf_obj)

        log.write_log('create_data_json: Done')
        return True

    except Exception as e:
        log.write_log('create_data_json: {}'.format(e.args[0]))
        return False
