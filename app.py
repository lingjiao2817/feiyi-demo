import streamlit as st

# ==============================
# 素材配置（本地图片 + 远程视频）
# ==============================
TEACH_VIDEO_URL = "https://raw.githubusercontent.com/zx327/-/main/vidio1.mp4"
STEP_IMAGES = [
    "assets/step1.png",
    "assets/step2.png",
    "assets/step3.png",
    "assets/step4.png",
]
STANDARD_IMG = "assets/standard.png"

# Dify 对话链接（侧边栏 iframe 嵌入）
DIFY_AI_URL = "https://udify.app/chat/eCOlOS9PT3LZQiXP"

# ==============================
# 全局样式
# ==============================
def set_custom_style():
    st.markdown("""
    <style>
        .stApp { background-color: #fdf8f2; }
        h1, h2, h3, h4 { color: #c8102e; font-family: "Microsoft YaHei", sans-serif; }
        div[data-testid="stVerticalBlock"] > div[style*="block"] {
            background: white; border-radius: 12px; padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .stButton > button {
            background: #c8102e; color: white; border-radius: 8px;
            border: none; width: 100%; height: 48px; font-weight: 500;
            font-size: 16px; transition: background 0.2s;
        }
        .stButton > button:hover { background: #a00c24; }
        .stAlert { background-color: #f8ece0; }
        blockquote {
            background-color: #F3F4F6; padding: 12px;
            border-left: 4px solid #9CA3AF; margin: 16px 0;
        }
        .observe-bar {
            background-color: #FFFBEB; padding: 12px; border-radius: 4px;
            margin-bottom: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

# ==============================
# 页面跳转
# ==============================
def go_to(page):
    st.query_params.step = page

# ==============================
# 页面1：诊学
# ==============================
def page_diagnosis():
    st.title("诊学 · 了解你的基础")

    if "dify_messages" not in st.session_state:
        st.session_state.dify_messages = []
    if not st.session_state.dify_messages:
        st.session_state.dify_messages.append(
            {"role": "assistant", "content": "欢迎来到英歌舞内旋槌教学，请告诉我你之前练过吗？"}
        )

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
                st.query_params.branch = "new"
                go_to("授法")
                st.rerun()
        with col2:
            if st.button("练过，直接对比", use_container_width=True):
                st.session_state.dify_answered = True
                st.session_state.dify_messages.append({"role": "user", "content": "练过，直接对比"})
                st.query_params.branch = "experienced"
                go_to("陪练")
                st.rerun()
        st.markdown(":gray[选择后系统会为你定制学习路径]")
    else:
        user_input = st.chat_input("继续提问")
        if user_input:
            st.session_state.dify_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.dify_messages.append(
                {"role": "assistant", "content": "感谢你的提问，你可以随时在侧边栏向 AI 助教详细咨询。"}
            )

# ==============================
# 页面2：授法
# ==============================
def page_teaching():
    st.title("授法 · 观看大师示范")

    st.markdown("""
    <div class="observe-bar">
        <strong>观察要点</strong> —— 
        握槌：掐而不紧、松而不滑 | 发力：手腕为轴，手臂固定 | 棒身：全程与地面平行
    </div>
    """, unsafe_allow_html=True)

    st.subheader("视频示范")
    try:
        st.video(TEACH_VIDEO_URL)
    except Exception:
        st.info("视频加载中，请稍后再试。")

    st.markdown("### 动作口诀")
    st.success("握槌虚活不僵硬，手肘收紧槌水平；\n发力只在手腕处，旋转还原姿态正。")
    st.markdown("> 传承人陈来发：手腕是轴，手臂是架，只转手不甩臂，内旋才标准。")

    if st.button("看完了，进入拆解学习", use_container_width=True):
        go_to("拆解")

# ==============================
# 页面3：拆解
# ==============================
def page_decomposition():
    st.title("拆解 · 四步分解学习")

    cols = st.columns(4)
    steps = [
        {"title": "第1步 预备握槌", "img": STEP_IMAGES[0], "desc": "双脚与肩同宽，膝盖微屈，双手握槌中部"},
        {"title": "第2步 内旋启动", "img": STEP_IMAGES[1], "desc": "手腕为轴发力，手臂固定，带动棒身旋转"},
        {"title": "第3步 水平控槌", "img": STEP_IMAGES[2], "desc": "棒身转至水平，双手微抬，两端对齐"},
        {"title": "第4步 还原定型", "img": STEP_IMAGES[3], "desc": "手腕平稳复位，棒身回到胸前"},
    ]
    for i, step in enumerate(steps):
        with cols[i]:
            st.subheader(step["title"])
            # 使用本地图片，带容错
            try:
                st.image(step["img"], width=150)
            except Exception:
                st.warning(f"图片缺失: {step['img']}")
            st.caption(step["desc"])

    st.markdown("""
    <blockquote>
        传承人陈来发说："手腕是轴，手臂是架，只转手不甩臂，内旋才标准。"
    </blockquote>
    """, unsafe_allow_html=True)

    if st.button("学会了，进入陪练对比", use_container_width=True):
        go_to("陪练")

# ==============================
# 页面4：陪练（动作自检模式）
# ==============================
def page_practice():
    st.title("陪练 · 动作自检")

    st.info("请做出 **第3步「水平控槌」** 动作，让同伴帮你拍一张正面照，然后上传对照标准图进行自查。")

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("标准动作")
        try:
            st.image(STANDARD_IMG, width=300)
        except Exception:
            st.warning("标准图缺失，请先放置 assets/standard.png")
        st.caption("观察：握槌位置、棒身水平、手肘内收")
    with col_right:
        st.subheader("你的动作")
        uploaded = st.file_uploader("上传照片", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        if uploaded:
            st.image(uploaded, width=300)
            st.success("已上传，请对照左侧标准图和下方要点逐项自查")
        else:
            st.info("点击此处上传你的练习照片")

    st.divider()

    st.subheader("自查要点")
    st.markdown("""
    请对着你的照片，确认以下三点：
    - **握槌位置**：双手是否握住槌身中部？虎口是否卡牢？
    - **棒身水平**：棒身是否与地面平行？两端是否对齐？
    - **手肘内收**：双肘是否向内收紧？有无外撇？
    """)

    # 自检清单（四项，包含发力感判断）
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

    if st.button("提交自检结果，完成学习", use_container_width=True):
        if all_checked:
            go_to("验成")
        else:
            st.warning("请逐项确认后再提交，至少需要检查完所有项目。")

# ==============================
# 页面5：验成
# ==============================
def page_achievement():
    st.title("恭喜完成学习")

    # 显示解锁信息
    if "self_check" in st.session_state and all(st.session_state.self_check.values()):
        st.success("恭喜解锁内旋槌技能！")
        st.balloons()
    else:
        st.info("你已走完教学流程，但自检清单未全部完成。")

    st.subheader("学习路径回顾")
    for step in ["诊学", "授法", "拆解", "陪练", "验成"]:
        st.markdown(f"- {step}")

    if st.button("重新开始学习", use_container_width=True):
        st.query_params.clear()
        # 清理状态
        for key in ["self_check", "dify_messages", "dify_answered"]:
            if key in st.session_state:
                del st.session_state[key]
        go_to("诊学")
        st.rerun()

# ==============================
# 侧边栏：学习进度 + Dify 对话
# ==============================
def show_sidebar():
    steps = ["诊学", "授法", "拆解", "陪练", "验成"]
    current = st.query_params.get("step", "诊学")
    current_idx = steps.index(current) if current in steps else 0

    with st.sidebar:
        st.title("学习进度")
        for i, name in enumerate(steps):
            if i == current_idx:
                st.button(name, key=f"nav_{name}", type="primary", use_container_width=True)
            elif i < current_idx:
                if st.button(name, key=f"nav_{name}", use_container_width=True):
                    go_to(name)
                    st.rerun()
            else:
                st.button(name, key=f"nav_{name}", disabled=True, use_container_width=True)

        st.markdown("---")
        st.subheader("AI 助教 · 随时问答")
        st.components.v1.iframe(DIFY_AI_URL, height=500, scrolling=True)

# ==============================
# 底部状态栏
# ==============================
def show_status_bar():
    current = st.query_params.get("step", "诊学")
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

# ==============================
# 主入口
# ==============================
def main():
    st.set_page_config(page_title="非遗数承 · 英歌舞内旋槌教学", layout="wide")
    set_custom_style()
    show_sidebar()

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

if __name__ == "__main__":
    main()