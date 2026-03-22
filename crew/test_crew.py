# PhysicsHub CrewAI 测试脚本
from crewai import Agent, Task, Crew
import os

print("🧪 测试 CrewAI 配置")
print("=" * 40)

# 检查API key
api_key = os.getenv("KIMI_API_KEY")
if not api_key:
    print("⚠️  未设置 KIMI_API_KEY")
    print("   请运行: export KIMI_API_KEY='your-key'")
    print("   或者使用虚拟模式测试")
    use_mock = True
else:
    print(f"✅ API Key 已设置: {api_key[:8]}...")
    use_mock = False

print()

# 创建测试Agent
try:
    from langchain_openai import ChatOpenAI
    
    if use_mock:
        print("📝 使用模拟模式（无API调用）")
    else:
        llm = ChatOpenAI(
            model="kimi-coding/k2p5",
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1",
            temperature=0.7
        )
        print("✅ LLM 配置成功")
    
    # 创建测试Agent
    test_agent = Agent(
        role='测试员',
        goal='验证CrewAI安装',
        backstory='你是一位测试工程师',
        verbose=False
    )
    print("✅ Agent 创建成功")
    
    # 创建测试任务
    test_task = Task(
        description='报告CrewAI安装状态',
        agent=test_agent,
        expected_output='安装状态报告'
    )
    print("✅ Task 创建成功")
    
    print()
    print("=" * 40)
    print("✅ 所有测试通过！")
    print()
    print("🚀 可以运行完整团队:")
    print("   python3 ~/Desktop/PhysicsHub/crew/physics_hub_team.py")
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("   请运行: pip3 install crewai langchain-openai")
    
except Exception as e:
    print(f"❌ 错误: {e}")
