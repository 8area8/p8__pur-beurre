"""S3 Storage module."""

from storages.backends.s3boto import S3BotoStorage
from django.conf import settings


class MediaStorage(S3BotoStorage):
    """Media storage class."""

    location = settings.AWS_MEDIA_DIR
