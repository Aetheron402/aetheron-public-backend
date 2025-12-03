"""
Aetheron — R2 Storage Client Template
-------------------------------------

This module provides a structural template for interacting with
an S3-compatible object storage service such as Cloudflare R2.

It shows how upload functions are organized and how file URLs
are constructed, while using simplified placeholder logic suitable
for a public backend template.
"""

import os
import boto3
from botocore.config import Config


# -------------------------------------------------------------------------
# Client Factory (Template)
# -------------------------------------------------------------------------

def get_r2_client():
    """
    Returns an S3-compatible client using environment configuration.

    Template version:
    - Uses standard boto3 client construction
    - Reflects the structure of the real implementation
    """

    return boto3.client(
        "s3",
        endpoint_url=os.getenv("R2_ENDPOINT"),
        aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
    )


# -------------------------------------------------------------------------
# Upload Helper (Template)
# -------------------------------------------------------------------------

def r2_upload_bytes(data: bytes, filename: str) -> str:
    """
    Uploads bytes to object storage and returns a public URL.

    Parameters:
    - data: raw file bytes
    - filename: name to store under

    Template version:
    - Performs a basic put_object call
    - Constructs a URL based on R2_PUBLIC_BASE
    """

    client = get_r2_client()
    bucket = os.getenv("R2_BUCKET_NAME")
    public_base = os.getenv("R2_PUBLIC_BASE")

    content_type = (
        "application/pdf"
        if filename.lower().endswith(".pdf")
        else "text/plain"
    )

    client.put_object(
        Bucket=bucket,
        Key=filename,
        Body=data,
        ContentType=content_type,
        ContentDisposition=f'attachment; filename="{filename}"',
    )

    # Return public URL
    return f"{public_base}/{filename}"
