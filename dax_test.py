import os, sys, time, datetime
import amazondax
import botocore.session
import asyncio

session = botocore.session.get_session()
dynamo = session.create_client('dynamodb', region_name='ap-northeast-1')
table_name = "perftest"

if len(sys.argv) > 1:
    endpoint = sys.argv[1]
    dax = amazondax.AmazonDaxClient(session, region_name='ap-northeast-1', endpoints=[endpoint])
    client = dax
else:
    client = dynamo

async def get_item(k, wait):
    for i in range(100):
        params = {
            "TableName": table_name,
            "Key": {
                "key": {"S": "allowed"}
            }
        }
        client.get_item(**params)
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
        "TableName": table_name,
        "Key": {
            "key": {"S": "allowed"}
        }
    }
    print(client.get_item(**params))
    print(t1-t0)
