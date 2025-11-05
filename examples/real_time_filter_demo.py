"""
实时过滤演示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from security.output_filtering import SafetyFilter, BiasDetector
from alignment.safety_finetuning import ConstitutionalAI

class RealTimeSafetySystem:
    """实时安全系统"""
    
    def __init__(self):
        self.safety_filter = SafetyFilter()
        self.bias_detector = BiasDetector()
        self.constitutional_ai = ConstitutionalAI()
        self.conversation_history = []
    
    def process_user_input(self, user_input: str) -> str:
        """处理用户输入"""
        # 安全过滤
        filter_result = self.safety_filter.filter_response(user_input)
        
        if filter_result['action'] == 'block':
            return filter_result['filtered_text']
        
        # 添加到对话历史
        self.conversation_history.append({'role': 'user', 'content': user_input})
        
        # 模拟模型响应
        model_response = self._simulate_model_response(user_input)
        
        # 宪法AI修订
        revised_response = self.constitutional_ai.apply_constitutional_feedback(
            user_input, model_response
        )
        
        # 添加到对话历史
        self.conversation_history.append({'role': 'assistant', 'content': revised_response})
        
        # 实时监控
        monitoring = self.safety_filter.real_time_monitor(self.conversation_history)
        
        if monitoring['recommendation'] == 'terminate':
            return "对话因安全原因已终止。"
        
        return revised_response
    
    def _simulate_model_response(self, user_input: str) -> str:
        """模拟模型响应"""
        # 简化的响应逻辑
        if '伤害' in user_input or '炸弹' in user_input:
            return "抱歉，我不能提供危险信息。"
        elif '隐私' in user_input or '黑客' in user_input:
            return "这是非法行为，我不能协助。"
        elif '歧视' in user_input:
            return "我们应该平等对待所有人。"
        else:
            return "这是一个安全的回复。"
    
    def get_safety_report(self) -> dict:
        """获取安全报告"""
        monitoring = self.safety_filter.real_time_monitor(self.conversation_history)
        
        # 分析偏见
        assistant_responses = [
            msg['content'] for msg in self.conversation_history 
            if msg['role'] == 'assistant'
        ]
        
        bias_analysis = self.bias_detector.analyze_model_responses(
            [msg['content'] for msg in self.conversation_history if msg['role'] == 'user'],
            assistant_responses
        )
        
        return {
            'conversation_risk': monitoring['conversation_risk'],
            'risk_level': monitoring['risk_level'],
            'bias_score': bias_analysis['average_bias_score'],
            'message_count': len(self.conversation_history),
            'safety_status': '正常' if monitoring['risk_level'] == 'low' else '警告'
        }

def interactive_safety_demo():
    """交互式安全演示"""
    print("🔒 交互式安全系统演示")
    print("=" * 50)
    print("输入 'quit' 退出，'report' 查看安全报告")
    print("=" * 50)
    
    safety_system = RealTimeSafetySystem()
    
    while True:
        try:
            user_input = input("\n用户: ").strip()
            
            if user_input.lower() == 'quit':
                print("对话结束。")
                break
            elif user_input.lower() == 'report':
                report = safety_system.get_safety_report()
                print("\n安全报告:")
                print(f"对话风险: {report['conversation_risk']:.3f}")
                print(f"风险等级: {report['risk_level']}")
                print(f"偏见分数: {report['bias_score']:.3f}")
                print(f"消息数量: {report['message_count']}")
                print(f"安全状态: {report['safety_status']}")
                continue
            elif not user_input:
                continue
            
            # 处理用户输入
            response = safety_system.process_user_input(user_input)
            print(f"助手: {response}")
            
            # 检查是否需要终止对话
            if "终止" in response:
                print("对话因安全原因自动终止。")
                break
        
        except KeyboardInterrupt:
            print("\n\n对话被用户中断。")
            break
        except Exception as e:
            print(f"系统错误: {e}")

if __name__ == "__main__":
    interactive_safety_demo()