
# ThingkingMathGPT

#### 让语言模型像人一样通过思考，而不是使用外部工具的前提下，计算出简单数学题答案。

---

### 一、关键目录结构

1. datasets - 数据集制作
   - src - 生成脚本
   - output - 初步生成输出区
   - release - 发行版本
2. experiment - 大模型实验框架
   - main-exp-frame - 通用全部训练实验框架
   - llama-recipes-main - llama1 用于参考学习
   - llama2-chinese-main - llama2中文 用于参考学习
3. analysis - 实验结果分析
   - checkpoint - 训练检查点记录
   - src - 结果分析用脚本
   - output - 结果分析输出

<br/>

### 二、环境配置


1. 数据集生成&实验结果分析环境
   - python 3.9+ 暂无其他

2. 大模型实验环境
   - 请参考 @MikeGu721 的[EasyLLM](https://github.com/MikeGu721/EasyLLM)项目README

<br/>

### 三、提问建议与BUG上报

1. 可通过Github的issue页进行提问与建议，尽量附带标签与详细代码。

2. 错误修复与新增功能请进行PR，当前只有主分支处于活跃。
