import streamlit as st
import random

# ページ設定
st.set_page_config(
    page_title="ビンゴカード",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ビンゴカードに表示するアイテムのリスト
# ここを自由に変更してください
BINGO_ITEMS = [
    "リンゴ", "バナナ", "イチゴ", "ブドウ", "メロン",
    "スイカ", "桃", "梨", "柿", "みかん",
    "キウイ", "マンゴー", "パイナップル", "レモン", "オレンジ",
    "さくらんぼ", "プラム", "アボカド", "パパイヤ", "グァバ",
    "ライチ", "ドラゴンフルーツ", "パッションフルーツ", "ザクロ", "いちじく"
]

# カスタムCSS - スマホ最適化
st.markdown("""
<style>
    /* メインコンテナの調整 */
    .main {
        padding: 0.5rem;
        max-width: 600px;
    }
    
    /* タイトルのスタイル */
    h1 {
        text-align: center;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    
    /* ビンゴカード全体のコンテナ */
    .bingo-grid-container {
        width: 100%;
        max-width: 500px;
        margin: 0 auto;
    }
    
    /* Streamlitのボタンを正方形にするスタイル */
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 !important;
        padding: 0 !important;
        height: auto !important;
        min-height: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: clamp(0.7rem, 2.5vw, 0.9rem) !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: 2px solid #333 !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.2 !important;
    }
    
    /* チェック済みボタン（primary） */
    .stButton > button[kind="primary"] {
        background-color: #ff6b6b !important;
        color: white !important;
        border-color: #ff6b6b !important;
    }
    
    /* 未チェックボタン（secondary） */
    .stButton > button[kind="secondary"] {
        background-color: #ffffff !important;
        color: #333 !important;
        border-color: #333 !important;
    }
    
    /* FREEマス */
    .stButton > button:disabled {
        background-color: #4ecdc4 !important;
        color: white !important;
        border-color: #4ecdc4 !important;
        opacity: 1 !important;
    }
    
    /* カラムの間隔調整 */
    div[data-testid="column"] {
        padding: 2px !important;
    }
    
    /* Streamlitのデフォルト余白を削除 */
    .element-container {
        margin-bottom: 0 !important;
    }
    
    .row-widget {
        margin-bottom: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'bingo_card' not in st.session_state:
    st.session_state.bingo_card = None
    st.session_state.checked = None

def generate_bingo_card():
    """リストからランダムに選んでビンゴカードを生成"""
    # 25マス分必要なので、リストをシャッフルして使用
    if len(BINGO_ITEMS) < 24:  # 24個（中央はFREE）
        # アイテムが足りない場合は重複を許可
        selected_items = random.choices(BINGO_ITEMS, k=24)
    else:
        # アイテムが十分ある場合は重複なしで選択
        selected_items = random.sample(BINGO_ITEMS, 24)
    
    card = []
    item_index = 0
    
    for row in range(5):
        row_data = []
        for col in range(5):
            if row == 2 and col == 2:
                # 中央はフリースペース
                row_data.append("FREE")
            else:
                row_data.append(selected_items[item_index])
                item_index += 1
        card.append(row_data)
    
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

# アプリを開いた時に毎回新しいカードを生成
if st.session_state.bingo_card is None:
    st.session_state.bingo_card = generate_bingo_card()
    st.session_state.checked = [[False for _ in range(5)] for _ in range(5)]
    st.session_state.checked[2][2] = True  # フリースペースは最初からチェック済み

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
    st.info("💡 アイテムをタップしてマークしましょう！")

# 使い方の説明（折りたたみ式）
with st.expander("📖 使い方"):
    st.markdown("""
    1. **アイテムをタップ**: 呼ばれたアイテムをタップしてマークします
    2. **ビンゴ**: 縦・横・斜めのいずれかが揃うとビンゴです
    3. **FREE**: 中央のマスは最初からマーク済みです
    4. **新しいカード**: ページを再読み込みすると新しいカードが生成されます
    5. **カスタマイズ**: コード内のBINGO_ITEMSリストを編集して好きなアイテムに変更できます
    """)
