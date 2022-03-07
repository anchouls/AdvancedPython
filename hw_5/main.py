import asyncio
import aiofiles
import aiohttp
import sys


async def download_photo(session, folder, i):
    async with session.get('https://picsum.photos/400') as response:
        if response.status == 200:
            file_name = f'{folder}/{i}.png'
            f = await aiofiles.open(file_name, mode='wb')
            await f.write(await response.read())
            await f.close()


async def download_all_photos(folder, count):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(download_photo(session, folder, i + 1) for i in range(count)))


def main():
    if len(sys.argv) == 3:
        folder = sys.argv[1]
        count = int(sys.argv[2])
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_all_photos(folder, count))
        loop.close()
    else:
        print('Wrong number of arguments')


if __name__ == "__main__":
    main()
