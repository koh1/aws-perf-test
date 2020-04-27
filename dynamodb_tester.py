import asyncio
import sys
import datetime
from boto3.session import Session

p = sys.argv
session = Session(aws_access_key_id=p[1], aws_secret_access_key=p[2])
dynamo = session.resource('dynamodb')
TABLE_NAME = "perftest"
key = "key"
table = dynamo.Table(TABLE_NAME)


def put_item(key, value):
    pass

def get_item(key):
    return ""

async def increment(thread_name, key, n, wait):
    for i in range(100):
        res = table.update_item(
            Key={
                'key': key
            },
            UpdateExpression="ADD #name :increment",
            ExpressionAttributeNames={
                '#name':'count'
            },
            ExpressionAttributeValues={
                ":increment": int(n)
            },
            ReturnValues="UPDATED_NEW"
        )
        #print("Thread: %s, Key=%s, Item=%s"%(thread_name, key, res['Attributes']['count']))
        await asyncio.sleep(wait)

def decrement(key, n):
    pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    table.put_item(Item={
        "key": "allowed",
        "count": 0
    })
    t0 = datetime.datetime.now()

    result = loop.run_until_complete(asyncio.gather(
        increment("th1", "allowed", 1, 0.002),
        increment("th2", "allowed", 1, 0.002),
        increment("th3", "allowed", 1, 0.002),
        increment("th4", "allowed", 1, 0.002),
    ))
    t1 = datetime.datetime.now()
    res = table.get_item(Key={
        "key": "allowed"
    })
    print(res)
    print(t1-t0)
