import frappe
import os
import re
import os.path
from frappe.utils import cint, split_emails


def take_backups_daily():
    take_backups_if("Daily")


def take_backups_weekly():
    take_backups_if("Weekly")


def take_backups_monthly():
    take_backups_if("Monthly")


def take_backups_if(freq):
    if cint(frappe.db.get_value("Amazon S3 BackUp", None, "enable")):
        if frappe.db.get_value("Amazon S3 BackUp", None, "frequency") == freq:
            take_backups_s3()


@frappe.whitelist()
def take_backups_s3():
    try:
        backup_to_s3()
        send_email(True, "Amazon S3 BackUp")
    except Exception:
        error_message = frappe.get_traceback()
        frappe.errprint(error_message)
        send_email(False, "Amazon S3 BackUp", error_message)


def send_email(success, service_name, error_status=None):
    if success:
        subject = "Backup Upload Successful"
        message = """<h3>Backup Uploaded Successfully</h3><p>Hi there, this is just to inform you
        that your backup was successfully uploaded to your %s account. So relax!</p> """ % service_name

    else:
        subject = "[Warning] Backup Upload Failed"
        message = """<h3>Backup Upload Failed</h3><p>Oops, your automated backup to %s failed.
        </p> <p>Error message: %s</p> <p>Please contact your system manager
        for more information.</p>""" % (service_name, error_status)

    if not frappe.db:
        frappe.connect()

    recipients = split_emails(frappe.db.get_value("Amazon S3 BackUp", None, "notification_email"))
    frappe.sendmail(recipients=recipients, subject=subject, message=message)


def backup_to_s3():
    from boto.s3.connection import S3Connection
    from frappe.utils.backups import new_backup
    from frappe.utils import get_backups_path
    if not frappe.db:
        frappe.connect()

    conn = S3Connection(frappe.db.get_value("Amazon S3 BackUp", None, "aws_access_key_id"),
                        frappe.db.get_value("Amazon S3 BackUp", None, "secret_access_key"))

    # upload database
    company = re.sub('\s', '_', str(frappe.db.get_value("Global Defaults", None, "default_company")).lower());
    backup = new_backup(ignore_files=False, backup_path_db=None,
                        backup_path_files=None, backup_path_private_files=None, force=True)
    db_filename = os.path.join(get_backups_path(), os.path.basename(backup.backup_path_db))
    files_filename = os.path.join(get_backups_path(), os.path.basename(backup.backup_path_files))
    private_files = os.path.join(get_backups_path(), os.path.basename(backup.backup_path_private_files))

    upload_file_to_s3(db_filename, company, conn, frappe.db.get_value("Amazon S3 BackUp", None, "backup_plan"))
    upload_file_to_s3(private_files, company, conn, frappe.db.get_value("Amazon S3 BackUp", None, "backup_plan"))
    upload_file_to_s3(files_filename, company, conn, frappe.db.get_value("Amazon S3 BackUp", None, "backup_plan"))

    frappe.db.close()
    frappe.connect()


def upload_file_to_s3(filename, folder, connection, plan):
    from filechunkio import FileChunkIO
    import math
    import datetime

    if plan == 'Weekly Rotation':
        today = datetime.date.today()

        name = ''
        split_name = str(filename).split('_')
        print split_name
        for name_item in split_name[2:4]:
            name += '_' + name_item
        name = today.strftime('%A').lower() + name
        destpath = os.path.join(folder, os.path.basename(name))
    else:
        destpath = os.path.join(folder, os.path.basename(filename))

    bucket = connection.get_bucket(frappe.db.get_value("Amazon S3 BackUp", None, "bucket"))
    source_path = filename
    source_size = os.stat(source_path).st_size
    mp = bucket.initiate_multipart_upload(destpath)
    chunk_size = 52428800
    chunk_count = int(math.ceil(source_size / float(chunk_size)))
    for i in range(chunk_count):
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        with FileChunkIO(source_path, 'r', offset=offset, bytes=bytes) as fp:
            mp.upload_part_from_file(fp, part_num=i + 1)
    mp.complete_upload()
