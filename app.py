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
    "利き手が左手", "名前に自然を表す漢字がある", "スマホがAndroid", "パンが好き", "ラーメンが好き",
    "きのこの山派", "たけのこの里派", "犬を飼っている or 飼っていた", "猫を飼っている or 飼っていた", "蛇を触ったことがある",
    "通勤にバスを使っている", "東京生まれ", "地方生まれ", "NETFLIXのプレミアムに契約している", "ジャングリアに行ったことがある", "YouTubeに出演したことがある",
    "白い眼鏡がチャームポイント", "アプリ通知が100以上溜まっている(1つのアプリで)", "朝のルーティーンがある", "夜のルーティーンがある", "運動が好き",
    "漫画は紙派", "今日二度寝した", "チョコを常備している", "インドア派", "アウトドア派", "チョコミン党", "ブラインドタッチはできない", "コンタクトレンズを付けている",
    "NETFLIXをプレミアムで契約している", "スマホの画面が割れている", "6ヶ月以内に資格を取得した", "ひとりカラオケに行ける", "ひとりで旅行に行ける", "ミスチルが好き", 
    "ウイスキーが好き", "日本酒が好き", "6か月以内にディズニーランドに行った", "6か月以内にUSJに行った", "会社のイスの高さにこだわりがある", "1分の遅刻も許せない",
    "学生時代ファンクラブがあった", "干支が馬", "カレーは飲み物を本気で思っている", "ctrl + D が好き", "よく道に迷う", "兄弟が5人以上いる", "イグアナを飼っている",
    "血液型がAB型", "スマホの充電が残り20%を切っている", "ジムに通っている", "15時間以上寝たことがある", "髪を染めたことがある", "データ活用チームに所属している", "統合運用管理チームに所属している", "クラウドチームに所属している",
    "データベースチームに所属している", "干支が蛇", "干支が辰", "干支が牛", "音楽が好き", "映画が好き", "海外旅行をしたことがある", "自分は穏やかな方だと思う", "ゲームが趣味", "読書が趣味", "通勤に片道1時間以上かかる", "好きな数字は7",
    "夏より冬が好き", "愛と金なら金を取る", "愛と金なら愛を取る", "バッグ・クロージャ―を知っている", "1日1食", "会議でミュート忘れをしたことがある", "学生時代数学が一番得意だった", "学生時代古文が得意だった", "自分はスーツが似合うと思う", 
    "冬より夏が好き", "コンビニと言えばミニストップ", "コンビニと言えばセブン", "コンビニと言えばファミマ", "コンビニと言えばローソン", "コンビニと言えばデイリーヤマザキ", "夜のラーメンがやめられない"
]

# カスタムCSS - スマホ最適化
st.markdown("""
<style>
    /* メインコンテナの調整 */
    .main {
        padding: 0.5rem;
        max-width: 100%;
    }
    
    /* タイトルのスタイル */
    h1 {
        text-align: center;
        font-size: clamp(1.5rem, 5vw, 1.8rem);
        margin-bottom: 1rem;
    }
    
    /* ビンゴカード全体のコンテナ */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Streamlitのボタンを正方形にするスタイル */
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 !important;
        padding: 0.5rem 0.2rem !important;
        height: auto !important;
        min-height: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: clamp(0.7rem, 3vw, 1rem) !important;
        font-weight: normal !important;
        border-radius: 8px !important;
        border: 2px solid #333 !important;
        white-space: pre-line !important;
        word-wrap: break-word !important;
        line-height: 1.4 !important;
        box-sizing: border-box !important;
    }
    
    /* ボタン内のテキストスタイル */
    .stButton > button > div {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.2rem !important;
        text-align: center !important;
        width: 100% !important;
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
        padding: 0.15rem !important;
    }
    
    /* 行の間隔調整 */
    .row-widget.stHorizontal {
        gap: 0 !important;
    }
    
    /* Streamlitのデフォルト余白を削除 */
    .element-container {
        margin-bottom: 0.3rem !important;
    }
    
    .row-widget {
        margin-bottom: 0 !important;
    }
    
    /* スマホ画面での調整 */
    @media (max-width: 768px) {
        .main {
            padding: 0.3rem;
        }
        
        h1 {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }
        
        .stButton > button {
            font-size: clamp(0.65rem, 3.5vw, 0.9rem) !important;
            padding: 0.3rem 0.1rem !important;
            border-width: 1.5px !important;
        }
        
        div[data-testid="column"] {
            padding: 0.1rem !important;
        }
    }
    
    /* 非常に小さい画面（モバイル）での調整 */
    @media (max-width: 480px) {
        .main {
            padding: 0.2rem;
        }
        
        h1 {
            font-size: 1.3rem;
        }
        
        .stButton > button {
            font-size: clamp(0.6rem, 3.8vw, 0.85rem) !important;
            padding: 0.25rem 0.1rem !important;
            line-height: 1.3 !important;
        }
        
        div[data-testid="column"] {
            padding: 0.08rem !important;
        }
        
        .element-container {
            margin-bottom: 0.2rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'bingo_card' not in st.session_state:
    st.session_state.bingo_card = None
    st.session_state.checked = None
    st.session_state.names = None  # 各マスに入力された名前を保存
    st.session_state.current_cell = None  # 現在編集中のセル

@st.dialog("✏️ 名前を入力してください")
def show_name_input_dialog(row, col, cell_value):
    """名前入力用のモーダルダイアログ"""
    st.write(f"項目: **{cell_value}**")
    
    name_input = st.text_input(
        "名前",
        key=f"name_input_{row}_{col}",
        placeholder="名前を入力...",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✓ 決定", key=f"submit_{row}_{col}", use_container_width=True):
            st.session_state.checked[row][col] = True
            st.session_state.names[row][col] = name_input
            st.session_state.current_cell = None
            st.rerun()
    
    with col2:
        if st.button("✕ キャンセル", key=f"cancel_{row}_{col}", use_container_width=True):
            st.session_state.current_cell = None
            st.rerun()


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
                # チェックマークを追加
                if is_checked:
                    label = f"✓ {label}"
                # 名前が入力されている場合は改行して表示
                if cell_name:
                    label = f"{label}\n\n{cell_name}"
                button_type = "primary" if is_checked else "secondary"
            
            # ボタンを作成
            if st.button(
                label,
                key=f"cell_{row_idx}_{col_idx}",
                type=button_type,
                disabled=is_free,
                use_container_width=True
            ):
                # マスがまだチェックされていない場合は名前入力ダイアログを表示
                if not is_checked:
                    st.session_state.current_cell = (row_idx, col_idx)
                    st.rerun()
                else:
                    # すでにチェック済みの場合はチェックを外す
                    st.session_state.checked[row_idx][col_idx] = False
                    st.session_state.names[row_idx][col_idx] = ""
                    st.rerun()

# ダイアログの表示処理
if st.session_state.current_cell is not None:
    row, col = st.session_state.current_cell
    cell_value = card[row][col]
    show_name_input_dialog(row, col, cell_value)

# ビンゴのチェック
bingo_count = check_bingo(st.session_state.checked)

# ビンゴ状態の表示
st.markdown("---")
if bingo_count > 0:
    st.balloons()  # 風船を表示
    st.success(f"🎉 {bingo_count}つのビンゴが揃いました！")
else:
    st.info("💡 アイテムをタップしてマークしましょう！")

