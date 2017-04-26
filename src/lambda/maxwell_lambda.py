from __future__ import print_function
import json
import base64
import boto3

firehose = boto3.client('firehose')
deliveryStreamName = 'FILL IN YOUR FIREHOSE STREAM NAME HERE'


def lambda_handler(event, context):
    for record in event['Records']:
       #Kinesis data is base64 encoded so decode here
       payload = base64.b64decode(record["kinesis"]["data"])
       json_str = json.loads(payload)
       print("Binlog Playload: " + json.dumps(json_str) + '\n')

       # put the record into Kinesis delivery string
       firehoseString = convertToFirehoseString(payload)
       print('Firehose string: ' + firehoseString)
       firehose.put_record(DeliveryStreamName=deliveryStreamName, Record={ 'Data': firehoseString})

    return 'Successfully processed {} records.'.format(len(event['Records']))



# function to parse the payload and return the string per field
# we just take a simple conversion to make all fields in string :-). The best way to implment this 
# could be a schematizer (like Yelp's implementation) for automatic parsing and conversion
def getBinlogField(payload, field):
    json_str = json.loads(payload)
    if field != 'data':
        field_str = str(json_str[field])
    # this is field data and lets assume this is only for employee table schema
    else:
        field_str = str(json_str[field]['emp_no']) + ',' + str(json_str[field]['birth_date']) + ',' + str(json_str[field]['first_name']) + ',' + str(json_str[field]['last_name']) + ',' + str(json_str[field]['gender']) + ',' + str(json_str[field]['hire_date'])

    return field_str


#Function for parsing the kinesis data payload into the desired String format (i.e. to csv)
def convertToFirehoseString(payload):
    print('Creating Firehose string')
   
    database = getBinlogField(payload, 'database')
    table = getBinlogField(payload, 'table')
    operation = getBinlogField(payload, 'type')
    data_item = getBinlogField(payload, 'data')

    # lets concatate the fields with comma so we can copy the from S3 to redshift
    firehoseString = ''
    firehoseString = database + ',' + table + ',' + operation + ',' + data_item + '\n'
    return firehoseString
 
