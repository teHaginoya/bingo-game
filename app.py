import streamlit as st
import random

st.set_page_config(
    page_title="ビンゴゲーム", 
    page_icon="🎯", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: 80px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
        white-space: normal;
        word-wrap: break-word;
    }
    </style>
    """, unsafe_allow_html=True)

# ===== ここに項目リストを追加してください =====
ITEM_LIST = [
    "項目1",
    "項目2",
    "項目3",
    "項目4",
    "項目5",
    "項目6",
    "項目7",
    "項目8",
    "項目9",
    "項目10",
    "項目11",
    "項目12",
    "項目13",
    "項目14",
    "項目15",
    "項目16",
    "項目17",
    "項目18",
    "項目19",
    "項目20",
    "項目21",
    "項目22",
    "項目23",
    "項目24",
    # 必要に応じて追加してください（24個以上推奨）
]
# ==========================================

# セッションステートの初期化
if 'bingo_card' not in st.session_state:
    st.session_state.bingo_card = None
if 'marked_cells' not in st.session_state:
    st.session_state.marked_cells = set()

def generate_bingo_card(items):
    """カスタム項目でビンゴカードを生成"""
    if len(items) < 24:
        return None
    
    # 24個をランダムに選択
    selected = random.sample(items, 24)
    
    # 5x5の配列に変換
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
    
    # FREEを最初からマーク
    st.session_state.marked_cells.add((2, 2))
    
    return card

def check_bingo(marked):
    """ビンゴ判定"""
    bingo_count = 0
    
    # 横
    for row in range(5):
        if all((row, col) in marked for col in range(5)):
            bingo_count += 1
    
    # 縦
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

def toggle_cell(row, col):
    """セルのマーク状態を切り替え"""
    if (row, col) in st.session_state.marked_cells:
        st.session_state.marked_cells.remove((row, col))
    else:
        st.session_state.marked_cells.add((row, col))

# 初回アクセス時に自動でカード生成
if st.session_state.bingo_card is None and len(ITEM_LIST) >= 24:
    st.session_state.bingo_card = generate_bingo_card(ITEM_LIST)
    st.session_state.marked_cells = {(2, 2)}

# タイトルとコントロール
st.title("🎯 ビンゴカード")

# コントロールボタン（コンパクトに配置）
col1, col2 = st.columns(2)
with col1:
    if st.button("🆕 新しいカード", use_container_width=True):
        st.session_state.bingo_card = generate_bingo_card(ITEM_LIST)
        st.session_state.marked_cells = {(2, 2)}
        st.rerun()
with col2:
    if st.button("🔄 リセット", use_container_width=True):
        st.session_state.marked_cells = {(2, 2)}
        st.rerun()

st.divider()

# ビンゴカード表示
if st.session_state.bingo_card is None:
    st.error("項目が不足しています（最低24個必要）")
else:
    # ビンゴ判定
    bingo_count = check_bingo(st.session_state.marked_cells)
    
    if bingo_count > 0:
        st.balloons()
        st.success(f"🎉 {bingo_count}ライン達成！")
    
    # ビンゴカード表示
    for row in range(5):
        cols = st.columns(5)
        for col in range(5):
            value = st.session_state.bingo_card[row][col]
            is_marked = (row, col) in st.session_state.marked_cells
            
            with cols[col]:
                # タッチして開く仕様
                if value == 'FREE':
                    st.button(
                        "⭐ FREE",
                        key=f"cell_{row}_{col}",
                        disabled=True,
                        use_container_width=True,
                        type="primary"
                    )
                elif is_marked:
                    if st.button(
                        f"✅\n{value}",
                        key=f"cell_{row}_{col}",
                        use_container_width=True,
                        type="primary"
                    ):
                        toggle_cell(row, col)
                        st.rerun()
                else:
                    if st.button(
                        value,
                        key=f"cell_{row}_{col}",
                        use_container_width=True,
                        type="secondary"
                    ):
                        toggle_cell(row, col)
                        st.rerun()
    
    st.divider()
    
    # 統計情報
    col1, col2 = st.columns(2)
    with col1:
        st.metric("マーク済み", f"{len(st.session_state.marked_cells)}/25")
    with col2:
        st.metric("ビンゴライン", bingo_count)
