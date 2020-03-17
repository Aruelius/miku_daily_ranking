# -*- coding:utf-8 -*-
import asyncio
import datetime
import os
import zipfile
from io import BytesIO

import aiohttp


class Miku():
    def __init__(self, proxy=None):
        self.NAME = "初音ミク"
        self.IMG_URL = "https://i.pximg.net/img-original/img/"
        self.headers = {"referer": "https://www.pixiv.net/"}
        self.proxy = proxy if proxy else None
        self.get_path = lambda: f"./Miku/{str(datetime.date.today())}/"
        self.ranking_url = lambda p: f"https://www.pixiv.net/ranking.php?mode=daily&p={p}&format=json"
        self.zip_url = lambda pid: f"https://www.pixiv.net/ajax/illust/{pid}/ugoira_meta"
        self.optimize_gif = False # 是否压缩GIF, 默认否

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

    async def unzip(self, pid: int) -> tuple:
        from numpy import argmax, bincount
        async with aiohttp.ClientSession() as session:
            async with session.get(self.zip_url(pid),
                headers=self.headers,
                proxy=self.proxy) as r:
                response = await r.json()
        frames =  response["body"]["frames"]
        duration = argmax(bincount([_["delay"] for _ in frames])) / 100
        image_list = [_["file"] for _ in frames]
        zip_file_url = response['body']['originalSrc']
        stream = await self.req(zip_file_url)
        f = zipfile.ZipFile(file=BytesIO(stream))
        f.extractall(f"{self.get_path()}{pid}")
        f.close()
        return image_list, duration

    def create_gif(self, pid: int, image_list: list, duration: float):
        import imageio
        frames = [
            imageio.imread(f"{self.get_path()}{pid}/{image_name}")
            for image_name in image_list
        ]
        print(f"Starting Create GIF: {pid}.gif")
        imageio.mimsave(f"{self.get_path()}{pid}.gif", frames, "GIF", duration=duration)
        if self.optimize_gif:
            try:
                from pygifsicle import optimize
                optimize(f"{self.get_path()}{pid}.gif")
            except:
                print("pygifsicle 安装教程：\n\
                https://github.com/LucaCappelletti94/pygifsicle")

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
            if suffix:
                image_url = f"{url}{suffix}"
                tasks.append(asyncio.create_task(
                    self.write_file(
                        file_path=f"{self.get_path()}{image_url.split('/')[-1]}",
                        stream=await self.req(image_url)
                )))
            else: # GIF
                image_list, duration = await self.unzip(pixiv_id)
                self.create_gif(pixiv_id, image_list, duration)                

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
