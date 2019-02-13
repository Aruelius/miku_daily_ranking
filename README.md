# get-pixiv-daily-ranking
获取pixiv日榜排行榜的初音未来的图片 
Python新手，代码比较凌乱。。。 
Python版本3.7.2 
代码默认在运行目录下创建一个当前时间的文件夹 格式：yy-mm-dd 例：2019-02-14 
代码调用我自己的反代p站网址：https://www.pixiv.pro
因为p站自己的网址直接访问需要Referer，懒得加，就用自己的，而且在国内也可以访问。
下载是用requests，单线程会比较慢。
很多if来判断图片的格式，图片是否有多p
