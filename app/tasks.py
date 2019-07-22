from celery import shared_task
from openpyxl import load_workbook
from . import models


@shared_task
def upload_file_task(file_name, title):
    try:
        # open uploaded excel file's first sheet
        work_book = load_workbook('media/' + file_name)
        sheet = work_book.get_sheet_by_name(work_book.sheetnames[0])

        # retrieve values of cells into a 2D array
        data = []

        # number of rows of the excel sheet
        num_rows = sheet.max_row

        for i in range(num_rows - 1):
            data.append([sheet['A' + str(i + 2)].value, sheet['B' + str(i + 2)].value,
                         sheet['C' + str(i + 2)].value,
                         sheet['D' + str(i + 2)].value, sheet['E' + str(i + 2)].value
                         ])

        # save metadata about the upload/submission to database
        upload_metadata = models.Upload(title=title, document_url=file_name)
        upload_metadata.publish()

        # save individual personal records to database
        for i in range(len(data)):
            individual_record = models.User(
                upload_id=upload_metadata.id,
                first_name=data[i][0],
                last_name=data[i][1],
                age=data[i][2],
                gender=data[i][3],
                address=data[i][4],
            )
            individual_record.publish()

        return 'Excel file uploaded successfully!, {} rows were recorded'.format(num_rows - 1)

    except Exception as e:
        return 'Excel file upload failed!, 0 rows were recorded'


