# miku_daily_ranking
## 获取pixiv日榜排行榜中的初音未来的图片  
1. Python3
2. 代码默认在运行目录下创建一个当前时间的文件夹 格式：yy-mm-dd 例：2019-02-14  
3. 如果想使用 Crontab 来定时运行，请自行设置**绝对路径**
#### 如果想使用代理
~~~python
miku = Miku("https://127.0.0.1:10809") # 注意，这是一个HTTP代理
~~~
