from abc import ABC
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage, ABC):
    location = settings.AWS_MEDIA_LOCATION
    file_override = True
    # default_acl = 'private'
