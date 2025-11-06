import streamlit as st
import random
import time

st.set_page_config(
    page_title="ビンゴゲーム", 
    page_icon="🎯", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# カスタムCSS - スマホ対応のビンゴカード
st.markdown("""
    <style>
    /* 水色のグラデーション背景 */
    .stApp {
        background: linear-gradient(135deg, #89CFF0 0%, #4FC3F7 50%, #0288D1 100%);
    }
    
    /* メインコンテンツエリア */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 100%;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    
    /* タイトルスタイル */
    h1 {
        color: white;
        text-align: center;
        font-size: 2rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* 列を強制的に横並びに - 最重要！ */
    div[data-testid="column"] {
        width: 20% !important;
        flex: 1 1 20% !important;
        min-width: 0 !important;
        padding: 2px !important;
    }
    
    /* 行を横並びに固定 */
    div[data-testid="stHorizontalBlock"] {
        gap: 0px !important;
        flex-wrap: nowrap !important;
    }
    
    /* ボタンのスタイル */
    .stButton button {
        width: 100%;
        height: 70px;
        font-size: 11px;
        font-weight: bold;
        border-radius: 8px;
        white-space: normal;
        word-wrap: break-word;
        line-height: 1.2;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 4px;
    }
    
    /* スマホ用の調整 */
    @media (max-width: 768px) {
        .stButton button {
            height: 65px;
            font-size: 10px;
            border-radius: 6px;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        div[data-testid="column"] {
            padding: 1px !important;
        }
    }
    
    /* さらに小さい画面用 */
    @media (max-width: 480px) {
        .stButton button {
            height: 60px;
            font-size: 9px;
        }
    }
    
    /* ボタンホバー効果 */
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* プライマリボタン（マーク済み） */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #333;
        border: 2px solid #FF6B6B;
        font-weight: bold;
    }
    
    /* セカンダリボタン（未マーク） */
    .stButton button[kind="secondary"] {
        background: white;
        color: #333;
        border: 2px solid #B0E0E6;
    }
    
    /* コントロールボタンエリアの列 */
    .main > div:first-child div[data-testid="column"] {
        width: 33.333% !important;
        flex: 1 1 33.333% !important;
    }
    
    /* コントロールボタン */
    .main > div:first-child .stButton button {
        height: 45px;
        font-size: 14px;
        border-radius: 22px;
        background: white;
        color: #0288D1;
        border: 2px solid #4FC3F7;
    }
    
    /* メトリクスカード */
    [data-testid="stMetricValue"] {
        font-size: 24px;
        color: white;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: white !important;
        font-size: 14px;
    }
    
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.25);
        padding: 10px;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* 区切り線 */
    hr {
        margin: 1rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
    }
    
    /* 成功メッセージ */
    .stSuccess {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
        padding: 15px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        border: 3px solid #FF6B6B;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
    }
    
    /* ダイアログのスタイル */
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
        box-shadow: 0 0 0 2px rgba(79, 195, 247, 0.2);
    }
    
    /* エラーメッセージ */
    .stError {
        background: rgba(244, 67, 54, 0.9);
        color: white;
        padding: 15px;
        border-radius: 10px;
    }
    
    /* トップのビンゴ数表示 */
    .bingo-count-display {
        text-align: center;
        color: white;
        font-size: 18px;
        margin-top: 8px;
        font-weight: bold;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        background: rgba(255, 215, 0, 0.3);
        padding: 6px;
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.5);
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

# コントロールボタン
col1, col2, col3 = st.columns([1, 1, 1])
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
    
    st.divider()
    
    # 統計情報
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 項目", len(ITEM_LIST))
    with col2:
        st.metric("✅ マーク", f"{len(st.session_state.marked_cells)}/25")
    with col3:
        st.metric("🎯 ビンゴ", bingo_count)
