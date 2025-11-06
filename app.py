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
        padding: 0.3rem !important;
        height: auto !important;
        min-height: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: clamp(0.65rem, 2.3vw, 0.85rem) !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: 2px solid #333 !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.1 !important;
    }
    
    /* ボタン内のテキストスタイル */
    .stButton > button > div {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 0.2rem !important;
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
    st.session_state.names = None  # 各マスに入力された名前を保存

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
    st.session_state.names = [["" for _ in range(5)] for _ in range(5)]  # 名前を初期化

# ビンゴカードの表示（5×5グリッド）
card = st.session_state.bingo_card
checked = st.session_state.checked
names = st.session_state.names

# 各行を表示
for row_idx in range(5):
    cols = st.columns(5)
    for col_idx in range(5):
        with cols[col_idx]:
            cell_value = card[row_idx][col_idx]
            is_checked = checked[row_idx][col_idx]
            is_free = cell_value == "FREE"
            cell_name = names[row_idx][col_idx]
            
            # ボタンのラベル
            if is_free:
                label = "FREE"
                button_type = "secondary"
            else:
                # 項目名を表示
                label = str(cell_value)
                # 名前が入力されている場合は下に表示
                if cell_name:
                    label = f"{label}\n({cell_name})"
                # チェックマークを追加
                if is_checked:
                    label = f"✓ {label}"
                button_type = "primary" if is_checked else "secondary"
            
            # ボタンを作成
            if st.button(
                label,
                key=f"cell_{row_idx}_{col_idx}",
                type=button_type,
                disabled=is_free,
                use_container_width=True
            ):
                # マスがまだチェックされていない場合は名前入力を促す
                if not is_checked:
                    st.session_state[f"input_modal_{row_idx}_{col_idx}"] = True
                    st.rerun()
                else:
                    # すでにチェック済みの場合はチェックを外す
                    st.session_state.checked[row_idx][col_idx] = False
                    st.session_state.names[row_idx][col_idx] = ""
                    st.rerun()

# 名前入力のダイアログ処理
for row_idx in range(5):
    for col_idx in range(5):
        modal_key = f"input_modal_{row_idx}_{col_idx}"
        if modal_key in st.session_state and st.session_state[modal_key]:
            cell_value = card[row_idx][col_idx]
            
            # ダイアログを表示
            with st.container():
                st.markdown("---")
                st.subheader(f"✏️ 名前を入力してください")
                st.write(f"項目: **{cell_value}**")
                
                name_input = st.text_input(
                    "名前",
                    key=f"name_input_{row_idx}_{col_idx}",
                    placeholder="名前を入力...",
                    label_visibility="collapsed"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✓ 決定", key=f"submit_{row_idx}_{col_idx}", use_container_width=True):
                        st.session_state.checked[row_idx][col_idx] = True
                        st.session_state.names[row_idx][col_idx] = name_input
                        del st.session_state[modal_key]
                        st.rerun()
                
                with col2:
                    if st.button("✕ キャンセル", key=f"cancel_{row_idx}_{col_idx}", use_container_width=True):
                        del st.session_state[modal_key]
                        st.rerun()
                
                st.markdown("---")
            
            # 1つだけダイアログを表示
            break
    else:
        continue
    break

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
    1. **アイテムをタップ**: 呼ばれたアイテムをタップします
    2. **名前を入力**: 名前入力画面が表示されるので、名前を入力して「決定」をタップ
    3. **名前の表示**: 入力した名前が項目の下に表示されます
    4. **チェック解除**: チェック済みのマスをタップすると、チェックと名前が解除されます
    5. **ビンゴ**: 縦・横・斜めのいずれかが揃うとビンゴです
    6. **FREE**: 中央のマスは最初からマーク済みです
    7. **新しいカード**: ページを再読み込みすると新しいカードが生成されます
    8. **カスタマイズ**: コード内のBINGO_ITEMSリストを編集して好きなアイテムに変更できます
    """)
