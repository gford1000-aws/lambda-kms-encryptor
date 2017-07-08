import boto3
from base64 import b64encode
import os

REGION_NAME = os.environ['RegionName']
ACCOUNT_ID = os.environ['AccountId']

def encrypt(plaintext, kms_key_arn):
    client = boto3.client('kms')
    return b64encode(client.encrypt(Plaintext=plaintext, KeyId=kms_key_arn)["CiphertextBlob"])

def get_plaintext(event):
    plaintext = event.get('PlainText', None)
    if plaintext == None:
        raise Exception('Missing PlainText attribute from event')
    plaintext = str(plaintext)
    if plaintext == '':
        raise Exception('PlainText must be non-empty string')
    if len(plaintext) >= 4096:
        raise Exception('PlainText length must be less than 4096 bytes ({} sent)'.format(len(plaintext)))
    return plaintext

def get_kms_arn(event):
    kms_arn = event.get('KmsArn', None)
    if kms_arn == None:
        raise Exception('Missing KmsArn attribute from event')
    kms_arn = kms_arn.lower()
    kms_parts = kms_arn.split(':')
    if len(kms_parts) <> 6:
        raise Exception('Invalid KmsArn')
    if ':'.join([kms_parts[0], kms_parts[1], kms_parts[2]]) != 'arn:aws:kms':
        raise Exception('Arn does not specify KMS service')
    if kms_parts[5].split('/')[0] != 'key':
        raise Exception('Arn does not specify a key')
    if kms_parts[3] != REGION_NAME:
        raise Exception('Arn specifies a key in another Region')
    if kms_parts[4] != ACCOUNT_ID:
        raise Exception('Arn specifies a key for another Account')
    return kms_arn

def process(event):
    kms_arn = get_kms_arn(event)
    plaintext = get_plaintext(event)
    return encrypt(plaintext, kms_arn)

def lambda_handler(event, context):
    data = process(event)
    return data
