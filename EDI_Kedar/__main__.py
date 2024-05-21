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



def main(args):
    print("Invoked main");
    neo4j_uri = 'neo4j+s://a2903c3d.databases.neo4j.io'
    neo4j_user = 'neo4j'
    neo4j_password = 'x7lO8GKrglcmm4MYuHcBp_PJx23STanbAUKfnuj_FIg'
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    return {"body": "success"}

