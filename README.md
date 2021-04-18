## 一些为了[label-studio](https://github.com/heartexlabs/label-studio)写的脚本

#### deve.py

- 开发测试使用，忽略即可

#### projectCreator.py

- 中间件
- 读取预定义的tsv文件，根据其中预定义的项目名称创建足够的项目，并返回项目id列表

#### upload_audio.py

- @Author：lovemefan
- 上传一个音频文件作为任务到指定项目
- 事实上上传的是一个路径，而非真实文件
- 可以携带预标记
- 可以根据本地文件自动获取文件持续时间

#### main.py

- 当前项目主入口文件
- 根据预定义tsv文件创建足够的项目并按照平均分配进行语料切割，上传到对应的项目中
- 详细参数参照文件内注释

#### config.py

- 项目配置文件，仓库内未给出，如要使用本项目，请自行定义

- 文件结构

- ```python
  class Config:
      URL = "string" -> label-studio地址
      TOKEN = "string" -> 创建者的token
      PROJETCS_DESP = "string" -> 新建项目的详细描述（Nullable）
      LABEL_CONFIG = "string" -> xml格式的项目预定义config，参考label-studio官方文档
      LOG_FILE = "string" -> 日志输出文件
  ```