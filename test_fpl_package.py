#!/usr/bin/env python3

from fpl import FPL
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login()
        classic_league = await fpl.get_classic_league(1137)
    print(classic_league)

asyncio.run(main())
