from neo4j import GraphDatabase
from neo4j import GraphDatabase
import json
import pprint
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
# from docx import Document

import ibm_boto3
from ibm_botocore.client import Config, ClientError

# Constants for IBM COS values
COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "9ITYiSk-BpydNpRFnwTczyliKE5VFqaTZEPtkhI_5MeH" # eg "W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/010dcec46cce40a9a8555682c8c82e84::serviceid:ServiceId-f61fe320-d830-4f83-bb07-e31daa91878d" # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003xxxxxxxxxx1c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

# Create resource
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

'''
{
    "apikey": "9ITYiSk-BpydNpRFnwTczyliKE5VFqaTZEPtkhI_5MeH",
    "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
    "iam_apikey_description": "Auto-generated for key crn:v1:bluemix:public:cloud-object-storage:global:a/010dcec46cce40a9a8555682c8c82e84:73483270-b430-45f6-aec0-595bbac30668:resource-key:89a2eb67-d52c-40b4-8d45-1a26870d2942",
    "iam_apikey_name": "edi-cloud-func",
    "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
    "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/010dcec46cce40a9a8555682c8c82e84::serviceid:ServiceId-f61fe320-d830-4f83-bb07-e31daa91878d",
    "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/010dcec46cce40a9a8555682c8c82e84:73483270-b430-45f6-aec0-595bbac30668::"
}
'''

def main(args):
    print("Invoked main")
    return {
          # specify headers for the HTTP response
          # we only set the Content-Type in this case, to 
          # ensure the text is properly displayed in the browser
          "headers": {
              "Content-Type": "text/plain;charset=utf-8",
          },
          
          ## use the text generator to create a response sentence
          #  with 10 words
          "body": "success"
      }

