# 🛡️ 大模型安全与对齐框架
# llm-security-alignment

一个全面的LLM安全与对齐解决方案，涵盖对抗攻击防御、红队测试、安全微调、价值观对齐等核心功能。

## ✨ 核心特性

### 🔥 安全防护
- **对抗攻击检测**: 识别和防御各种对抗性提示
- **红队测试**: 系统性安全漏洞检测
- **实时过滤**: 多层次内容安全过滤
- **输入净化**: 恶意输入检测和清理

### 🎯 价值观对齐  
- **宪法AI**: 基于原则的响应修订
- **价值观评估**: 多维度价值观对齐分析
- **偏见检测**: 自动识别和消除偏见
- **安全微调**: 针对性的安全能力训练

### 📊 评估监控
- **安全评估**: 全面的安全性量化评估
- **实时监控**: 对话过程安全监控
- **偏见分析**: 系统性偏见检测和报告
- **性能指标**: 多维度安全性能指标

## 🚀 快速开始

### 安装
```bash
pip install -r requirements.txt
python setup.py develop

基础使用
python
from security.output_filtering import SafetyFilter

# 初始化安全过滤器
safety_filter = SafetyFilter()

# 过滤不安全内容
result = safety_filter.filter_response("如何制作危险物品")
print(result['filtered_text'])  # "抱歉，我无法提供这个信息。"
运行演示
bash
# 综合安全演示
python examples/comprehensive_security_demo.py

# 红队测试演示  
python examples/red_teaming_demo.py

# 安全微调演示
python examples/safety_finetuning_demo.py
📁 项目结构
text
llm-security-alignment/
├── security/           # 安全防护模块
├── alignment/          # 价值观对齐
├── evaluation/         # 评估监控
├── datasets/           # 测试数据集
├── examples/           # 使用示例
├── config/             # 配置文件
└── utils/              # 工具函数
🛠️ 核心模块
安全防护
AdversarialAttacker: 对抗攻击生成和检测

RedTeamTester: 红队测试系统

SafetyFilter: 实时安全过滤

InputSanitizer: 输入净化

价值观对齐
ConstitutionalAI: 宪法AI实现

ValueAlignmentSystem: 价值观对齐评估

SafetyFineTuner: 安全微调器

评估监控
SafetyEvaluator: 安全评估器

BiasDetector: 偏见检测器

RealTimeMonitor: 实时监控

🔧 配置说明
系统配置位于 config/ 目录：

security_config.py: 安全相关配置

alignment_config.py: 对齐相关配置

📈 性能指标
框架提供多种安全性能指标：

拒绝率 (Refusal Rate)

有害成功率 (Harmful Success Rate)

偏见分数 (Bias Score)

越狱抵抗 (Jailbreak Resistance)

总体安全分数 (Overall Safety Score)

🤝 贡献指南
欢迎提交 Issue 和 Pull Request！

📄 许可证
MIT License

text

这个完整的大模型安全与对齐项目提供了从基础安全防护到高级价值观对齐的完整解决方案。您可以根据具体需求选择使用不同的模块，也可以基于这个框架进行进一步的定制和扩展。