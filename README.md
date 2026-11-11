# Whisper 字幕

将音频转成文字和SRT字幕，支持中文、英文、日文及英文翻译。

AutoDL.Art：[Whisper-Subtitles](https://www.autodl.art/i/zw2029181901/autodl-whisper/Whisper-Subtitles)。v1已提交审核，等待平台通过后开放创建实例。

源码仓库不包含模型权重。本次导出环境把模型、独立依赖和启动配置放在系统盘，使用之后保存就绪的镜像无需再次安装或下载模型。模型版本固定在 `app.json`。

镜像 `autodl-whisper-20261111`，UUID `image-cd03170f61`，平台体积1.91GB，已就绪。社区审核及公开状态以平台当前状态为准。

镜像使用说明见 [IMAGE_README.md](IMAGE_README.md)，验收及保存记录见 [IMAGE_VALIDATION.json](IMAGE_VALIDATION.json)。

## 从源码另行安装

以下命令在AutoDL Linux实例执行。已使用保存镜像的用户直接打开6006即可。

```bash
cd /root
git clone https://github.com/zw2029181901/autodl-whisper.git
cd /root/autodl-whisper
bash install.sh
.venv/bin/python runtime/prefetch.py --project .
.venv/bin/python runtime/doctor.py --project . --models
bash start.sh
```

CPU INT8模式，不依赖GPU。建议8核CPU、4GB内存起测。

模型约0.49GB，输出等预留空间建议2GB；基础框架和Python依赖另计。保存镜像只保存系统盘，数据盘不会随镜像分发；本次权重位于系统盘 `/root/autodl-active/models`。平台实际镜像体积与账号总容量须逐份核对。

许可：MIT。[模型项目](https://github.com/SYSTRAN/faster-whisper)。本项目提供中文界面、运行配置与部署脚本，模型算法归原作者。许可文件随代码保留。
