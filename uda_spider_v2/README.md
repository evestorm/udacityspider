## [拉勾](http://www.lagou.com/)爬取 

### 1. 项目介绍

爬取 [Lagou](www.lagou.com)工作数据,得到最新工作信息  

### 2. 安装支持

1. 安装homebrew

    terminal输入：`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

2. 安装 python3

    `brew install python3`

3. 安装 pip3

​        `sudo easy_install pip3`

1. 安装第三方库

​        `sudo pip3 install -r requirements.txt`

### 3. 使用方法

将整个项目文件夹放入 vs code，或者打开terminal，输入 `cd ` ，然后将整个文件夹拖入terminal。

然后输入 `cd spider` 进入 spider文件夹。

浏览器打开 `https://m.lagou.com/jobs/4737590.html` ，打开开发者工具，快捷键`ALT+CMD+I`，切到 network ，刷新网页，找到 `4737590.html` ，将 `Cookie` 值取出，放进 `jobdetail_spider` 中。

运行Spider下py文件，信息存储于Excel中

1. 运行 [m_lagou_spider.py](spider/m_lagou_spider.py) 来获取工作数据并生成Excel文件，生成文件位于 `spider——>data——>list` 下
2. 运行jobdetail_spider.py （运行之前，确保该文件下save_excel方法下的保存路径正确）获取职位详细信息，生成文件位于 `spider——>data——>detail` 下
3. 运行sw_combine.py 合并表格

​    匹配副表与主表相同字段，追加副表内容到主表中

​    合并文件后的文件位于`spider——>data——>combine` 下

> python3 m_lagou_spider.py

### 注意事项

如果在运行 `jobdetail_spider.py` 后报错，请将 `spider——>data` 文件夹下的 `list` 和 `detail` 两个文件夹中的内容保存到临时文件夹temp中。然后重新创建 `list` 和 `detail` 文件夹，然后将刚才保存在临时文件夹下的 `-JD.xlsx` 文件放入 `detail` 文件夹中；`.xlsx` 文件放入 `list` 文件夹中。