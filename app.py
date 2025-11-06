import streamlit as st
import random

st.set_page_config(
    page_title="ビンゴゲーム", 
    page_icon="🎯", 
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: 80px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# セッションステートの初期化
if 'item_list' not in st.session_state:
    st.session_state.item_list = []
if 'bingo_card' not in st.session_state:
    st.session_state.bingo_card = None
if 'marked_cells' not in st.session_state:
    st.session_state.marked_cells = set()

def generate_bingo_card(items):
    """カスタム項目でビンゴカードを生成"""
    if len(items) < 24:
        return None
    
    # 24個をランダムに選択（中央はFREE）
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

# サイドバー：項目管理
with st.sidebar:
    st.header("📝 項目管理")
    
    # 新規項目追加
    new_item = st.text_input("新しい項目を追加", key="new_item_input")
    if st.button("➕ 追加", use_container_width=True):
        if new_item and new_item not in st.session_state.item_list:
            st.session_state.item_list.append(new_item)
            st.success(f"追加しました: {new_item}")
            st.rerun()
        elif new_item in st.session_state.item_list:
            st.warning("既に登録されています")
        else:
            st.warning("項目を入力してください")
    
    st.divider()
    
    # 登録済み項目リスト
    st.subheader(f"登録項目 ({len(st.session_state.item_list)}個)")
    
    if st.session_state.item_list:
        # 項目削除
        items_to_delete = []
        for i, item in enumerate(st.session_state.item_list):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i+1}. {item}")
            with col2:
                if st.button("🗑️", key=f"delete_{i}"):
                    items_to_delete.append(item)
        
        # 削除処理
        for item in items_to_delete:
            st.session_state.item_list.remove(item)
            st.rerun()
        
        st.divider()
        
        # 全削除
        if st.button("🗑️ 全て削除", use_container_width=True):
            st.session_state.item_list = []
            st.session_state.bingo_card = None
            st.session_state.marked_cells = set()
            st.rerun()
    else:
        st.info("項目を追加してください")
    
    st.divider()
    
    # カード生成
    st.subheader("🎯 ビンゴカード")
    
    if len(st.session_state.item_list) >= 24:
        if st.button("🆕 新しいカードを生成", use_container_width=True):
            st.session_state.bingo_card = generate_bingo_card(st.session_state.item_list)
            st.session_state.marked_cells = {(2, 2)}
            st.rerun()
        
        if st.session_state.bingo_card is not None:
            if st.button("🔄 リセット", use_container_width=True):
                st.session_state.marked_cells = {(2, 2)}
                st.rerun()
    else:
        st.warning(f"あと{24 - len(st.session_state.item_list)}個必要です（最低24個）")

# メインエリア：ビンゴカード表示
st.title("🎯 ビンゴカード")

if st.session_state.bingo_card is None:
    st.info("👈 サイドバーで項目を追加して、カードを生成してください")
else:
    # ビンゴ判定
    bingo_count = check_bingo(st.session_state.marked_cells)
    
    if bingo_count > 0:
        st.balloons()
        st.success(f"🎉 {bingo_count}ライン達成！")
    
    st.divider()
    
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
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("総項目数", len(st.session_state.item_list))
    with col2:
        st.metric("マーク済み", len(st.session_state.marked_cells))
    with col3:
        st.metric("ビンゴライン", bingo_count)
