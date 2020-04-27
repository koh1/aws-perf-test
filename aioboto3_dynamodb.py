import asyncio
import aioboto3

async def main():
    async with aioboto3.resource('dynamodb', region_name='ap-northeast-1') as dr:
        table = await dr.Table('perftest')




loop = asyncio.get_event_loop()
loop.run_until_complete(main())