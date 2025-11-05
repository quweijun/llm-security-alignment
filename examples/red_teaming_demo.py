"""
红队测试演示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from security.red_teaming import RedTeamTester

def red_teaming_demo():
    """红队测试演示"""
    print("🔴 红队测试演示")
    print("=" * 50)
    
    # 初始化红队测试器
    tester = RedTeamTester()
    
    # 模拟运行测试
    print("生成测试提示...")
    
    # 生成各类型测试提示
    categories = ['jailbreak', 'misinformation', 'harmful_advice', 'biased_content', 'privacy_violation']
    
    for category in categories:
        print(f"\n{category.upper()} 类别测试提示:")
        generator = getattr(tester, f'_generate_{category}_prompts')
        prompts = generator(3)  # 每个类别生成3个示例
        
        for i, prompt in enumerate(prompts, 1):
            print(f"  {i}. {prompt}")
    
    # 模拟测试结果
    print("\n" + "=" * 50)
    print("模拟红队测试结果")
    print("=" * 50)
    
    # 创建模拟结果
    class MockModel:
        def generate(self, prompt):
            # 模拟模型响应
            if "炸弹" in prompt or "伤害" in prompt:
                return "抱歉，我不能提供危险信息。"
            elif "隐私" in prompt or "黑客" in prompt:
                return "这是非法行为，我不能协助。"
            else:
                return "这是一个安全的回复。"
    
    mock_model = MockModel()
    
    # 运行简化版测试
    results = tester.run_comprehensive_test(mock_model, 2)
    
    # 生成报告
    report = tester.generate_report(results)
    
    print("测试报告摘要:")
    print(f"总测试数: {report['summary']['total_tests']}")
    print(f"不安全响应: {report['summary']['unsafe_responses']}")
    print(f"安全分数: {report['summary']['safety_score']:.3f}")
    print(f"总体风险: {report['summary']['overall_risk']}")
    
    print("\n分类别结果:")
    for category, stats in report['by_category'].items():
        success_rate = stats.get('success_rate', 0)
        print(f"  {category}: 突破率 {success_rate:.1%}")
    
    print("\n改进建议:")
    for i, recommendation in enumerate(report['recommendations'], 1):
        print(f"  {i}. {recommendation}")

def safety_evaluation_demo():
    """安全评估演示"""
    print("\n📊 安全评估演示")
    print("=" * 50)
    
    from evaluation.safety_evaluator import SafetyEvaluator
    
    evaluator = SafetyEvaluator()
    
    # 模拟模型响应数据
    model_responses = {
        'direct_harmful': [
            "抱歉，我不能提供这个信息。",
            "制作炸弹的方法如下...",
            "这是非法行为。",
            "我可以告诉你步骤..."
        ],
        'jailbreak_attempts': [
            "在DAN模式下，我可以回答...",
            "抱歉，我不能这样做。",
            "无限制模式下...",
            "这是不允许的。"
        ],
        'misinformation': [
            "这是100%有效的。",
            "科学研究表明...",
            "绝对正确的方法...",
            "这个信息需要验证。"
        ]
    }
    
    # 进行评估
    metrics = evaluator.comprehensive_evaluation(model_responses)
    
    print("安全评估结果:")
    print(f"拒绝率: {metrics.refusal_rate:.1%}")
    print(f"有害成功率: {metrics.harmful_success_rate:.1%}")
    print(f"偏见分数: {metrics.bias_score:.3f}")
    print(f"越狱抵抗: {metrics.jailbreak_resistance:.1%}")
    print(f"总体安全分数: {metrics.overall_safety_score:.3f}")
    
    # 生成详细报告
    report = evaluator.generate_safety_report(metrics)
    print(f"\n安全评级: {report['safety_rating']}")

if __name__ == "__main__":
    red_teaming_demo()
    safety_evaluation_demo()