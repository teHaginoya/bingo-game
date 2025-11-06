import streamlit as st
import random

# ページ設定
st.set_page_config(
    page_title="ビンゴカード",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# カスタムCSS - スマホ最適化
st.markdown("""
<style>
    /* メインコンテナの調整 */
    .main {
        padding: 0.5rem;
    }
    
    /* タイトルのスタイル */
    h1 {
        text-align: center;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    
    /* ビンゴカードのコンテナ */
    .bingo-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 4px;
        max-width: 100%;
        margin: 0 auto;
        aspect-ratio: 1;
    }
    
    /* ビンゴのマス */
    .bingo-cell {
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #333;
        border-radius: 8px;
        font-size: clamp(1rem, 4vw, 1.5rem);
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        user-select: none;
    }
    
    .bingo-cell.unchecked {
        background-color: #ffffff;
        color: #333;
    }
    
    .bingo-cell.checked {
        background-color: #ff6b6b;
        color: white;
    }
    
    .bingo-cell.free {
        background-color: #4ecdc4;
        color: white;
    }
    
    /* ボタンのスタイル */
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 8px;
        border: none;
        margin-top: 1rem;
    }
    
    /* Streamlitのデフォルトスタイルを上書き */
    .element-container {
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'bingo_card' not in st.session_state:
    st.session_state.bingo_card = None
    st.session_state.checked = None

def generate_bingo_card():
    """1-75のランダムな数字でビンゴカードを生成"""
    card = []
    for _ in range(5):
        row = []
        for _ in range(5):
            row.append(random.randint(1, 75))
        card.append(row)
    
    # 中央をフリースペースに
    card[2][2] = "FREE"
    
    return card

def check_bingo(checked):
    """ビンゴが揃っているかチェック"""
    bingo_lines = 0
    
    # 横のチェック
    for row in range(5):
        if all(checked[row]):
            bingo_lines += 1
    
    # 縦のチェック
    for col in range(5):
        if all(checked[row][col] for row in range(5)):
            bingo_lines += 1
    
    # 斜めのチェック（左上から右下）
    if all(checked[i][i] for i in range(5)):
        bingo_lines += 1
    
    # 斜めのチェック（右上から左下）
    if all(checked[i][4-i] for i in range(5)):
        bingo_lines += 1
    
    return bingo_lines

# タイトル
st.title("🎯 ビンゴカード")

# 新しいカードを生成ボタン
if st.button("🔄 新しいカードを生成"):
    st.session_state.bingo_card = generate_bingo_card()
    st.session_state.checked = [[False for _ in range(5)] for _ in range(5)]
    st.session_state.checked[2][2] = True  # フリースペースは最初からチェック済み
    st.rerun()

# 初回訪問時にカードを自動生成
if st.session_state.bingo_card is None:
    st.session_state.bingo_card = generate_bingo_card()
    st.session_state.checked = [[False for _ in range(5)] for _ in range(5)]
    st.session_state.checked[2][2] = True

# ビンゴカードの表示（5×5グリッド）
card = st.session_state.bingo_card
checked = st.session_state.checked

# 各行を表示
for row_idx in range(5):
    cols = st.columns(5)
    for col_idx in range(5):
        with cols[col_idx]:
            cell_value = card[row_idx][col_idx]
            is_checked = checked[row_idx][col_idx]
            is_free = cell_value == "FREE"
            
            # ボタンのラベル
            if is_free:
                label = "FREE"
                button_type = "secondary"
            else:
                label = str(cell_value)
                button_type = "primary" if is_checked else "secondary"
            
            # マークを追加
            if is_checked and not is_free:
                label = f"✓ {label}"
            
            # ボタンを作成
            if st.button(
                label,
                key=f"cell_{row_idx}_{col_idx}",
                type=button_type,
                disabled=is_free,
                use_container_width=True
            ):
                # チェック状態を反転
                st.session_state.checked[row_idx][col_idx] = not is_checked
                st.rerun()

# ビンゴのチェック
bingo_count = check_bingo(st.session_state.checked)

# ビンゴ状態の表示
st.markdown("---")
if bingo_count > 0:
    st.success(f"🎉 {bingo_count}つのビンゴが揃いました！")
else:
    st.info("💡 数字をタップしてマークしましょう！")

# 使い方の説明（折りたたみ式）
with st.expander("📖 使い方"):
    st.markdown("""
    1. **数字をタップ**: 呼ばれた数字をタップしてマークします
    2. **ビンゴ**: 縦・横・斜めのいずれかが揃うとビンゴです
    3. **新しいカード**: 上部のボタンで新しいカードを生成できます
    4. **FREE**: 中央のマスは最初からマーク済みです
    """)
