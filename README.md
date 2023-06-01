# Automated Attendance Tracking System

This is a Python script that automates the process of tracking employee attendance using Google Forms and Google Sheets. The script retrieves responses from a Google Form, updates a Google Sheet with the attendance data, and sends email notifications to the manager for any employees who are late or absent.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/attendance-tracker.git
   ```

2. Install the script:

   ```bash
   pip install -e .
   ```

3. Set up a Google Form and Google Sheet for tracking attendance. The Google Form should have three questions: one for the date and time, one for the employee name, and one for the attendance status (Present, Late, or Absent). The Google Sheet should have four columns: Date, Time, Employee Name, and Attendance Status.

4. Create a Google Service Account and download the JSON key file. This will be used to authenticate the Google Sheets API.

5. Set up environment variables for the Google Service Account JSON key file path and the manager email address:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service_account.json
   export MANAGER_EMAIL=manager@example.com
   ```

## Usage

To run the script, use the following command:

```bash
atts [sheet_name] [worksheet_name] [form_url]
```

where `[sheet_name]` is the name of the Google Sheet, `[worksheet_name]` is the name of the Google Sheet worksheet, and `[form_url]` is the URL of the Google Form.

For example:

```bash
atts "Attendance Sheet" "March 2022" "https://forms.google.com/test-form"
```

This will retrieve responses from the Google Form, update the Google Sheet with the attendance data, and send email notifications to the manager for any employees who are late or absent.

## Testing

To run the unit tests, use the following command:

```bash
python -m unittest discover
```

This will run all the unit tests in the `tests` directory.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
