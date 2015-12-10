# -*- coding: utf-8 -*-
# Copyright (c) 2015, Chris Ian Fiel and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class AmazonS3Settings(Document):
    def validate(self):
        from boto.s3.connection import S3Connection

        conn = S3Connection(self.aws_access_key_id, self.secret_access_key)
        try:
            conn.get_all_buckets()
        except:
            frappe.throw(_("Invalid Access Key or Secret Key."))

        bucket_lower = str(self.bucket).lower()

        check_exist = conn.lookup(bucket_lower)
        if check_exist is None:
            try:
                conn.create_bucket(bucket_lower)
            except:
                frappe.throw(_("Unable to create bucket {0}. Change it to a more unique ").format(bucket_lower))
