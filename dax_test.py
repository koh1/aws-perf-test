import os, sys, time, datetime
import amazondax
from boto3.session import Session
import asyncio

p = sys.argv
if len(p) < 4:
    print("Usage: python %s <AWS_ID> <AWS_SECRET> <endpoint>" % p[0])
    sys.exit(0)

session = Session(aws_access_key_id=p[1], aws_secret_access_key=p[2], region_name="ap-northeast-1")
dynamo = session.resource('dynamodb')
TABLE_NAME = "perftest"
key = "key"
table = dynamo.Table(TABLE_NAME)
dax = amazondax.AmazonDaxClient.resource(endpoints=[p[3]])

async def get_item(k, wait):
    for i in range(100):
        params = {
            "TableName": TABLE_NAME,
            "Key": {
                "key": {"S": "allowed"}
            }
        }
        dax.get_item(**params)
        await asyncio.sleep(wait)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t0 = datetime.datetime.now()
    result = loop.run_until_complete(asyncio.gather(
        get_item("allowed", 0.002),
        get_item("allowed", 0.002),
        get_item("allowed", 0.002),
        get_item("allowed", 0.002),
    ))
    t1 = datetime.datetime.now()
    params = {
        "TableName": TABLE_NAME,
        "Key": {
            "key": {"S": "allowed"}
        }
    }
    print(dax.get_item(**params))
    print(t1-t0)
