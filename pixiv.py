# -*- coding:utf-8 -*-
import asyncio
import datetime
import os

import aiohttp


class Miku():
    def __init__(self, proxy=None):
        self.NAME = "初音ミク"
        self.IMG_URL = "https://i.pximg.net/img-original/img/"
        self.headers = {"referer": "https://www.pixiv.net/"}
        self.proxy = proxy if proxy else None
        self.get_path = lambda: f"./Miku/{str(datetime.date.today())}/"
        self.ranking_url = lambda p: f"https://www.pixiv.net/ranking.php?mode=daily&p={p}&format=json"

    async def req(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers,
                    proxy=self.proxy) as r:
                return await r.read()

    async def png_or_jpg(self, url: str):
        for suffix in [".png", ".jpg"]:
            async with aiohttp.ClientSession() as session:
                async with session.head(url + suffix,
                        headers=self.headers,
                        proxy=self.proxy) as r:
                    if r.status == 200: return suffix

    async def write_file(self, file_path: str, stream: bytes):
        if not os.path.exists(self.get_path()):
            os.makedirs(self.get_path())
        with open(file_path, "wb") as f:
            f.write(stream)
            f.close()

    async def download(self, content: dict):
        title = content["title"]
        up_date = content["date"]
        pixiv_id = content["illust_id"]
        width = content["width"]
        height = content["height"]
        rank = content["rank"]
        illust_page_count = int(content["illust_page_count"])
        
        path_list = content["url"].split('/')
        year, month, day, hour, minute, second = [_ for _ in path_list[7:13]]

        print("=" * 39)
        print("日榜排名:", rank)
        print("标题:", title)
        print("上传日期:", up_date)
        print("图片ID:", pixiv_id)
        print(f"分辨率: {width} X {height}")

        tasks = []
        for index in range(illust_page_count):
            url = f"{self.IMG_URL}{year}/{month}/{day}/{hour}/{minute}/{second}/{pixiv_id}_p{index}"
            suffix = await self.png_or_jpg(url)
            image_url = f"{url}{suffix}"
            tasks.append(asyncio.create_task(
                self.write_file(
                    file_path=f"{self.get_path()}{image_url.split('/')[-1]}",
                    stream=await self.req(image_url)
            )))
        for task in tasks:
            await task
    
    async def fetch(self, url: str):
        tasks  = []
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, proxy=self.proxy) as r:
                response = await r.json()
        for content in response["contents"]:
            if self.NAME in str(content):
                tasks.append(asyncio.create_task(self.download(content)))
        for task in tasks:
            await task
        
    async def run(self):
        tasks = []
        for p in range(1, 11):
            tasks.append(asyncio.create_task(self.fetch(self.ranking_url(p))))
        for task in tasks:
            await task

    def main(self):
        asyncio.run(self.run())

if __name__ == "__main__":
    miku = Miku()
    miku.main()
