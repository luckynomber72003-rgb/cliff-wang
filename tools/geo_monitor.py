"""
GEO 自动化监测脚本
上海胜美科技

功能：
1. 定期测试 AI 对品牌的认知
2. 生成监测报告
3. 发送邮件通知

使用方法：
1. pip install openai anthropic schedule
2. 设置 API Key（环境变量或直接修改）
3. python geo_monitor.py
"""

import os
import json
import time
from datetime import datetime

# 尝试导入依赖
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("提示: pip install openai 以启用 ChatGPT 监测")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("提示: pip install anthropic 以启用 Claude 监测")

try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    print("提示: pip install schedule 以启用定时任务")

# ========== 配置 ==========

# API Keys（从环境变量读取，或直接填写）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your-anthropic-key")

# 品牌关键词（出现这些词表示被提及）
BRAND_KEYWORDS = [
    "胜美科技",
    "上海胜美",
    "王佳胜",
    "Cliff Wang",
    "王佳勝"
]

# 测试问题
TEST_QUERIES = [
    "GEO 优化公司推荐",
    "生成式引擎优化哪家好",
    "上海胜美科技是做什么的",
    "王佳胜是谁",
    "ChatGPT 搜索优化找谁做",
    "AI 搜索排名优化服务商"
]

# 报告保存目录
REPORT_DIR = "geo_reports"

# ========== 核心功能 ==========

def test_chatgpt(query):
    """测试 ChatGPT"""
    if not OPENAI_AVAILABLE:
        return {"error": "openai 未安装"}

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 使用便宜的模型
            messages=[{"role": "user", "content": query}],
            max_tokens=500
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

def test_claude(query):
    """测试 Claude"""
    if not ANTHROPIC_AVAILABLE:
        return {"error": "anthropic 未安装"}

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # 使用便宜的模型
            max_tokens=500,
            messages=[{"role": "user", "content": query}]
        )
        return {"response": response.content[0].text}
    except Exception as e:
        return {"error": str(e)}

def analyze_mention(text, keywords):
    """分析是否提及关键词"""
    if not text:
        return []

    text_lower = text.lower()
    mentioned = []
    for kw in keywords:
        if kw.lower() in text_lower:
            mentioned.append(kw)
    return mentioned

def run_monitoring():
    """执行一次监测"""
    print(f"\n{'='*50}")
    print(f"GEO 监测开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    results = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total_queries": len(TEST_QUERIES),
            "chatgpt_mentions": 0,
            "claude_mentions": 0
        },
        "tests": []
    }

    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"[{i}/{len(TEST_QUERIES)}] 测试: {query}")

        test_result = {
            "query": query,
            "chatgpt": None,
            "claude": None
        }

        # ChatGPT
        gpt_result = test_chatgpt(query)
        if "response" in gpt_result:
            mentions = analyze_mention(gpt_result["response"], BRAND_KEYWORDS)
            test_result["chatgpt"] = {
                "mentioned": mentions,
                "response_preview": gpt_result["response"][:300] + "..."
            }
            if mentions:
                results["summary"]["chatgpt_mentions"] += 1
                print(f"  ChatGPT: ✅ 提及 {mentions}")
            else:
                print(f"  ChatGPT: ❌ 未提及")
        else:
            test_result["chatgpt"] = {"error": gpt_result.get("error")}
            print(f"  ChatGPT: ⚠️ 错误 - {gpt_result.get('error')}")

        time.sleep(1)

        # Claude
        claude_result = test_claude(query)
        if "response" in claude_result:
            mentions = analyze_mention(claude_result["response"], BRAND_KEYWORDS)
            test_result["claude"] = {
                "mentioned": mentions,
                "response_preview": claude_result["response"][:300] + "..."
            }
            if mentions:
                results["summary"]["claude_mentions"] += 1
                print(f"  Claude:  ✅ 提及 {mentions}")
            else:
                print(f"  Claude:  ❌ 未提及")
        else:
            test_result["claude"] = {"error": claude_result.get("error")}
            print(f"  Claude:  ⚠️ 错误 - {claude_result.get('error')}")

        results["tests"].append(test_result)
        time.sleep(2)

    return results

def save_report(results):
    """保存报告"""
    # 创建报告目录
    os.makedirs(REPORT_DIR, exist_ok=True)

    # 保存 JSON
    filename = f"{REPORT_DIR}/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n报告已保存: {filename}")
    return filename

def print_summary(results):
    """打印总结"""
    print(f"\n{'='*50}")
    print("监测总结")
    print(f"{'='*50}")
    print(f"测试问题数: {results['summary']['total_queries']}")
    print(f"ChatGPT 提及次数: {results['summary']['chatgpt_mentions']}")
    print(f"Claude 提及次数: {results['summary']['claude_mentions']}")

    total = results['summary']['total_queries']
    gpt_rate = results['summary']['chatgpt_mentions'] / total * 100 if total > 0 else 0
    claude_rate = results['summary']['claude_mentions'] / total * 100 if total > 0 else 0

    print(f"\nChatGPT 提及率: {gpt_rate:.1f}%")
    print(f"Claude 提及率: {claude_rate:.1f}%")

    if gpt_rate == 0 and claude_rate == 0:
        print("\n⚠️ 品牌尚未被 AI 识别，需要加强 GEO 优化")
    elif gpt_rate < 50 or claude_rate < 50:
        print("\n📈 品牌有一定认知度，继续优化可提升")
    else:
        print("\n🎉 品牌 AI 认知度良好！")

def job():
    """定时任务"""
    results = run_monitoring()
    save_report(results)
    print_summary(results)

# ========== 主程序 ==========

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        # 定时模式
        if not SCHEDULE_AVAILABLE:
            print("错误: 请先安装 schedule (pip install schedule)")
            sys.exit(1)

        print("GEO 监测服务已启动")
        print("将在每周一 9:00 自动运行")
        print("按 Ctrl+C 停止\n")

        schedule.every().monday.at("09:00").do(job)

        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        # 单次运行
        results = run_monitoring()
        save_report(results)
        print_summary(results)
