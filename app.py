import streamlit as st
import random
import time

st.set_page_config(
    page_title="ビンゴゲーム", 
    page_icon="🎯", 
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# カスタムCSS - マスを大幅に小さく
st.markdown("""
<style>
/* ====== 全体背景 ====== */
.stApp {
    background: linear-gradient(135deg, #89CFF0 0%, #4FC3F7 50%, #0288D1 100%);
}

/* ====== メインエリア ====== */
.main .block-container {
    padding: 1rem;
    max-width: 500px;
    margin: 0 auto;
}

/* ====== タイトル ====== */
h1 {
    color: white;
    text-align: center;
    font-size: 1.6rem !important;
    margin: 0.5rem 0 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

/* ====== ビンゴカード行 ====== */
div[data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-wrap: nowrap !important;
    justify-content: center;
    gap: 4px;
}

/* ====== ビンゴカードの列 ====== */
div[data-testid="column"] {
    flex: 0 0 calc(20% - 4px);
    padding: 2px !important;
}

/* ====== 🎯 ビンゴカードのマス（正方形） ====== */
.bingo-card .stButton button {
    width: 100%;
    aspect-ratio: 1 / 1; /* 正方形維持 */
    font-size: 0.6rem;
    border-radius: 6px;
    border: 2px solid #B0E0E6;
    background: white;
    color: #333;
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: all 0.2s ease;
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.1;
    display: flex;
    align-items: center;
    justify-content: center;
}

.bingo-card .stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.bingo-card .stButton button[kind="primary"] {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
    border: 2px solid #FF6B6B;
    color: #333;
}

.bingo-card .stButton button[kind="secondary"] {
    background: white;
    color: #333;
    border: 2px solid #B0E0E6;
}

/* ====== 🔘 コントロールボタン（新規・リセットなど） ====== */
.control-buttons .stButton button {
    width: 100%;
    height: 45px;
    border-radius: 10px;
    background: white;
    color: #0288D1;
    border: 2px solid #4FC3F7;
    font-size: 0.9rem;
    font-weight: bold;
    transition: all 0.2s ease;
}

.control-buttons .stButton button:hover {
    background: linear-gradient(135deg, #4FC3F7 0%, #0288D1 100%);
    color: white;
    border: 2px solid #0288D1;
}

/* ====== ビンゴ数表示 ====== */
.bingo-count-display {
    text-align: center;
    color: white;
    font-size: 1rem;
    font-weight: bold;
    background: rgba(255, 215, 0, 0.3);
    padding: 8px;
    border-radius: 8px;
    border: 2px solid rgba(255, 255, 255, 0.5);
    margin: 12px auto;
}

/* ====== 区切り線 ====== */
hr {
    margin: 0.8rem 0;
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
}

/* ====== 成功メッセージ ====== */
.stSuccess {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
    color: white;
    padding: 10px;
    border-radius: 10px;
    font-size: 0.9rem;
    font-weight: bold;
    text-align: center;
    border: 2px solid #FF6B6B;
    box-shadow: 0 6px 12px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)


# ===== ここに項目リストを追加してください =====
ITEM_LIST = [
    "朝食を食べた",
    "運動した",
    "本を読んだ",
    "早起きした",
    "水を2L飲んだ",
    "ストレッチした",
    "瞑想した",
    "日記を書いた",
    "友達と話した",
    "新しいことを学んだ",
    "掃除をした",
    "料理をした",
    "散歩した",
    "音楽を聴いた",
    "映画を見た",
    "買い物した",
    "洗濯した",
    "勉強した",
    "仕事した",
    "ゲームした",
    "写真を撮った",
    "ブログを書いた",
    "メールを返信した",
    "会議に参加した",
    "プレゼンした",
]
# ==========================================

# セッションステートの初期化
if 'bingo_card' not in st.session_state:
    st.session_state.bingo_card = None
if 'marked_cells' not in st.session_state:
    st.session_state.marked_cells = {}
if 'selected_cell' not in st.session_state:
    st.session_state.selected_cell = None
if 'flip_cell' not in st.session_state:
    st.session_state.flip_cell = None
if 'last_bingo_count' not in st.session_state:
    st.session_state.last_bingo_count = 0

def generate_bingo_card(items):
    """カスタム項目でビンゴカードを生成"""
    if len(items) < 24:
        return None
    
    selected = random.sample(items, 24)
    
    card = []
    index = 0
    for row in range(5):
        row_items = []
        for col in range(5):
            if row == 2 and col == 2:
                row_items.append('FREE')
            else:
                row_items.append(selected[index])
                index += 1
        card.append(row_items)
    
    st.session_state.marked_cells[(2, 2)] = "FREE"
    
    return card

def check_bingo(marked):
    """ビンゴ判定"""
    bingo_count = 0
    
    for row in range(5):
        if all((row, col) in marked for col in range(5)):
            bingo_count += 1
    
    for col in range(5):
        if all((row, col) in marked for row in range(5)):
            bingo_count += 1
    
    if all((i, i) in marked for i in range(5)):
        bingo_count += 1
    
    if all((i, 4-i) in marked for i in range(5)):
        bingo_count += 1
    
    return bingo_count

def show_snow_effect(bingo_count):
    """ビンゴ数に応じた雪のエフェクトを表示"""
    if bingo_count == 1:
        st.snow()
    elif bingo_count == 2:
        st.snow()
        time.sleep(0.3)
        st.snow()
    elif bingo_count >= 3:
        for i in range(min(bingo_count, 5)):
            st.snow()
            if i < min(bingo_count, 5) - 1:
                time.sleep(0.3)

# 初回アクセス時に自動でカード生成
if st.session_state.bingo_card is None and len(ITEM_LIST) >= 24:
    st.session_state.bingo_card = generate_bingo_card(ITEM_LIST)
    st.session_state.marked_cells = {(2, 2): "FREE"}

# タイトル
st.title("🎯 ビンゴカード")

# コントロールエリア
st.markdown('<div class="control-buttons">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🆕 新規", use_container_width=True):
        st.session_state.bingo_card = generate_bingo_card(ITEM_LIST)
        st.session_state.marked_cells = {(2, 2): "FREE"}
        st.session_state.selected_cell = None
        st.session_state.flip_cell = None
        st.session_state.last_bingo_count = 0
        st.rerun()

with col2:
    if st.button("🔄 リセット", use_container_width=True):
        st.session_state.marked_cells = {(2, 2): "FREE"}
        st.session_state.selected_cell = None
        st.session_state.flip_cell = None
        st.session_state.last_bingo_count = 0
        st.rerun()

with col3:
    if st.session_state.bingo_card:
        bingo_count = check_bingo(st.session_state.marked_cells)
        st.markdown(f"<div class='bingo-count-display'>🏆 {bingo_count}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ダイアログ表示
@st.dialog("✨ 名前を入力")
def name_input_dialog(row, col):
    item_name = st.session_state.bingo_card[row][col]
    st.markdown(f"### 📝 {item_name}")
    
    current_name = st.session_state.marked_cells.get((row, col), "")
    
    name = st.text_input("👤 お名前", value=current_name, key=f"name_input_{row}_{col}", placeholder="例: 山田太郎")
    
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ 登録", use_container_width=True, key=f"register_{row}_{col}", type="primary"):
            if name.strip():
                st.session_state.marked_cells[(row, col)] = name.strip()
                st.session_state.selected_cell = None
                st.session_state.flip_cell = (row, col)
                st.rerun()
            else:
                st.warning("名前を入力してください")
    
    with col2:
        if st.button("🗑️ 削除", use_container_width=True, key=f"delete_{row}_{col}"):
            if (row, col) in st.session_state.marked_cells:
                del st.session_state.marked_cells[(row, col)]
            st.session_state.selected_cell = None
            st.session_state.flip_cell = (row, col)
            st.rerun()
    
    with col3:
        if st.button("❌ 閉じる", use_container_width=True, key=f"cancel_{row}_{col}"):
            st.session_state.selected_cell = None
            st.rerun()

if st.session_state.selected_cell:
    row, col = st.session_state.selected_cell
    name_input_dialog(row, col)

# ビンゴカード表示
if st.session_state.bingo_card is None:
    st.error("❌ 項目が不足しています（最低24個必要）")
else:
    # ビンゴ判定
    bingo_count = check_bingo(st.session_state.marked_cells)
    
    # ビンゴ数が増えた場合のみ雪エフェクト表示
    if bingo_count > st.session_state.last_bingo_count:
        show_snow_effect(bingo_count)
        st.session_state.last_bingo_count = bingo_count
    
    # ビンゴメッセージ
    if bingo_count == 1:
        st.success(f"❄️ 素晴らしい！{bingo_count}ライン達成！")
    elif bingo_count == 2:
        st.success(f"❄️❄️ すごい！{bingo_count}ライン達成！ ❄️❄️")
    elif bingo_count >= 3:
        st.success(f"❄️❄️❄️ 完璧です！{bingo_count}ライン達成！ ❄️❄️❄️")
    
    # ビンゴカード表示（5x5グリッド）
    st.markdown('<div class="bingo-card">', unsafe_allow_html=True)
    
    for row in range(5):
        cols = st.columns(5)
        for col in range(5):
            value = st.session_state.bingo_card[row][col]
            is_marked = (row, col) in st.session_state.marked_cells
            
            with cols[col]:
                if value == 'FREE':
                    st.button(
                        "⭐FREE",
                        key=f"cell_{row}_{col}",
                        disabled=True,
                        use_container_width=True,
                        type="primary"
                    )
                elif is_marked:
                    name = st.session_state.marked_cells[(row, col)]
                    button_text = f"{value}\n✅{name}"
                    if st.button(
                        button_text,
                        key=f"cell_{row}_{col}",
                        use_container_width=True,
                        type="primary"
                    ):
                        st.session_state.selected_cell = (row, col)
                        st.rerun()
                else:
                    if st.button(
                        value,
                        key=f"cell_{row}_{col}",
                        use_container_width=True,
                        type="secondary"
                    ):
                        st.session_state.selected_cell = (row, col)
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # 統計情報
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 項目", len(ITEM_LIST))
    with col2:
        st.metric("✅ マーク", f"{len(st.session_state.marked_cells)}/25")
    with col3:
        st.metric("🎯 ビンゴ", bingo_count)
