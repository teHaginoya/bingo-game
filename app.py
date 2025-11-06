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

# カスタムCSS - PC専用
st.markdown("""
    <style>
    /* 背景 */
    .stApp {
        background: linear-gradient(135deg, #89CFF0 0%, #4FC3F7 50%, #0288D1 100%);
    }
    
    /* メインコンテンツエリア */
    .main .block-container {
        padding: 30px;
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* タイトル */
    h1 {
        color: white;
        text-align: center;
        font-size: 2.5rem !important;
        margin: 20px 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* ============================================ */
    /* コントロールエリア */
    /* ============================================ */
    
    .control-area {
        margin-bottom: 30px;
    }
    
    /* コントロールエリアの列 */
    .control-area div[data-testid="column"] {
        padding: 8px !important;
    }
    
    /* コントロールボタン */
    .control-area .stButton button {
        width: 100% !important;
        height: 60px !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        background: white !important;
        color: #0288D1 !important;
        border: 3px solid #4FC3F7 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 3px 6px rgba(0,0,0,0.15) !important;
        cursor: pointer !important;
    }
    
    .control-area .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.25) !important;
        background: #f0f9ff !important;
    }
    
    /* ビンゴ数表示 */
    .bingo-count-display {
        text-align: center;
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: rgba(255, 215, 0, 0.4);
        padding: 15px 10px;
        border-radius: 12px;
        border: 3px solid rgba(255, 255, 255, 0.6);
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 8px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.15);
    }
    
    /* ============================================ */
    /* ビンゴカードエリア */
    /* ============================================ */
    
    .bingo-card-area {
        display: flex;
        flex-direction: column;
        gap: 0;
        max-width: 650px;
        margin: 0 auto;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* ビンゴカードの行 */
    .bingo-card-area div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        gap: 0 !important;
        margin: 0 !important;
    }
    
    /* ビンゴカードの列 - 正方形を作るための設定 */
    .bingo-card-area div[data-testid="column"] {
        padding: 5px !important;
        flex: 1 !important;
        min-width: 0 !important;
    }
    
    /* ビンゴカードのボタン - 正方形 */
    .bingo-card-area .stButton {
        width: 100%;
    }
    
    .bingo-card-area .stButton button {
        width: 110px !important;
        height: 110px !important;
        font-size: 0.85rem !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.3 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 3px 6px rgba(0,0,0,0.15) !important;
        padding: 8px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
    }
    
    .bingo-card-area .stButton button:hover {
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 6px 12px rgba(0,0,0,0.25) !important;
    }
    
    /* マーク済みボタン */
    .bingo-card-area .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%) !important;
        color: #333 !important;
        border: 3px solid #FF6B6B !important;
    }
    
    /* 未マークボタン */
    .bingo-card-area .stButton button[kind="secondary"] {
        background: white !important;
        color: #333 !important;
        border: 3px solid #B0E0E6 !important;
    }
    
    /* ============================================ */
    /* その他の要素 */
    /* ============================================ */
    
    /* 区切り線 */
    hr {
        margin: 25px 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
    }
    
    /* 成功メッセージ */
    .stSuccess {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
        padding: 18px;
        border-radius: 15px;
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        border: 3px solid #FF6B6B;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        margin: 15px 0;
    }
    
    /* エラーメッセージ */
    .stError {
        background: rgba(244, 67, 54, 0.9);
        color: white;
        padding: 18px;
        border-radius: 15px;
        font-size: 1.1rem;
    }
    
    /* メトリクス */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: white;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: white !important;
        font-size: 1rem;
    }
    
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.25);
        padding: 15px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* ダイアログ */
    [data-testid="stModal"] {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        border: 3px solid #4FC3F7;
    }
    
    /* テキスト入力 */
    .stTextInput input {
        border-radius: 10px;
        border: 2px solid #4FC3F7;
        padding: 12px;
        font-size: 16px;
    }
    
    .stTextInput input:focus {
        border-color: #0288D1;
        box-shadow: 0 0 0 3px rgba(79, 195, 247, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# ===== 項目リスト =====
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

# セッションステートの初期化
if 'bingo_card' not in st.session_state:
    st.session_state.bingo_card = None
if 'marked_cells' not in st.session_state:
    st.session_state.marked_cells = {}
if 'selected_cell' not in st.session_state:
    st.session_state.selected_cell = None
if 'last_bingo_count' not in st.session_state:
    st.session_state.last_bingo_count = 0

def generate_bingo_card(items):
    """ビンゴカードを生成"""
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
    
    # 横列チェック
    for row in range(5):
        if all((row, col) in marked for col in range(5)):
            bingo_count += 1
    
    # 縦列チェック
    for col in range(5):
        if all((row, col) in marked for row in range(5)):
            bingo_count += 1
    
    # 斜め（左上→右下）
    if all((i, i) in marked for i in range(5)):
        bingo_count += 1
    
    # 斜め（右上→左下）
    if all((i, 4-i) in marked for i in range(5)):
        bingo_count += 1
    
    return bingo_count

def show_snow_effect(bingo_count):
    """ビンゴ数に応じた雪のエフェクト"""
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
st.markdown('<div class="control-area">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🆕 新規カード", use_container_width=True, key="btn_new"):
        st.session_state.bingo_card = generate_bingo_card(ITEM_LIST)
        st.session_state.marked_cells = {(2, 2): "FREE"}
        st.session_state.selected_cell = None
        st.session_state.last_bingo_count = 0
        st.rerun()

with col2:
    if st.button("🔄 リセット", use_container_width=True, key="btn_reset"):
        st.session_state.marked_cells = {(2, 2): "FREE"}
        st.session_state.selected_cell = None
        st.session_state.last_bingo_count = 0
        st.rerun()

with col3:
    if st.session_state.bingo_card:
        bingo_count = check_bingo(st.session_state.marked_cells)
        st.markdown(f"<div class='bingo-count-display'>🏆 ビンゴ数: {bingo_count}</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ダイアログ
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
                st.rerun()
            else:
                st.warning("名前を入力してください")
    
    with col2:
        if st.button("🗑️ 削除", use_container_width=True, key=f"delete_{row}_{col}"):
            if (row, col) in st.session_state.marked_cells:
                del st.session_state.marked_cells[(row, col)]
            st.session_state.selected_cell = None
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
    
    # ビンゴ数が増えた場合のみ雪エフェクト
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
    st.markdown('<div class="bingo-card-area">', unsafe_allow_html=True)
    
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
        st.metric("📊 総項目数", len(ITEM_LIST))
    with col2:
        st.metric("✅ マーク済", f"{len(st.session_state.marked_cells)}/25")
    with col3:
        st.metric("🎯 ビンゴ数", bingo_count)
