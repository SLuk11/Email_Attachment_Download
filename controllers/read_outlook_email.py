import requests
import datetime
import os
import logger as log
from controllers.get_access_token_by_user_email_and_confidential import get_access_token
from controllers.directory_operator import create_batch_id


def download_email_attachments(api_endpoint, mail_user, message_id, batch_id, headers, save_dir):
    try:
        # Request email attachments
        response = requests.get(
            api_endpoint + '/users/{}/messages/{}/attachments'.format(mail_user, message_id),
            headers=headers
        )
        current_datetime = datetime.datetime.now()
        attachment_items = response.json()['value']
        attachment_data = []

        # loop for each attachment
        for attachment in attachment_items:
            attachment_detail = []
            file_name = attachment['name']

            # check file extension
            if file_name.endswith('.xlsx') or file_name.endswith('.pdf'):
                attachment_id = attachment['id']
                file_size = attachment['size']

                # Download attachment content
                attachment_content = requests.get(
                    api_endpoint + '/users/{}/messages/{}/attachments/{}/$value'.format(mail_user, message_id,
                                                                                        attachment_id)
                    , headers=headers
                )

                # save attachment content to directory
                save_name = '{}_{}_{}.{}'.format(file_name.split('.')[0]
                                                 , batch_id
                                                 ,current_datetime.strftime('%Y%m%d%H%M%S')
                                                 , file_name.split('.')[1])

                with open(os.path.join(save_dir, save_name), 'wb') as _f:
                    _f.write(attachment_content.content)

                # get attachment detail
                attachment_detail.append(file_name)
                attachment_detail.append(save_name)
                attachment_detail.append(file_name.split('.')[1])
                attachment_detail.append(file_size)
                attachment_detail.append(current_datetime)

                # append detail to data array
                attachment_data.append(attachment_detail)

        return attachment_data

    except Exception as e:
        log.write_log('Download_attachment: {}, {}'.format(file_name, e.args[0]))
        return []


def get_email_attachment(tenant_id, app_id, app_secret, app_scope, mail_user, api_endpoint
                         , req_params, sender_list, subject_key, save_dir):
    # get access_token
    token = get_access_token(tenant_id, app_id, app_secret, app_scope)
    headers = {
        "Authorization": f"Bearer {token}",
        "ContentType": "application/json"
    }

    if token != None:
        try:
            # Get Folder "Booking" id
            fol_res = requests.get(api_endpoint + '/users/{}/mailFolders/?includeHiddenFolders=true'.format(mail_user)
                                   , headers=headers)
            fol_res_json = fol_res.json()
            mailfolders = fol_res_json['value']
            fol_id = [fol['id'] for fol in mailfolders if fol['displayName'] == 'Booking']

            # Get mails messages in specific folder
            response = requests.get(api_endpoint + '/users/{}/mailFolders/{}/messages'.format(mail_user, fol_id[0])
                                    , headers=headers, params=req_params)
            response_json = response.json()
            emails = response_json['value']
            emails_sort = sorted(emails, key=lambda d: d['lastModifiedDateTime'])
            attachment_data = []

            for email in emails_sort:
                if email['hasAttachments']:
                    if email['from']['emailAddress']['address'] in sender_list \
                            and subject_key in email['subject'].lower():
                        email_id = email['id']
                        batch_id = create_batch_id()
                        attachment_detail = download_email_attachments(api_endpoint, mail_user, email_id
                                                            , batch_id, headers, save_dir)
                        if len(attachment_detail) > 0:
                            requests.patch(f'https://graph.microsoft.com/v1.0/users/{mail_user}/messages/{email_id}'
                                           , json={'isRead': True}, headers={'Authorization': f'Bearer {token}'})
                            log.write_log('Mark_read_email: Done')

                            # Create attachment dictionary

                            for detail in attachment_detail:
                                #Create attachment data dictionary
                                detail_array = []
                                detail_array.append(str(email['from']['emailAddress']['address'])),
                                detail_array.append(str(email['subject'])),
                                detail_array.append(str(detail[0])),
                                detail_array.append(str(detail[1])),
                                detail_array.append(str(detail[2])),
                                detail_array.append(str(detail[3])),
                                detail_array.append(str(detail[4])),
                                detail_array.append(str(email['lastModifiedDateTime']))

                                # add array to attachment_data
                                attachment_data.append(detail_array) #[Sender, 'Subject', 'OriginalFileName', 'FileName', 'Extension', 'Size', 'ReceiveDate', 'Created']

                        else:
                            log.write_log('Reading_email_process: Can NOT download attachment')

            log.write_log('Reading_email_process: Done')
            return attachment_data

        except Exception as e:
            log.write_log('Download_attachment: {}'.format(e.args[0]))
            return []

    else:
        return []