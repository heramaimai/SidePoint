import streamlit as st
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
ASSETS_DIR = APP_DIR / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"

AUDIO_SOURCES = {
    "夏天的暴雨": AUDIO_DIR / "雷雨白噪音.wav",
    "夜晚的海边": AUDIO_DIR / "海浪声.wav",
    "清晨的鸟鸣": AUDIO_DIR / "鸟鸣.wav",
}


def load_audio_bytes(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except Exception:
        return None


SUPPLEMENT_MARKER = "__supplement__"
SUPPLEMENT_PHRASES = [
    "我想用我自己的词汇描绘它...",
    "在上述选项之外，我想这样描述它...",
    "除了这些，我还想告诉你..",
]


def get_supplement_phrase(qid: str) -> str:
    """
    为每一题挑一句浪漫的“补充入口”文案，并在同一次故事中保持稳定。
    """
    if "supplement_phrases" not in st.session_state:
        st.session_state.supplement_phrases = {}
    phrases: dict[str, str] = st.session_state.supplement_phrases
    if qid not in phrases:
        # 在三句里为每题分配一个稳定入口
        idx = (sum(ord(c) for c in qid) + 7) % len(SUPPLEMENT_PHRASES)
        phrases[qid] = SUPPLEMENT_PHRASES[idx]
    return phrases[qid]


def apply_theme() -> None:
    st.set_page_config(page_title="支点", page_icon="✨", layout="centered")
    st.markdown(
        """
        <style>
          :root {
            --bg: #141018;
            --text: #F6B4C7;
            --muted: rgba(246, 180, 199, 0.86);
            --card: rgba(255,255,255,0.04);
            --border: rgba(246, 180, 199, 0.18);
          }

          html, body, [data-testid="stAppViewContainer"] {
            background: var(--bg);
            color: var(--text) !important;
          }
          /* iPhone / Mobile-first 优化 */
          html { -webkit-text-size-adjust: 100%; }
          * { -webkit-tap-highlight-color: rgba(0,0,0,0); }
          /* iOS: 避免输入框聚焦时自动放大页面 */
          input, textarea, select { font-size: 16px !important; }
          /* Streamlit containers sometimes override text color via theme.
             注意：不要用 * 选择器，避免影响 audio 控件可见性。 */
          [data-testid="stMarkdownContainer"],
          [data-testid="stText"],
          [data-testid="stCaptionContainer"],
          [data-testid="stSidebar"],
          p, span, div, label, li, blockquote {
            color: var(--text) !important;
          }
          a { color: rgba(246, 180, 199, 0.92) !important; }

          /* 去掉顶部那条“空白椭圆长条/装饰” */
          [data-testid="stHeader"] { display: none; height: 0px; }
          [data-testid="stToolbar"] { visibility: hidden; height: 0px; }
          [data-testid="stDecoration"] { display: none; height: 0px; }
          /* 某些版本还会渲染额外的顶部容器 */
          [data-testid="stAppHeader"] { display: none; height: 0px; }
          [data-testid="stAppToolbar"] { display: none; height: 0px; }
          [data-testid="stAppViewBlockContainer"] { padding-top: 1.25rem; }
          /* iPhone 安全区：底部留出空间 */
          [data-testid="stAppViewBlockContainer"] { padding-bottom: calc(1.25rem + env(safe-area-inset-bottom)); }

          * { letter-spacing: 0.02em; }

          .sp-wrap { max-width: 720px; margin: 0 auto; }
          .sp-title {
            font-size: 2.05rem;
            font-weight: 650;
            line-height: 1.25;
            margin: 0.4rem 0 0.2rem 0;
          }
          .sp-sub {
            font-size: 1.02rem;
            opacity: 0.92;
            line-height: 1.9;
          }
          .sp-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 18px 18px 8px 18px;
            margin: 12px 0 18px 0;
            box-shadow: 0 18px 46px rgba(0,0,0,0.22);
          }
          .sp-divider {
            height: 1px;
            background: rgba(246, 180, 199, 0.14);
            margin: 14px 0 6px 0;
          }

          /* Buttons */
          div.stButton > button {
            border-radius: 999px !important;
            padding: 0.75rem 1.05rem !important;
            border: 1px solid rgba(246, 180, 199, 0.34) !important;
            background: rgba(246, 180, 199, 0.10) !important;
            color: var(--text) !important;
            transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
          }
          div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 34px rgba(0,0,0,0.30);
            background: rgba(246, 180, 199, 0.14) !important;
          }

          /* Radios */
          div[role="radiogroup"] label {
            padding: 10px 12px;
            border-radius: 14px;
            border: 1px solid rgba(246, 180, 199, 0.18);
            background: rgba(255,255,255,0.03);
            margin: 6px 0;
          }

          /* Inputs */
          input, textarea {
            border-radius: 14px !important;
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(246, 180, 199, 0.22) !important;
            color: var(--text) !important;
          }

          /* 小屏适配：更大点击区、更松留白、两列自动变一列 */
          @media (max-width: 640px) {
            .sp-wrap { max-width: 100%; padding: 0 4px; }
            .sp-title { font-size: 1.85rem; margin-top: 0.1rem; }
            .sp-sub { font-size: 1.00rem; }
            .sp-card { border-radius: 20px; padding: 18px 16px 10px 16px; }

            div.stButton > button {
              padding: 0.92rem 1.05rem !important;
              font-size: 1.02rem !important;
            }
            div[role="radiogroup"] label { padding: 12px 12px; }

            /* Streamlit columns: 在手机上堆叠 */
            div[data-testid="stHorizontalBlock"] {
              flex-direction: column !important;
              gap: 0.65rem !important;
            }
            div[data-testid="stColumn"] {
              width: 100% !important;
              flex: 1 1 100% !important;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    if "step" not in st.session_state:
        st.session_state.step = "home"
    if "answers" not in st.session_state:
        st.session_state.answers = {}


def set_step(step: str) -> None:
    st.session_state.step = step
    st.rerun()


def md_quote(text: str) -> None:
    st.markdown(f'> *{text}*')

def reset_story() -> None:
    st.session_state.answers = {}
    set_step("home")


def advance_if_complete(qid: str, next_step: str, *, second_triggers_input: bool = False, option2: str = "") -> None:
    a = st.session_state.answers
    choice = a.get(f"{qid}__choice", "")
    extra = (a.get(f"{qid}__extra", "") or "").strip()

    if not choice:
        return
    if choice == SUPPLEMENT_MARKER:
        if extra == "":
            return
        set_step(next_step)
        return
    if second_triggers_input and choice == option2:
        if extra == "":
            return
        set_step(next_step)
        return

    set_step(next_step)


def advance_if_text(qid: str, next_step: str) -> None:
    val = (st.session_state.answers.get(f"{qid}__text", "") or "").strip()
    if val == "":
        return
    set_step(next_step)


def question_with_supplement(
    qid: str,
    title: str,
    option1: str,
    option2: str,
    *,
    help_text: str | None = None,
    second_triggers_input: bool = False,
    placeholder: str = "我想补充…",
    next_step: str | None = None,
    allow_supplement: bool = True,
) -> None:
    """
    除纯输入题外：固定选项1、固定选项2、以及“我想补充...”选项（选中后出现输入框）。
    某些题（如 Q5 / Q10 的固定选项2）也需要输入时，用 second_triggers_input=True。
    """
    st.write(f"**{qid}**  {title}")
    if help_text:
        md_quote(help_text)

    key_choice = f"{qid}__choice"
    key_extra = f"{qid}__extra"

    prev_choice = st.session_state.answers.get(key_choice, "")
    prev_extra = st.session_state.answers.get(key_extra, "")

    # 顶部：两个固定选项并列放置
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button(option1, use_container_width=True, key=f"{qid}__btn1"):
            st.session_state.answers[key_choice] = option1
            st.session_state.answers[key_extra] = ""
            if next_step:
                set_step(next_step)
    with col2:
        if st.button(option2, use_container_width=True, key=f"{qid}__btn2"):
            st.session_state.answers[key_choice] = option2
            # Q5/Q10 这类：固定选项2本身需要继续输入，因此不立刻跳转
            if not second_triggers_input and next_step:
                st.session_state.answers[key_extra] = ""
                set_step(next_step)

    # 当前选择展示（让用户知道自己选中了什么）
    choice = st.session_state.answers.get(key_choice, prev_choice)
    if choice:
        shown = get_supplement_phrase(qid) if choice == SUPPLEMENT_MARKER else choice
        st.markdown(f"<div style='opacity:0.86'>你刚刚选择了：{shown}</div>", unsafe_allow_html=True)

    st.write("")

    # 底部：开放输入区（浪漫补充入口 或 固定2需要输入）
    needs_input = (choice == SUPPLEMENT_MARKER) or (second_triggers_input and choice == option2)

    # “我想补充...”入口（可按题目关闭，例如 Q10）
    if allow_supplement:
        supplement_label = get_supplement_phrase(qid)
        if st.button(supplement_label, use_container_width=True, key=f"{qid}__choose_supplement"):
            st.session_state.answers[key_choice] = SUPPLEMENT_MARKER
            st.rerun()

        # 只有当用户选择了“补充”，才出现输入框
        if st.session_state.answers.get(key_choice) == SUPPLEMENT_MARKER:
            default_extra = st.session_state.answers.get(key_extra, "")
            extra = st.text_input(
                " ",
                value=default_extra,
                placeholder=placeholder,
                key=key_extra,
            )
            st.session_state.answers[key_extra] = extra
            if next_step:
                if st.button(
                    "继续下一题",
                    use_container_width=True,
                    key=f"{qid}__supp_next",
                    disabled=(extra.strip() == ""),
                ):
                    set_step(next_step)
    else:
        # 若之前状态里意外残留“补充模式”，为避免困在输入区，自动回落到 option1
        if st.session_state.answers.get(key_choice) == SUPPLEMENT_MARKER:
            st.session_state.answers[key_choice] = option1
            st.session_state.answers[key_extra] = ""

    # 固定选项2触发输入（Q5/Q10）
    if second_triggers_input and choice == option2:
        st.write("")
        default_extra = st.session_state.answers.get(key_extra, "")
        extra = st.text_input(
            " ",
            value=default_extra,
            placeholder=placeholder,
            key=key_extra,
        )
        st.session_state.answers[key_extra] = extra
        if next_step:
            if st.button("继续下一题", use_container_width=True, key=f"{qid}__opt2_next", disabled=(extra.strip() == "")):
                set_step(next_step)

    # 兼容：如果旧状态里 choice 是“补充模式”，但用户切换回固定选项，应清掉 extra
    if choice in (option1, option2) and (choice != prev_choice or prev_extra != st.session_state.answers.get(key_extra, "")):
        if not (second_triggers_input and choice == option2):
            st.session_state.answers[key_extra] = ""

    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)


def question_pure_input(
    qid: str,
    title: str,
    *,
    help_text: str | None = None,
    placeholder: str = "",
    next_step: str | None = None,
) -> None:
    st.write(f"**{qid}**  {title}")
    if help_text:
        md_quote(help_text)
    key = f"{qid}__text"
    default_val = st.session_state.answers.get(key, "")
    val = st.text_input(
        " ",
        value=default_val,
        placeholder=placeholder,
        key=key,
        on_change=(lambda: advance_if_text(qid, next_step)) if next_step else None,
    )
    st.session_state.answers[key] = val
    st.markdown('<div class="sp-divider"></div>', unsafe_allow_html=True)


def get_final_text(qid: str) -> str:
    """
    返回该题最终展示文本：
    - 若选“补充模式”则优先补充文本（为空则回退到提示语）
    - 若固定2需要输入且为空，则仍展示“我看到了…”这类选择
    """
    choice = st.session_state.answers.get(f"{qid}__choice", "")
    extra = (st.session_state.answers.get(f"{qid}__extra", "") or "").strip()
    if choice == SUPPLEMENT_MARKER:
        return extra if extra else get_supplement_phrase(qid)
    if extra and choice:
        # 适配“固定2也触发输入”的题：用“选项 + 输入”
        if choice in ("我看到了…", "其实关于它的影响，我还想补充..."):
            return f"{choice}{extra}"
    return choice


def build_narrative() -> str:
    a = st.session_state.answers

    # 外化名称：优先 Q7（正式名字），否则 Q6（称呼）
    q6 = (a.get("Q6__text", "") or "").strip()
    q7_choice = a.get("Q7__choice", "").strip()
    external_name = q7_choice or q6 or "那个困扰"

    # 影响与感受
    vol = get_final_text("Q1")
    shape = get_final_text("Q2")
    gender = get_final_text("Q3")
    mirror = get_final_text("Q4")
    scene = get_final_text("Q5")
    wave = get_final_text("Q8")
    self_view = get_final_text("Q9")
    impact_more = get_final_text("Q10")

    # 例外瞬间与微光
    ex1 = get_final_text("Q11")
    ex2 = get_final_text("Q12")
    value = (a.get("Q13__text", "") or "").strip()
    witness = (a.get("Q14__text", "") or "").strip()
    comfort = (a.get("Q15__text", "") or "").strip()
    branch = get_final_text("Q16")

    # 温柔兜底（避免空白破坏叙事）
    value = value or "你珍视的某种重要之物"
    witness = witness or "某种你一直拥有却常常忘记的品质"
    comfort = comfort or "那些仍愿意向前的部分"

    # 控制长度：尽量约 300 字左右（不做死限制，保持自然）
    narrative = (
        f"你把 {external_name} 轻轻请到对面：它 {vol}，线条是 {shape}，"
        f"声音里带着 {gender} 的气息。你望向它，像望进一面镜子——{mirror}。"
        f"它也许曾带来一幅画面：{scene}。在它的陪伴或对抗里，你心底涌动着 {wave}，"
        f"你看见的自己是 {self_view}。而你仍愿意补充它的影响：{impact_more}。"
        f"可在那些幽暗的日子里，你也曾有过微小的偏离：{ex1}。那一刻，你的身体记得 {ex2}。"
        f"当你做出那个“不一样”的动作，你其实在守护 {value}；在爱你、懂你的人眼中，"
        f"你呈现出 {witness}。于是你也开始为自己感到欣慰：{comfort}。"
        f"如果主线仍在延伸，那么这段支线就叫做「{branch}」——它不喧哗，却会在你需要时，"
        f"成为你继续讲述自己的支点。"
    )
    return narrative


def render_home() -> None:
    st.markdown('<div class="sp-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="sp-title">支点 SidePoint</div>', unsafe_allow_html=True)

    if "home_reveal" not in st.session_state:
        st.session_state.home_reveal = 0

    # 通过点击，一步步呈现寓意与入口
    if st.session_state.home_reveal >= 1:
        st.markdown('<div class="sp-card">', unsafe_allow_html=True)
        md_quote("在生命那场宏大的叙事里，每个人都需要一个支点。")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.home_reveal >= 2:
        st.markdown('<div class="sp-card">', unsafe_allow_html=True)
        md_quote("哪怕只是微小的光斑，当点与点连成了线，就能在孤独的主线之外，织就出丰厚而自由的支线故事。")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.home_reveal >= 3:
        st.markdown('<div class="sp-card">', unsafe_allow_html=True)
        md_quote("欢迎来到这里，让那些被遮蔽的，重新被看见。")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.home_reveal < 3:
        next_labels = {
            0: "轻轻点一下，让故事继续",
            1: "我准备好探索我的人生支线故事了",
            2: "我要书写我的人生",
        }
        if st.button(next_labels.get(st.session_state.home_reveal, "轻轻点一下，让故事继续"), use_container_width=True):
            st.session_state.home_reveal += 1
            st.rerun()
    else:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            if st.button("此刻，我有一些困扰想说给你听", use_container_width=True):
                set_step("q1")
        with c2:
            if st.button("我只想安静地坐一会儿，你陪陪我就好", use_container_width=True):
                set_step("quiet")

    st.markdown("</div>", unsafe_allow_html=True)


def render_quiet() -> None:
    st.markdown('<div class="sp-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="sp-title">我在</div>', unsafe_allow_html=True)
    st.markdown('<div class="sp-card">', unsafe_allow_html=True)
    md_quote("我们可以什么都不急着说。你只要呼吸就好。")
    md_quote("如果你愿意，我为你留三种声音。你可以选一种，像把自己交给一段温柔的背景。")
    st.write("")
    scene = st.radio(
        label="",
        options=["夏天的暴雨", "夜晚的海边", "清晨的鸟鸣"],
        horizontal=False,
        key="quiet_scene",
    )

    cache_key = f"quiet_audio__{scene}"
    if cache_key not in st.session_state:
        path = AUDIO_SOURCES.get(scene)
        audio_bytes = load_audio_bytes(path) if path else None
        st.session_state[cache_key] = audio_bytes

    audio_bytes = st.session_state.get(cache_key)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav", loop=True)
        md_quote("选好以后，轻轻按下播放器里的播放键就好。")
    else:
        md_quote("我还没能把声音取回来。请检查音频文件是否仍在桌面，并且文件名没有变化。")
        st.write(f"我正在寻找：`{AUDIO_SOURCES.get(scene)}`")

    st.write("")
    md_quote("接下来是一个身体扫描的正念练习。你不需要做得“正确”，只需要在。")

    if "quiet_started" not in st.session_state:
        st.session_state.quiet_started = False
    if not st.session_state.quiet_started:
        if st.button("开始身体扫描练习", use_container_width=True):
            st.session_state.quiet_started = True
            st.rerun()
    else:
        md_quote("先把注意力交还给呼吸。吸气时，像把一束柔软的光带进胸腔；呼气时，把紧绷轻轻放下。")
        md_quote("感受你的脚：脚趾、脚背、脚踝。冷或热、麻或沉，都没关系。只要看见。")
        md_quote("把注意力带到小腿与膝盖。你不需要改变它们，你只是陪它们待一会儿。")
        md_quote("再到大腿与骨盆。让身体在椅子上、在地面上，有一个安全的落点。")
        md_quote("把注意力轻轻放到腹部。它或许起伏，或许紧缩。你可以对它说：我看见你了。")
        md_quote("来到胸口与心脏。你可以把手心贴上去。感受心跳像一盏小灯——它一直在。")
        md_quote("让肩膀放松一点点。想象它们像雪落一样慢慢下沉。")
        md_quote("注意手臂、手掌、指尖。让每一根手指都得到允许：允许颤动，允许安静。")
        md_quote("把注意力移到喉咙与下颌。你可以轻轻松开牙关，让舌头回到温柔的位置。")
        md_quote("来到眼睛与眉间。让眼皮像两片柔软的花瓣，慢慢合上或半合。")
        md_quote("最后，感受整个身体像一座小小的宇宙：此刻你在这里，被空气拥抱，被时间照看。")
        st.write("")
        if st.button("我准备好了，回到首页", use_container_width=True):
            st.session_state.quiet_started = False
            set_step("home")
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("回到首页", use_container_width=True):
        st.session_state.quiet_started = False
        set_step("home")
    st.markdown("</div>", unsafe_allow_html=True)

QUESTION_ORDER = [f"q{i}" for i in range(1, 17)]
NEXT_STEP = {f"q{i}": (f"q{i+1}" if i < 16 else "before_result") for i in range(1, 17)}
PREV_STEP = {f"q{i}": (f"q{i-1}" if i > 1 else "home") for i in range(1, 17)}


def render_question(step: str) -> None:
    idx = int(step[1:])
    qid = f"Q{idx}"
    next_step = NEXT_STEP[step]

    st.markdown('<div class="sp-wrap">', unsafe_allow_html=True)

    if idx <= 10:
        st.markdown('<div class="sp-title">这是我的人生故事</div>', unsafe_allow_html=True)
        md_quote("这一部分我们将问题从你的身体里“请”出来，像观察一个新朋友一样观察它。")
    else:
        st.markdown('<div class="sp-title">这也是我的人生</div>', unsafe_allow_html=True)
        md_quote("即便在最幽暗的时刻，你的生命也从未被完全占据。那些被你忽略的微光，才是你真正的支撑。")

    st.write("")
    st.markdown('<div class="sp-card">', unsafe_allow_html=True)

    if qid == "Q1":
        question_with_supplement(
            "Q1",
            "那个一直缠绕着你的困扰，如果此时它就坐在你对面，它占据了多大的空间？",
            "大概只如手掌般大，我可以轻轻托起",
            "像遥远宇宙里寂静的天体，无边无际",
            next_step=next_step,
        )
    elif qid == "Q2":
        question_with_supplement(
            "Q2",
            "当你闭上眼，它的轮廓在你的呼吸中呈现出什么样的线条？",
            "棱角分明，带着坚硬的方形",
            "柔和却也沉重的圆形",
            next_step=next_step,
        )
    elif qid == "Q3":
        question_with_supplement(
            "Q3",
            "它的声音里，是否藏着某种性别的色彩或性格？",
            "像某种刚强沉稳的男性气息",
            "像某种细腻潮湿的女性质感",
            next_step=next_step,
        )
    elif qid == "Q4":
        question_with_supplement(
            "Q4",
            "它是一面镜子吗？当你注视它时，里面出现的是？",
            "那些已经泛黄却未褪色的旧事",
            "那些说不清道不明的、确切的感受",
            next_step=next_step,
        )
    elif qid == "Q5":
        question_with_supplement(
            "Q5",
            "它的出现，是否让你想到脑海中的某个画面？",
            "那里是一片荒芜，没有任何画面",
            "我看到了…",
            second_triggers_input=True,
            placeholder="我看到了……",
            next_step=next_step,
        )
    elif qid == "Q6":
        question_pure_input(
            "Q6",
            "如果这个问题是个人的话，你会如何称呼她/他/它？",
            placeholder="你想怎么称呼它？",
            next_step=next_step,
        )
        st.write("")
        q6_val = (st.session_state.answers.get("Q6__text", "") or "").strip()
        if st.button("先这样，继续", use_container_width=True, disabled=(q6_val == "")):
            set_step(next_step)
    elif qid == "Q7":
        question_with_supplement(
            "Q7",
            "我们试着给它一个正式的名字吧。是想沿用刚才那个称呼，还是给它一个新名字？",
            "就用刚才那个充满灵性的称呼",
            "还是简单地称它为“这个问题”吧",
            next_step=next_step,
        )
    elif qid == "Q8":
        question_with_supplement(
            "Q8",
            "在它的陪伴或对抗下，你的心底涌动的是怎样的浪潮？",
            "是像火焰般燃烧的愤怒",
            "是像深海般静默的恐惧",
            next_step=next_step,
        )
    elif qid == "Q9":
        question_with_supplement(
            "Q9",
            "在这层感受的滤镜下，你眼中的自己是什么样子的？",
            "是一个即便疲惫却依然有力量的人",
            "是一个正处于失落缝隙中的失败者",
            next_step=next_step,
        )
    elif qid == "Q10":
        question_with_supplement(
            "Q10",
            "谢谢你带我走进了这个故事。你觉得我已经足够了解它对你的影响了吗？",
            "已经足够了，谢谢你",
            "其实关于它的影响，我还想补充...",
            second_triggers_input=True,
            placeholder="你还想补充的是……",
            next_step=next_step,
            allow_supplement=False,
        )
    elif qid == "Q11":
        question_with_supplement(
            "Q11",
            "在“它”如此强大、试图掌控你生活的日子里，是否曾有过那么一个极小的瞬间，你并没有听从它的指挥，而是选择了寻找你的节奏？",
            "有过一个瞬间，我感受到了内心久违的宁静",
            "有过一次，我虽然害怕，但还是尝试去做了自己",
            next_step=next_step,
        )
    elif qid == "Q12":
        question_with_supplement(
            "Q12",
            "在那个瞬间，你的身体感受到了什么？",
            "像是一阵清风拂过，肩膀轻快了许多",
            "像是一粒种子破土，感受到了一丝韧性",
            next_step=next_step,
        )
    elif qid == "Q13":
        question_pure_input(
            "Q13",
            "当你做出那个“不一样”的动作时，你其实是在守护你生命中什么重要的东西？",
            placeholder="你在守护的是……",
            next_step=next_step,
        )
        st.write("")
        if st.button("先这样，继续", use_container_width=True):
            set_step(next_step)
    elif qid == "Q14":
        question_pure_input(
            "Q14",
            "如果你生命里那个对你非常重要的、非常爱你的、懂你的人（或者曾经的你自己）在那一刻注视着你，他/她会从你的行动中看到什么样的品质？",
            placeholder="他/她会看到你拥有……",
            next_step=next_step,
        )
        st.write("")
        if st.button("先这样，继续", use_container_width=True):
            set_step(next_step)
    elif qid == "Q15":
        question_pure_input(
            "Q15",
            "如果透过他/她的眼睛来看现在的你，你会为自己身上的哪些地方感到欣慰？",
            placeholder="你会为自己欣慰的是……",
            next_step=next_step,
        )
        st.write("")
        if st.button("先这样，继续", use_container_width=True):
            set_step(next_step)
    elif qid == "Q16":
        question_with_supplement(
            "Q16",
            "如果说之前的那个困扰是你人生的“主线故事”，那么这个不太一样的例外瞬间，你想给它起一个浪漫的名字？",
            "裂缝中的阳光",
            "未被定义的自由",
            next_step=next_step,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # 底部导航（不抢戏，但提供退路）
    c1, c2 = st.columns(2, gap="large")
    with c1:
        if st.button("回到首页", use_container_width=True):
            set_step("home")
    with c2:
        if st.button("返回上一题", use_container_width=True):
            set_step(PREV_STEP[step])

    st.markdown("</div>", unsafe_allow_html=True)


def render_before_result() -> None:
    st.markdown('<div class="sp-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="sp-title">把线轻轻系好</div>', unsafe_allow_html=True)
    md_quote("当点与点连成了线，你会看见：主线之外，你也一直在织就支线。")
    st.markdown('<div class="sp-card">', unsafe_allow_html=True)
    if st.button("这一次，我选择这样讲述我的生命故事", use_container_width=True):
        set_step("result")
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("返回上一题", use_container_width=True):
        set_step("q16")
    st.markdown("</div>", unsafe_allow_html=True)


def render_result() -> None:
    st.markdown('<div class="sp-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="sp-title">生命叙事书</div>', unsafe_allow_html=True)
    st.markdown('<div class="sp-card">', unsafe_allow_html=True)
    md_quote("谢谢你把这些交给我。下面这段文字，会把你说过的、选择过的微光，轻轻串起来。")
    st.write("")
    st.write(build_narrative())
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sp-card">', unsafe_allow_html=True)
    st.write("**你此刻留下的答案**")

    st.write("**显影（外化探索）**")
    for i in range(1, 11):
        qid = f"Q{i}"
        if qid in ("Q6",):
            st.write(f"- **{qid}**：{(st.session_state.answers.get('Q6__text','') or '').strip()}")
        else:
            st.write(f"- **{qid}**：{get_final_text(qid)}")

    st.write("")
    st.write("**寻光**")
    for qid in ("Q11", "Q12", "Q16"):
        st.write(f"- **{qid}**：{get_final_text(qid)}")
    for qid in ("Q13", "Q14", "Q15"):
        st.write(f"- **{qid}**：{(st.session_state.answers.get(f'{qid}__text','') or '').strip()}")

    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        if st.button("回到首页", use_container_width=True):
            set_step("home")
    with c2:
        if st.button("我想要再讲一个不同的故事", use_container_width=True):
            st.session_state.answers = {}
            set_step("q1")

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    apply_theme()
    init_state()

    step = st.session_state.step
    if step == "home":
        render_home()
        return
    if step == "quiet":
        render_quiet()
        return
    if step.startswith("q") and step[1:].isdigit():
        if step in {f"q{i}" for i in range(1, 17)}:
            render_question(step)
            return
    if step == "before_result":
        render_before_result()
        return
    if step == "result":
        render_result()
        return

    # fallback
    st.session_state.step = "home"
    st.rerun()


if __name__ == "__main__":
    main()
