from push_receiver_py import register, listen
from ruo import Client


import asyncio
import aiohttp
import json


clientid = 848238537804
credentials = {}
loop = asyncio.get_event_loop()

from pathlib import Path 
async def main():
    credentials = {}
    c = Client()

    if Path("response.json").is_file() and Path("key.pem").is_file():
        c.import_response("response.json")
        c.import_key("key.pem")
    else:
        c.export_key("key.pem")
        while True:
            try:
                code = input("Enter code: ")

                c.read_code(code)
                c.activate()
                c.export_response()
                break
            except ValueError:
                print("Invalid code")
    
    if Path("fcm_cred.json").is_file():
        with open("fcm_cred.json", "r") as f:
            credentials = json.load(f)
    else:
        async with aiohttp.ClientSession() as session:
            credentials = await register(session, clientid)
            with open("fcm_cred.json", "w") as f:
                json.dump(credentials, f)
    
    print(credentials)
    c.register("GCM:"+credentials["fcm"]["token"])
    # print(c.device_info())

    async with aiohttp.ClientSession() as session:
        client = await listen(session, credentials) 
        with client:
            while True:
                recv = await client.recv()
                print(recv)
                if "data" in recv and "urgid" in recv["data"]:
                    c.reply_transaction(recv["data"]["urgid"], "approve")



    


if __name__ == "__main__":
    loop.run_until_complete(main())