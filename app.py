import streamlit as st
import random

st.set_page_config(
    page_title="ビンゴゲーム", 
    page_icon="🎯", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# カスタムCSS - UIを美しく
st.markdown("""
    <style>
    /* 全体の背景をグラデーションに */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* メインコンテンツエリア */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    
    /* タイトルスタイル */
    h1 {
        color: white;
        text-align: center;
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* ボタンのスタイル */
    .stButton button {
        width: 100%;
        height: 90px;
        font-size: 15px;
        font-weight: bold;
        border-radius: 15px;
        white-space: normal;
        word-wrap: break-word;
        line-height: 1.4;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* ボタンホバー効果 */
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    /* プライマリボタン（マーク済み） */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 3px solid #FFD700;
    }
    
    /* セカンダリボタン（未マーク） */
    .stButton button[kind="secondary"] {
        background: white;
        color: #333;
        border: 2px solid #ddd;
    }
    
    /* コントロールボタン */
    div[data-testid="column"]:has(.stButton) .stButton button {
        height: 50px;
        font-size: 16px;
        border-radius: 25px;
    }
    
    /* メトリクスカード */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: white;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: white !important;
        font-size: 16px;
    }
    
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 区切り線 */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
    }
    
    /* 成功メッセージ */
    .stSuccess {
        background: rgba(40, 167, 69, 0.9);
        color: white;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
    }
    
    /* ダイアログのスタイル */
    [data-testid="stModal"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
    }
    
    /* テキスト入力 */
    .stTextInput input {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 10px;
        font-size: 16px;
    }
    
    /* エラーメッセージ */
    .stError {
        background: rgba(220, 53, 69, 0.9);
        color: white;
        padding: 15px;
        border-radius: 10px;
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

# 初回アクセス時に自動でカード生成
if st.session_state.bingo_card is None and len(ITEM_LIST) >= 24:
    st.session_state.bingo_card = generate_bingo_card(ITEM_LIST)
    st.session_state.marked_cells = {(2, 2): "FREE"}

# タイトル
st.title("🎯 ビンゴカード")

# コントロールボタン
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🆕 新しいカード", use_container_width=True):
        st.session_state.bingo_card = generate_bingo_card(ITEM_LIST)
        st.session_state.marked_cells = {(2, 2): "FREE"}
        st.session_state.selected_cell = None
        st.rerun()

with col2:
    if st.button("🔄 リセット", use_container_width=True):
        st.session_state.marked_cells = {(2, 2): "FREE"}
        st.session_state.selected_cell = None
        st.rerun()

with col3:
    # 統計をここに表示
    if st.session_state.bingo_card:
        bingo_count = check_bingo(st.session_state.marked_cells)
        st.markdown(f"<div style='text-align: center; color: white; font-size: 18px; margin-top: 10px;'>🏆 {bingo_count}ライン</div>", unsafe_allow_html=True)

st.divider()

# ダイアログ表示
@st.dialog("✨ 名前を入力")
def name_input_dialog(row, col):
    item_name = st.session_state.bingo_card[row][col]
    st.markdown(f"### 📝 {item_name}")
    
    current_name = st.session_state.marked_cells.get((row, col), "")
    
    name = st.text_input("👤 お名前", value=current_name, key=f"name_input_{row}_{col}", placeholder="例: 山田太郎")
    
    st.write("")  # スペース
    
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
    
    if bingo_count > 0:
        st.balloons()
        st.success(f"🎉🎊 おめでとうございます！{bingo_count}ライン達成！ 🎊🎉")
    
    # ビンゴカード表示
    for row in range(5):
        cols = st.columns(5)
        for col in range(5):
            value = st.session_state.bingo_card[row][col]
            is_marked = (row, col) in st.session_state.marked_cells
            
            with cols[col]:
                # FREEマス
                if value == 'FREE':
                    st.button(
                        "⭐ FREE ⭐",
                        key=f"cell_{row}_{col}",
                        disabled=True,
                        use_container_width=True,
                        type="primary"
                    )
                # マーク済みマス
                elif is_marked:
                    name = st.session_state.marked_cells[(row, col)]
                    button_text = f"{value}\n\n✅ {name}"
                    if st.button(
                        button_text,
                        key=f"cell_{row}_{col}",
                        use_container_width=True,
                        type="primary"
                    ):
                        st.session_state.selected_cell = (row, col)
                        st.rerun()
                # 未マークマス
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
        st.metric("📊 総項目数", len(ITEM_LIST))
    with col2:
        st.metric("✅ マーク済み", f"{len(st.session_state.marked_cells)}/25")
    with col3:
        st.metric("🎯 ビンゴライン", bingo_count)
