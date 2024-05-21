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


def multi_part_upload(bucket_name, item_name, file_data):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        # with open(file_path, "rb") as file_data:
        cos.Object(bucket_name, item_name).upload_fileobj(
            Fileobj=file_data,
            Config=transfer_config
        )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))

# def create_word_doc_with_dict(data_dict):
#     doc = Document()
#
#     # Convert the dictionary to a pretty-printed JSON-formatted string
#     json_string = json.dumps(data_dict, indent=4)
#     pretty_json = pprint.pformat(json.loads(json_string))
#
#     # Write the JSON content to the Word document
#     doc.add_paragraph(pretty_json)
#
#     # Save the Word document
#     doc.save("output_new1.docx")


def create_pdf_with_dict(data_dict):
    buffer = BytesIO()  # Create a BytesIO buffer to hold the PDF content
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Set up the styles for the text
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']

    # Convert the dictionary to a pretty-printed JSON-formatted string
    json_string = json.dumps(data_dict, indent=4)
    pretty_json = pprint.pformat(json.loads(json_string))

    # Split the pretty-printed JSON string into lines
    lines = pretty_json.splitlines()

    # Create a list of Paragraph objects with appropriate line breaks
    text_content = [Paragraph(line, style_normal) for line in lines]

    # Build the PDF document
    doc.build(text_content)

    # Move the buffer's pointer back to the beginning
    buffer.seek(0)

    return buffer


neo4j_uri = 'neo4j+s://a2903c3d.databases.neo4j.io'
neo4j_user = 'neo4j'
neo4j_password = 'x7lO8GKrglcmm4MYuHcBp_PJx23STanbAUKfnuj_FIg'


def get_versions(session, agency):
    query = "MATCH (a:Agency {agencyID: $agency})-->(v:Version) RETURN v LIMIT 10"
    result = session.run(query, agency=agency)
    details = []
    for record in result:
        # print(record)
        details.append(record['v']._properties["version"])
        # details.append({
        #   "label": record['v']._properties["version"],
        #   "value": {
        #     "input": {
        #       "text": record['v']._properties["version"]
        #     }
        #   }
        # })
    return details


def get_fgs(session, agency, version):
    query = "MATCH (a:Agency {agencyID: $agency})-->(v:Version {version: $version})-->(fg: FunctionalGroup) RETURN fg LIMIT 10"
    result = session.run(query, agency=agency, version=version)
    details = []
    for record in result:
        # print(record)
        details.append(record['fg']._properties["FunctionalGroupID"])
        # details.append({
        #   "label": record['fg']._properties["FunctionalGroupID"],
        #   "value": {
        #     "input": {
        #       "text": record['fg']._properties["FunctionalGroupID"]
        #     }
        #   }
        # })
    return details


def get_tss(session, agency, version, fg):
    query = "MATCH (a:Agency {agencyID: $agency})-->(v:Version {version: $version})-->(fg: FunctionalGroup {FunctionalGroupID: $fg})-->(ts: TransactionSet) RETURN ts LIMIT 10"
    result = session.run(query, agency=agency, version=version, fg=fg)
    details = []
    for record in result:
        # print(record)
        details.append(record['ts']._properties["transaction_set"])
        # details.append({
        #   "label": record['ts']._properties["transaction_set"],
        #   "value": {
        #     "input": {
        #       "text": record['ts']._properties["transaction_set"]
        #     }
        #   }
        # })
    return details


def get_segments(session, agency, version, fg, ts):
    query = "MATCH (a:Agency {agencyID: $agency})-->(v:Version {version: $version})-->(fg: FunctionalGroup {FunctionalGroupID: $fg})-->(ts: TransactionSet {transaction_set: $ts})-->(s: Segment) RETURN s LIMIT 10"
    result = session.run(query, agency=agency, version=version, fg=fg, ts=ts)
    details = []
    for record in result:
        # print(record)
        details.append(record['s']._properties["SegmentID"])
        # details.append({
        #   "label": record['s']._properties["SegmentID"],
        #   "value": {
        #     "input": {
        #       "text": record['s']._properties["SegmentID"]
        #     }
        #   }
        # })
    return details


def get_elements(session, agency, version, fg, ts, segment):
    query = "MATCH (a:Agency {agencyID: $agency})-->(v:Version {version: $version})-->(fg: FunctionalGroup {FunctionalGroupID: $fg})-->(ts: TransactionSet {transaction_set: $ts})-->(s: Segment {SegmentID: $segment})-->(e: Element) RETURN e LIMIT 10"
    result = session.run(query, agency=agency, version=version, fg=fg, ts=ts, segment=segment)
    details = []
    for record in result:
        # print(record)
        details.append(record['e']._properties["ElementID"])
        # details.append({
        #   "label": record['e']._properties["ElementID"],
        #   "value": {
        #     "input": {
        #       "text": record['e']._properties["ElementID"]
        #     }
        #   }
        # })
    return details


def get_codes(session, agency, version, fg, ts, segment, element):
    query = "MATCH (a:Agency {agencyID: $agency})-->(v:Version {version: $version})-->(fg: FunctionalGroup {FunctionalGroupID: $fg})-->(ts: TransactionSet {transaction_set: $ts})-->(s: Segment {SegmentID: $segment})-->(e: Element {ElementID: $element})-->(c: Code) RETURN c LIMIT 10"
    result = session.run(query, agency=agency, version=version, fg=fg, ts=ts, segment=segment, element=element)
    details = []
    for record in result:
        # print(record)
        details.append(record['c']._properties["value"])
        # details.append({
        #   "label": record['c']._properties["value"],
        #   "value": {
        #     "input": {
        #       "text": record['c']._properties["value"]
        #     }
        #   }
        # })
    return details


def get_info(session, agency, version, fg, ts, segment, element, code, name, ftype='pdf'):
    query = "MATCH (a:Agency {agencyID: $agency})-->(v:Version {version: $version})-->(fg: FunctionalGroup {FunctionalGroupID: $fg})-->(ts: TransactionSet {transaction_set: $ts})-->(s: Segment {SegmentID: $segment})-->(e: Element {ElementID: $element})-->(c: Code {value: $code}) RETURN a,v,fg,ts,s,e,c"
    result = session.run(query, agency=agency, version=version, fg=fg, ts=ts, segment=segment, element=element, code=code)
    details = []
    for record in result:
        # print(record)
        details.append({
            "Agency": record['a']._properties,
            "Version": record['v']._properties,
            "FunctionalGroup": record['fg']._properties,
            "TransactionSet": record['ts']._properties,
            "Segment": record['s']._properties,
            "Element": record['e']._properties,
            "Code": record['c']._properties
        })
    if ftype == 'pdf':
        pdf_buffer = create_pdf_with_dict({"results": details})
        # Now you can save the buffer contents into a file if needed
        multi_part_upload("edi-bucket", name+"_edi.pdf", pdf_buffer)
        # with open("output.pdf", "wb") as f:
        #     f.write(pdf_buffer.read())
        return "https://edi-bucket.s3.us-south.cloud-object-storage.appdomain.cloud/"+name+"_edi.pdf"
    # else:
    #     create_word_doc_with_dict({"results": details})
    return details


def main(args):
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    details = []
    with driver.session() as session:
        agency = args.get("agency")
        version = args.get("version")
        fg = args.get("fg")
        tset = args.get("tset")
        segment = args.get("segment")
        element = args.get("element")
        code = args.get("code")
        ftype = args.get("ftype")
        name = args.get("name")
        title = "Please select "
        if code:
            details = get_info(session, agency, version, fg, tset, segment, element, code, name, ftype)
            return {"results": details}
        elif element:
            details = get_codes(session, agency, version, fg, tset, segment, element)
            title += "a code"
        elif segment:
            details = get_elements(session, agency, version, fg, tset, segment)
            title += "an element"
        elif tset:
            details = get_segments(session, agency, version, fg, tset)
            title += "a segment"
        elif fg:
            details = get_tss(session, agency, version, fg)
            title += "a transaction set"
        elif version:
            details = get_fgs(session, agency, version)
            title += "a functional group"
        elif agency:
            details = get_versions(session, agency)
            title += "a version"
    driver.close()
    # return {"results": [
    #     {
    #         "title": title,
    #         "options": details,
    #         "description": "",
    #         "response_type": "option"
    #     }
    # ]}
    return {"results": details}


# print(main({"agency": "E", "version": "092001", "fg": "CONEST", "tset": "CONEST", "segment": "BII",
#             "element": "7429", "code": "2", "name": "kedar", "ftype": "docx"}))
# pdf_buffer = create_pdf_with_dict({"11":"heloo","new":{"2":"hello2","3":"hello3"}})
#
# # Now you can save the buffer contents into a file if needed
# with open("output.pdf", "wb") as f:
#     f.write(pdf_buffer.read())
# create_word_doc_with_dict({"11":"heloo","new":{"2":"hello2","3":"hello3"}})
# print(main({"agency": "E"}))
# main({"agency": "E", "version": "092001", "fg": "CONEST", "tset": "CONEST", "segment": "BII",
#             "element": "7429", "code": "2", "name": "kedar", "ftype": "docx"})


def main(args):
    print("Invoked main");
    #driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    return {"body": "success"}

