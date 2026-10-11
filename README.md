# Cloud Resource Janitor

Cloud Resource Janitor is a read-only platform that inventories AWS and Azure
resources, detects governance and potential cost risks, and produces safe
cleanup recommendations.

## Safety principle

The Janitor does not delete, stop, resize, or modify cloud resources.
All recommendations require human verification and approval.

## Initial resource scope

### AWS

- EC2 instances
- EBS volumes
- S3 buckets

### Azure

- Virtual machines
- Managed disks
- Storage accounts

## Current features

- FastAPI application
- Health endpoint
- Mock cloud-resource endpoint
- Interactive API documentation

## Local setup

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
