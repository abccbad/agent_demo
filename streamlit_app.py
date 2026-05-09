import json
import requests
import streamlit as st
import textwrap
# 初始化会话

if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False
if "input_value" not in st.session_state:
    st.session_state.input_value = ""



MODEL_URL = "https://api.deepseek.com/chat/completions"

# 重构写实商圈数据：开放多业态 + 严格按你给定全套人群画像占比
PRODUCT_DATA = {
    "有机朝阳大米": [
        {
            "城市": "北京",
            "渠道": "山姆会员店",
            "销量": "11.2吨",
            "同比增速": "40%",
            "周边业态": {
                "超市便利店": "高占比",
                "快餐厅": "中高占比",
                "咖啡厅": "中等占比",
                "茶饮果汁": "中等占比",
                "面包甜点": "中低占比",
                "火锅": "低占比",
                "生鲜卖场": "高占比",
                "住宅底商": "高占比"
            },
            "人群画像": {
                "人口结构": {"常驻人口": "65%", "流动人口": "35%"},
                "常驻年龄分布": {
                    "18-24岁": "12%", "25-30岁": "18%", "31-35岁": "22%",
                    "36-40岁": "20%", "41-45岁": "15%", "46-60岁": "10%", "60岁以上": "3%"
                },
                "流动年龄分布": {
                    "18-24岁": "25%", "25-30岁": "30%", "31-35岁": "22%",
                    "36-40岁": "13%", "41-45岁": "6%", "46-60岁": "3%", "60岁以上": "1%"
                },
                "常驻消费水平": {"低": "8%", "次低": "15%", "中": "32%", "次高": "30%", "高": "15%"},
                "流动消费水平": {"低": "12%", "次低": "20%", "中": "35%", "次高": "25%", "高": "8%"},
                "常驻性别": {"男": "48%", "女": "52%"},
                "流动性别": {"男": "55%", "女": "45%"}
            },
            "同品类对标": "高于同城同类型商超大米平均销量及增速，中高端家庭采购需求旺盛，竞品以普通平价大米为主，本品差异化优势明显"
        },
        {
            "城市": "北京",
            "渠道": "盒马鲜生",
            "销量": "9.5吨",
            "同比增速": "38%",
            "周边业态": {
                "茶饮果汁": "高占比",
                "咖啡厅": "高占比",
                "面包甜点": "中高占比",
                "快餐厅": "中等占比",
                "超市便利店": "中等占比",
                "火锅": "中低占比",
                "美妆零售": "中高占比",
                "商场配套商业": "高占比"
            },
            "人群画像": {
                "人口结构": {"常驻人口": "45%", "流动人口": "55%"},
                "常驻年龄分布": {
                    "18-24岁": "15%", "25-30岁": "25%", "31-35岁": "24%",
                    "36-40岁": "18%", "41-45岁": "10%", "46-60岁": "6%", "60岁以上": "2%"
                },
                "流动年龄分布": {
                    "18-24岁": "28%", "25-30岁": "32%", "31-35岁": "20%",
                    "36-40岁": "12%", "41-45岁": "5%", "46-60岁": "2%", "60岁以上": "1%"
                },
                "常驻消费水平": {"低": "5%", "次低": "12%", "中": "28%", "次高": "35%", "高": "20%"},
                "流动消费水平": {"低": "8%", "次低": "15%", "中": "30%", "次高": "32%", "高": "15%"},
                "常驻性别": {"男": "45%", "女": "55%"},
                "流动性别": {"男": "48%", "女": "52%"}
            },
            "同品类对标": "处于同城生鲜商超中上水平，年轻流动客群偏好高品质粮油，平价竞品分流有限，增速稳定向好"
        },
        {
            "城市": "郑州",
            "渠道": "家家悦",
            "销量": "6.9吨",
            "同比增速": "24%",
            "周边业态": {
                "超市便利店": "高占比",
                "快餐厅": "中高占比",
                "面包甜点": "中等占比",
                "茶饮果汁": "中低占比",
                "火锅": "中等占比",
                "社区门诊": "中高占比",
                "老旧社区底商": "高占比"
            },
            "人群画像": {
                "人口结构": {"常驻人口": "78%", "流动人口": "22%"},
                "常驻年龄分布": {
                    "18-24岁": "8%", "25-30岁": "12%", "31-35岁": "16%",
                    "36-40岁": "22%", "41-45岁": "20%", "46-60岁": "18%", "60岁以上": "4%"
                },
                "流动年龄分布": {
                    "18-24岁": "20%", "25-30岁": "28%", "31-35岁": "25%",
                    "36-40岁": "15%", "41-45岁": "8%", "46-60岁": "3%", "60岁以上": "1%"
                },
                "常驻消费水平": {"低": "18%", "次低": "25%", "中": "38%", "次高": "15%", "高": "4%"},
                "流动消费水平": {"低": "22%", "次低": "28%", "中": "35%", "次高": "12%", "高": "3%"},
                "常驻性别": {"男": "49%", "女": "51%"},
                "流动性别": {"男": "58%", "女": "42%"}
            },
            "同品类对标": "低于同城核心商圈商超销量及增速，周边以刚需平价消费为主，高端粮油接受度偏低，增量空间受限"
        }
    ],
    "大连金州大樱桃": [
        {
            "城市": "杭州",
            "渠道": "盒马鲜生",
            "销量": "8.6万斤",
            "同比增速": "37%",
            "周边业态": {
                "茶饮果汁": "高占比",
                "咖啡厅": "高占比",
                "火锅": "中高占比",
                "面包甜点": "中高占比",
                "快餐厅": "中等占比",
                "精品零售": "高占比",
                "商场休闲业态": "高占比"
            },
            "人群画像": {
                "人口结构": {"常驻人口": "40%", "流动人口": "60%"},
                "常驻年龄分布": {
                    "18-24岁": "18%", "25-30岁": "28%", "31-35岁": "25%",
                    "36-40岁": "15%", "41-45岁": "8%", "46-60岁": "5%", "60岁以上": "1%"
                },
                "流动年龄分布": {
                    "18-24岁": "30%", "25-30岁": "35%", "31-35岁": "22%",
                    "36-40岁": "9%", "41-45岁": "3%", "46-60岁": "1%", "60岁以上": "0%"
                },
                "常驻消费水平": {"低": "4%", "次低": "10%", "中": "25%", "次高": "38%", "高": "23%"},
                "流动消费水平": {"低": "6%", "次低": "12%", "中": "28%", "次高": "35%", "高": "19%"},
                "常驻性别": {"男": "44%", "女": "56%"},
                "流动性别": {"男": "46%", "女": "54%"}
            },
            "同品类对标": "明显高于同城生鲜门店同类水果销量，年轻高消费流动人群集中，高端时令水果接受度高，竞品多为普通平价水果"
        }
    ]
}

def get_ai_answer(question, api_key):


    # 1. 使用 dedent 去除多余缩进
    # 2. 将格式要求放在前面，作为 System Prompt 或更高优先级的要求
    prompt = textwrap.dedent(f"""
        你是一个专业的数据分析师。请针对用户的具体问题进行精准分析，禁止输出无关内容。
        
        【核心要求】
        1. 只分析用户问题中提到的具体城市、渠道和商品
        2. 禁止输出其他城市、渠道或商品的数据
        3. 严格按照六大模块格式输出
        
        【格式约束】
        1. 必须使用 Markdown 粗体格式作为标题（例如：**一、销量基础概况**）。
        2. 标题后必须紧跟一个空行。
        3. 内容输出从标题后的第一行开始，段落间无多余空行。
        4. 模块间保持一个空行。
        
        【输出模板】
        **一、销量基础概况**

        [只分析用户问题中提到的商品数据]

        **二、周边业态环境数据分析**

        [只分析用户问题中提到的渠道业态]

        **三、常驻及流动人口画像占比分析**

        [只分析用户问题中提到的人群数据]

        **四、同城同渠道同品类交易对标分析**

        [只分析用户问题中提到的商品对标]

        **五、销量高低及市场表现综合原因总结**

        [只总结用户问题中提到的商品表现]

        **六、渠道经营及品类优化建议**

        [只针对用户问题中提到的商品提供建议]

        用户提问：{question}
        商圈数据：{json.dumps(PRODUCT_DATA, ensure_ascii=False, indent=2)}
        """)




    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    }
    try:
        res = requests.post(MODEL_URL, headers=headers, json=payload, timeout=30)
        return res.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"接口请求失败：{str(e)}"

def main():
    st.set_page_config(
        page_title="辽宁优品 · 智能市场分析系统",
        page_icon="📊",
        layout="wide"
    )

    # 侧边栏配置密钥 + 示例问题
    with st.sidebar:
        st.markdown("### 🔑 接口密钥配置")
        input_key = st.text_input("Deepseek API_KEY", value=st.session_state.api_key, type="password")
        if st.button("保存密钥", type="primary", use_container_width=True):
            st.session_state.api_key = input_key
            st.success("密钥已保存")

        st.divider()
        st.markdown("### 💡 示例提问")
        example_qs = [
            "北京山姆会员店有机朝阳大米销量表现如何",
            "杭州盒马鲜生大连金州大樱桃销量原因分析",
            "郑州家家悦有机朝阳大米销量偏低原因分析"
        ]
        for i, q in enumerate(example_qs):
            if st.button(q, key=f"eq_{i}", use_container_width=True):
                st.session_state.input_value = q
                st.rerun()



    # 全局样式
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600&display=swap');
    * {font-family: 'Noto Sans SC', sans-serif !important;font-size:14px !important;box-sizing:border-box;}
    #MainMenu, footer, header {visibility:hidden;}
    .block-container {padding:0 !important;max-width:100% !important;}
    .title-text {font-size:16px !important;font-weight:600;}
    .u-bub {background:#e5392e;color:#fff;border-radius:14px 14px 3px 14px;padding:12px 16px;max-width:70%;line-height:1.6;}
    .a-bub {background:#f3f4f8;border-radius:3px 14px 14px 14px;padding:12px 16px;max-width:85%;line-height:1.8;color:#1e293b;white-space:pre-wrap;}
    .u-msg {display:flex;justify-content:flex-end;margin:12px 0;}
    .a-msg {display:flex;gap:10px;margin:12px 0;}
    .a-av {width:32px;height:32px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;}
    .chat-container {background:#fff;border:1.5px solid #e8eaf0;border-radius:12px;padding:20px;height:450px;overflow-y:auto;display:flex;flex-direction:column;gap:8px;}
    .chat-empty {display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:#94a3b8;}
    .flow-bar {display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:8px;background:#f8faff;border:1px solid #dde5ff;border-radius:8px;padding:12px;margin-bottom:14px;}
    .fn {background:#fff;border:1px solid #c7d2fe;border-radius:6px;padding:6px 12px;color:#4338ca;font-weight:500;}
    .fa {color:#a5b4fc;}
    ::-webkit-scrollbar {width:6px;}
    ::-webkit-scrollbar-thumb {background:#cbd5e1;border-radius:3px;}

    /* 针对 text_area 设置边框和阴影 */
    div[data-baseweb="textarea"] {
        border: 2px solid #dde5ff !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05) !important;
        border-radius: 8px !important;
        background-color: #ffffff !important;
    }

    /* 当鼠标点击输入框时，给边框一个高亮颜色，阴影加深一点 */
    div[data-baseweb="textarea"]:focus-within {
        border: 2px solid #4f46e5 !important;
        box-shadow: 0 4px 8px rgba(79, 70, 229, 0.15) !important;
    }

    /* 确保内部文字区域背景透明 */
    textarea {
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)


    # 顶部标题栏
    st.markdown('<div style="display:flex;align-items:center;gap:10px;padding:0 24px;height:52px;background:#fff;border-bottom:1.5px solid #e8eaf0;position:sticky;top:0;z-index:200;">'
    '<span style="font-size:18px;">📊</span>'
    '<span class="title-text">辽宁优品 · 智能市场分析系统</span>'
    '<div style="flex:1;"></div>'
    '<span style="width:7px;height:7px;border-radius:50%;background:#22c55e;display:inline-block;"></span>'
    '<span>系统运行正常</span>'
    '</div>', unsafe_allow_html=True)

    # 顶部说明栏
    st.markdown('<div class="flow-bar"><span class="fn">多维数据支撑</span><span class="fa">→</span><span class="fn">POI业态+人群画像+同品类对标</span><span class="fa">→</span><span class="fn">自动生成专业分析报告</span></div>', unsafe_allow_html=True)

    # 唯一对话框
    chat_container = st.empty()

    def draw_chat(loading=False):
        html = '<div class="chat-container">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                html += f'<div class="u-msg"><div class="u-bub">{msg["content"]}</div></div>'
            else:
                # 处理 Markdown 格式
                content = msg["content"]
                # 确保 Markdown 标题格式正确
                content = content.replace('**一、', '\n\n**一、')
                content = content.replace('**二、', '\n\n**二、')
                content = content.replace('**三、', '\n\n**三、')
                content = content.replace('**四、', '\n\n**四、')
                content = content.replace('**五、', '\n\n**五、')
                content = content.replace('**六、', '\n\n**六、')
                html += f'<div class="a-msg"><div class="a-av">📊</div><div class="a-bub">{content}</div></div>'
        if loading:
            html += '<div class="a-msg"><div class="a-av">📊</div><div class="a-bub">正在分析，请稍候……</div></div>'
        html += '</div>'
        chat_container.markdown(html, unsafe_allow_html=True)




    # 初始空状态
    if not st.session_state.chat_history:
        chat_container.markdown('''
        <div class="chat-container">
            <div class="chat-empty">
                <div style="font-size:40px;margin-bottom:12px;">📈</div>
                <div class="title-text" style="margin-bottom:8px;">智能市场分析报告系统</div>
                <div>依托周边POI、人群画像、同品类交易数据，自动生成标准化分析报告</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        draw_chat(loading=st.session_state.is_loading)

    # 清空输入函数
    def clear_input():
        st.session_state.input_value = ""
        st.session_state.chat_history = []
        st.session_state.is_loading = False



    # 输入框
    # user_in = st.text_input(
    #     label="输入问题",
    #     placeholder="请输入城市、渠道、商品相关分析问题...",
    #     value=st.session_state.input_value,
    #     label_visibility="collapsed"
    # )

    user_in = st.text_area(
        label="输入问题",
        placeholder="请输入城市、渠道、商品相关分析问题...",
        value=st.session_state.input_value,
        label_visibility="collapsed",
        height=80  # 这里可以直接设置高度，单位为像素
    )

    col1, col2, col3 = st.columns([6,1,1])
    with col2:
        send_btn = st.button("发送 →", type="primary", use_container_width=True)
    with col3:
        clear_btn = st.button("清空", use_container_width=True, on_click=clear_input)

    # 发送按钮逻辑
    if send_btn and user_in.strip() and not st.session_state.is_loading:
        if not st.session_state.api_key:
            st.warning("请先在左侧侧边栏输入并保存 Deepseek API_KEY")
        else:
            question = user_in.strip()
            st.session_state.chat_history.append({"role": "user", "content": question})
            st.session_state.is_loading = True
            st.session_state.input_value = ""  # 清空输入框
            draw_chat(loading=True)
            st.rerun()



    # 获取答案逻辑
    if st.session_state.is_loading and len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1]["role"] == "user":
        ans = get_ai_answer(st.session_state.chat_history[-1]["content"], st.session_state.api_key)
        st.session_state.chat_history.append({"role": "assistant", "content": ans})
        st.session_state.is_loading = False
        draw_chat(loading=False)


if __name__ == "__main__":
    main()
