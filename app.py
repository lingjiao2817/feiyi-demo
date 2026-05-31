import streamlit as st
import os
import requests
from openai import OpenAI

# ------------------------------
# API 配置
# ------------------------------
API_KEY = "sk-e75e8926aaed40d48ddb6e3a55201c51"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-plus"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

DIFY_API_URL = "https://udify.app/chat/eCOlOS9PT3LZQiXP"

# ------------------------------
# 素材路径
# ------------------------------
REMOTE_VIDEO_URL = None
LOCAL_VIDEO_PATH = "assets/demo_video.mp4"

STANDARD_IMG = "assets/standard.png"
STEP_IMAGES = [
    "assets/step1.png",
    "assets/step2.png",
    "assets/step3.png",
    "assets/step4.png",
]

# ------------------------------
# 全局样式
# ------------------------------
def set_custom_style():
    st.markdown("""
    <style>
        .stApp {
            background-color: #fdf8f2;
        }
        h1, h2, h3, h4 {
            color: #c8102e;
            font-family: "Microsoft YaHei", sans-serif;
        }
        div[data-testid="stVerticalBlock"] > div[style*="block"] {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .stButton > button {
            background: #c8102e;
            color: white;
            border-radius: 8px;
            border: none;
            width: 100%;
            height: 48px;
            font-weight: 500;
            font-size: 16px;
            transition: background 0.2s;
        }
        .stButton > button:hover {
            background: #a00c24;
        }
        .stAlert {
            background-color: #f8ece0;
        }
        blockquote {
            background-color: #F3F4F6;
            padding: 12px;
            border-left: 4px solid #9CA3AF;
            margin: 16px 0;
        }
        .observe-bar {
            background-color: #FFFBEB;
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 16px;
        }
        .css-1d391kg {
            background-color: #f8ece0;
        }
    </style>
    """, unsafe_allow_html=True)

# ------------------------------
# 工具函数
# ------------------------------
def go_to(page):
    st.query_params.step = page

def show_image(path, caption="", width=None):
    try:
        if os.path.exists(path):
            st.image(path, caption=caption, width=width)
        else:
            st.warning(f"图片缺失: {os.path.basename(path)}")
    except Exception as e:
        st.warning(f"加载图片失败: {str(e)}")

def show_video():
    if REMOTE_VIDEO_URL:
        st.video(REMOTE_VIDEO_URL)
    elif os.path.exists(LOCAL_VIDEO_PATH):
        st.video(LOCAL_VIDEO_PATH)
    else:
        st.info("视频准备中，请稍后观看。")

def send_to_dify(message, session_id=None):
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "query": message,
            "user": session_id or "anonymous",
            "response_mode": "blocking"
        }
        api_url = DIFY_API_URL if DIFY_API_URL.endswith("/api/v1/chat-messages") else f"{DIFY_API_URL}/api/v1/chat-messages"
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json().get("answer", "")
        else:
            return None
    except Exception:
        return None

# ------------------------------
# 页面：诊学
# ------------------------------
def page_diagnosis():
    st.title("诊学 · 了解你的基础")

    if "dify_messages" not in st.session_state:
        st.session_state.dify_messages = []
        initial_response = send_to_dify("你好")
        if initial_response:
            st.session_state.dify_messages.append({"role": "assistant", "content": initial_response})
        else:
            st.session_state.dify_messages.append({"role": "assistant", "content": "欢迎来到英歌舞内旋槌教学，请告诉我你之前练过吗？"})

    for msg in st.session_state.dify_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if "dify_answered" not in st.session_state:
        st.subheader("你之前练过英歌舞内旋槌吗？")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("没练过，从头学", use_container_width=True):
                st.session_state.dify_answered = True
                st.session_state.dify_messages.append({"role": "user", "content": "没练过，从头学"})
                response = send_to_dify("没练过，从头学")
                if response:
                    st.session_state.dify_messages.append({"role": "assistant", "content": response})
                go_to("授法")
                st.query_params.branch = "new"
                st.rerun()
        with col2:
            if st.button("练过，直接对比", use_container_width=True):
                st.session_state.dify_answered = True
                st.session_state.dify_messages.append({"role": "user", "content": "练过，直接对比"})
                response = send_to_dify("练过，直接对比")
                if response:
                    st.session_state.dify_messages.append({"role": "assistant", "content": response})
                go_to("陪练")
                st.query_params.branch = "experienced"
                st.rerun()
        st.markdown(":gray[选择后系统会为你定制学习路径]")
    else:
        user_input = st.chat_input("请输入你的问题")
        if user_input:
            st.session_state.dify_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            response = send_to_dify(user_input)
            if response:
                st.session_state.dify_messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.write(response)
            else:
                st.error("抱歉，AI服务暂时不可用。")

# ------------------------------
# 页面：授法
# ------------------------------
def page_teaching():
    st.title("授法 · 观看大师示范")

    st.markdown("""
    <div class="observe-bar">
        <strong>观察要点</strong> —— 
        握槌：掐而不紧、松而不滑 | 
        发力：手腕为轴，手臂固定 | 
        棒身：全程与地面平行
    </div>
    """, unsafe_allow_html=True)

    st.subheader("视频示范")
    show_video()

    if st.button("看完了，进入拆解学习", use_container_width=True):
        go_to("拆解")

# ------------------------------
# 页面：拆解
# ------------------------------
def page_decomposition():
    st.title("拆解 · 四步分解学习")

    cols = st.columns(4)
    steps = [
        {"title": "第1步 预备握槌", "image": STEP_IMAGES[0], "desc": "双脚与肩同宽，膝盖微屈，双手握槌中部"},
        {"title": "第2步 内旋启动", "image": STEP_IMAGES[1], "desc": "手腕为轴发力，手臂固定，带动棒身旋转"},
        {"title": "第3步 水平控槌", "image": STEP_IMAGES[2], "desc": "棒身转至水平，双手微抬，两端对齐"},
        {"title": "第4步 还原定型", "image": STEP_IMAGES[3], "desc": "手腕平稳复位，棒身回到胸前"},
    ]
    for i, step in enumerate(steps):
        with cols[i]:
            st.subheader(step["title"])
            show_image(step["image"], width=150)
            st.caption(step["desc"])

    st.markdown("""
    <blockquote>
        传承人陈来发说："手腕是轴，手臂是架，只转手不甩臂，内旋才标准。"
    </blockquote>
    """, unsafe_allow_html=True)

    if st.button("学会了，进入陪练对比", use_container_width=True):
        go_to("陪练")

# ------------------------------
# 页面：陪练
# ------------------------------
def page_practice():
    st.title("陪练 · 左右对比纠错")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("标准动作")
        show_image(STANDARD_IMG, width=300)
    with col2:
        st.subheader("你的动作")
        uploaded = st.file_uploader("上传你的动作照片", type=["png", "jpg", "jpeg"])
        if uploaded:
            st.image(uploaded, caption="你的练习", width=300)
            st.success("已上传，请对照左侧标准图自查")
        else:
            st.info("点击上方按钮上传照片")

    st.divider()

    with st.expander("常见错误自查", expanded=True):
        st.markdown("""
        - 握槌过紧/过松 → 调整手指力度  
        - 手肘外撇、棒身倾斜 → 手肘内收  
        - 用手臂发力而非手腕 → 放松大臂  
        - 还原不到位 → 手腕完整复位
        """)

    if st.button("提交对比，完成学习", use_container_width=True):
        go_to("验成")

# ------------------------------
# 页面：验成
# ------------------------------
def page_achievement():
    st.title("恭喜完成学习")

    if "self_check" not in st.session_state:
        st.session_state.self_check = {
            "手肘内收": False,
            "棒身水平": False,
            "手腕发力": False,
            "握槌稳固": False
        }

    st.subheader("自检清单")
    for item in st.session_state.self_check:
        st.session_state.self_check[item] = st.checkbox(item, value=st.session_state.self_check[item])

    all_checked = all(st.session_state.self_check.values())

    if all_checked:
        st.success("恭喜解锁内旋槌技能！")
        st.subheader("学习路径回顾")
        for step in ["诊学", "授法", "拆解", "陪练", "验成"]:
            st.markdown(f"- {step}")
    else:
        st.info("请逐项确认后解锁")

    if st.button("重新开始学习", use_container_width=True):
        st.query_params.clear()
        st.session_state.pop("self_check", None)
        st.session_state.pop("dify_messages", None)
        st.session_state.pop("dify_answered", None)
        go_to("诊学")
        st.rerun()

# ------------------------------
# 侧边栏进度
# ------------------------------
def show_sidebar_progress():
    steps = ["诊学", "授法", "拆解", "陪练", "验成"]
    current = st.query_params.get("step", "诊学")
    current_idx = steps.index(current) if current in steps else 0

    st.sidebar.title("学习进度")
    for i, name in enumerate(steps):
        if i == current_idx:
            st.sidebar.button(name, key=f"nav_{name}", type="primary", use_container_width=True)
        elif i < current_idx:
            if st.sidebar.button(name, key=f"nav_{name}", use_container_width=True):
                go_to(name)
                st.rerun()
        else:
            st.sidebar.button(name, key=f"nav_{name}", disabled=True, use_container_width=True)

# ------------------------------
# 底部状态栏
# ------------------------------
def show_status_bar():
    current = st.query_params.get("step", "诊学")
    branch = st.query_params.get("branch", "")

    path_parts = ["诊学"]
    if current in ["授法", "拆解", "陪练", "验成"]:
        path_parts.append("授法")
    if current in ["拆解", "陪练", "验成"]:
        path_parts.append("拆解")
    if current in ["陪练", "验成"]:
        path_parts.append("陪练")
    if current == "验成":
        path_parts.append("验成")

    path_str = " -> ".join(path_parts)
    st.markdown(f"---\n**当前页面**: {current} | **学习路径**: {path_str}")

# ------------------------------
# AI 问答
# ------------------------------
def show_ai_chat():
    with st.expander("AI问答 · 有任何问题都可以问我"):
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt = st.chat_input("输入你的问题")
        if prompt:
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            try:
                messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history]
                response = client.chat.completions.create(model=MODEL_NAME, messages=messages)
                answer = response.choices[0].message.content
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                with st.chat_message("assistant"):
                    st.write(answer)
            except Exception:
                error_msg = "抱歉，AI服务暂时不可用，请稍后再试。"
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                with st.chat_message("assistant"):
                    st.error(error_msg)

# ------------------------------
# 主入口
# ------------------------------
def main():
    st.set_page_config(page_title="非遗数承 · 英歌舞内旋槌教学", layout="wide")
    set_custom_style()
    show_sidebar_progress()

    current = st.query_params.get("step", "诊学")
    if current == "诊学":
        page_diagnosis()
    elif current == "授法":
        page_teaching()
    elif current == "拆解":
        page_decomposition()
    elif current == "陪练":
        page_practice()
    elif current == "验成":
        page_achievement()
    else:
        go_to("诊学")
        st.rerun()

    show_status_bar()
    show_ai_chat()

if __name__ == "__main__":
    main()