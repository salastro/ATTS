import argparse
import datetime
import smtplib

import gspread
from loguru import logger
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API credentials
scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'YOUR_SERVICE_ACCOUNT_JSON_FILE_NAME.json', scope)
client = gspread.authorize(creds)


def update_attendance(sheet_name, worksheet_name, form_url, manager_email):
    try:
        # Get the Google Sheet and Worksheet
        sheet = client.open(sheet_name)
        worksheet = sheet.worksheet(worksheet_name)

        # Get the responses from the Google Form
        form = client.open_by_url(form_url)
        responses = form.get_form_responses()

        # Get the last row index
        last_row = len(worksheet.col_values(1))

        # Update the Google Sheet
        for response in responses:
            row_data = response.values()
            timestamp = datetime.datetime.strptime(
                row_data[0], '%m/%d/%Y %I:%M:%S %p')
            employee_name = row_data[1]
            attendance_status = row_data[2]

            # Check if the employee is late or absent
            if attendance_status == 'Late' or attendance_status == 'Absent':
                # Send email notification to the manager
                subject = f'{employee_name} is {attendance_status} on {timestamp.strftime("%m/%d/%Y")}'
                message = f'{employee_name} is {attendance_status} on {timestamp.strftime("%m/%d/%Y %I:%M:%S %p")}.'
                send_email(manager_email, subject, message)
                logger.info(f'Email notification sent to {manager_email}')

            # Update the Google Sheet
            data = [timestamp.strftime(
                '%m/%d/%Y'), timestamp.strftime('%I:%M:%S %p'), employee_name, attendance_status]
            worksheet.insert_row(data, last_row + 1)
            last_row += 1
            logger.info(
                f'Attendance data updated for {employee_name} on {timestamp.strftime("%m/%d/%Y %I:%M:%S %p")}')
    except Exception as e:
        logger.error(f'Error updating attendance: {e}')


def parse_arguments():
    # Define command line arguments
    parser = argparse.ArgumentParser(
        description='Automated Attendance Tracking System')
    parser.add_argument('sheet_name', type=str,
                        help='Name of the Google Sheet')
    parser.add_argument('worksheet_name', type=str,
                        help='Name of the Google Sheet worksheet')
    parser.add_argument('form_url', type=str, help='URL of the Google Form')
    parser.add_argument('manager_email', type=str,
                        help='Email address of the manager')
    return parser.parse_args()


def send_email(to, subject, message):
    try:
        # Email account details
        from_address = 'YOUR_EMAIL_ADDRESS'
        password = 'YOUR_EMAIL_PASSWORD'

        # Create the email message
        msg = f'Subject: {subject}\n\n{message}'

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(from_address, password)
            smtp.sendmail(from_address, to, msg)
    except Exception as e:
        logger.error(f'Error sending email: {e}')


if __name__ == '__main__':
    # Configure logging
    logger.add('attendance.log', rotation='10 MB',
               compression='zip', format='{time} {level} {message}')

    # Parse the command line arguments
    args = parse_arguments()

    # Call the update_attendance function
    update_attendance(args.sheet_name, args.worksheet_name,
                      args.form_url, args.manager_email)
