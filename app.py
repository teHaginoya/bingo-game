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
        font-size: 14px;
        font-weight: bold;
        border-radius: 10px;
        white-space: normal;
        word-wrap: break-word;
        line-height: 1.3;
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
    st.session_state.marked_cells = {}  # {(row, col): "名前"}の辞書
if 'selected_cell' not in st.session_state:
    st.session_state.selected_cell = None

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
    st.session_state.marked_cells[(2, 2)] = "FREE"
    
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

# 初回アクセス時に自動でカード生成
if st.session_state.bingo_card is None and len(ITEM_LIST) >= 24:
    st.session_state.bingo_card = generate_bingo_card(ITEM_LIST)
    st.session_state.marked_cells = {(2, 2): "FREE"}

# タイトルとコントロール
st.title("🎯 ビンゴカード")

# コントロールボタン
col1, col2 = st.columns(2)
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

st.divider()

# ダイアログ表示（修正版）
@st.dialog("名前を入力してください")
def name_input_dialog(row, col):
    item_name = st.session_state.bingo_card[row][col]
    st.write(f"**項目:** {item_name}")
    
    # 既存の名前があれば表示
    current_name = st.session_state.marked_cells.get((row, col), "")
    
    name = st.text_input("お名前", value=current_name, key=f"name_input_{row}_{col}", placeholder="山田太郎")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ 登録", use_container_width=True, key=f"register_{row}_{col}"):
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
        if st.button("❌ キャンセル", use_container_width=True, key=f"cancel_{row}_{col}"):
            st.session_state.selected_cell = None
            st.rerun()

# 選択されたセルがある場合、ダイアログを表示
if st.session_state.selected_cell:
    row, col = st.session_state.selected_cell
    name_input_dialog(row, col)

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
                # FREEマス
                if value == 'FREE':
                    st.button(
                        "⭐ FREE",
                        key=f"cell_{row}_{col}",
                        disabled=True,
                        use_container_width=True,
                        type="primary"
                    )
                # マーク済みマス
                elif is_marked:
                    name = st.session_state.marked_cells[(row, col)]
                    # 項目名と名前を改行で分けて表示
                    button_text = f"{value}\n---\n✅ {name}"
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
    col1, col2 = st.columns(2)
    with col1:
        st.metric("マーク済み", f"{len(st.session_state.marked_cells)}/25")
    with col2:
        st.metric("ビンゴライン", bingo_count)
