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
        height: 60px;
        font-size: 18px;
        font-weight: bold;
    }
    .stMarkdown {
        font-size: 20px;
        text-align: center;
    }
    [data-testid="stMetricValue"] {
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'bingo_card' not in st.session_state:
    st.session_state.bingo_card = None
if 'called_numbers' not in st.session_state:
    st.session_state.called_numbers = []
if 'marked_cells' not in st.session_state:
    st.session_state.marked_cells = set()

def generate_bingo_card():
    card = []
    for col in range(5):
        start = col * 15 + 1
        end = start + 15
        numbers = random.sample(range(start, end), 5)
        card.append(numbers)
    
    card[2][2] = 'FREE'
    st.session_state.marked_cells.add((2, 2))
    
    return card

def check_bingo(card, marked):
    bingo_count = 0
    
    for row in range(5):
        if all((col, row) in marked for col in range(5)):
            bingo_count += 1
    
    for col in range(5):
        if all((col, row) in marked for row in range(5)):
            bingo_count += 1
    
    if all((i, i) in marked for i in range(5)):
        bingo_count += 1
    
    if all((i, 4-i) in marked for i in range(5)):
        bingo_count += 1
    
    return bingo_count

def call_number():
    all_numbers = set(range(1, 76))
    available = all_numbers - set(st.session_state.called_numbers)
    
    if available:
        number = random.choice(list(available))
        st.session_state.called_numbers.append(number)
        
        for col in range(5):
            for row in range(5):
                if st.session_state.bingo_card[col][row] == number:
                    st.session_state.marked_cells.add((col, row))
        
        return number
    return None

st.title("🎯 ビンゴゲーム")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🆕 新規", use_container_width=True):
        st.session_state.bingo_card = generate_bingo_card()
        st.session_state.called_numbers = []
        st.session_state.marked_cells = {(2, 2)}
        st.rerun()

with col2:
    if st.session_state.bingo_card is not None:
        if st.button("🎲 抽選", use_container_width=True):
            number = call_number()
            if number:
                st.toast(f"🎲 {number}", icon="🎲")
            else:
                st.warning("終了！")

with col3:
    if st.button("🔄 リセット", use_container_width=True):
        st.session_state.bingo_card = None
        st.session_state.called_numbers = []
        st.session_state.marked_cells = set()
        st.rerun()

st.divider()

if st.session_state.called_numbers:
    latest = st.session_state.called_numbers[-1]
    st.markdown(f"### 最新: :blue[{latest}]")
    
    if len(st.session_state.called_numbers) > 1:
        with st.expander(f"📋 履歴 ({len(st.session_state.called_numbers)}個)"):
            recent = st.session_state.called_numbers[-10:][::-1]
            st.write(", ".join(map(str, recent)))

st.divider()

if st.session_state.bingo_card is None:
    st.info("👆「🆕 新規」ボタンを押してスタート")
else:
    bingo_count = check_bingo(st.session_state.bingo_card, st.session_state.marked_cells)
    
    if bingo_count > 0:
        st.balloons()
        st.success(f"🎉 {bingo_count}ライン ビンゴ！")
    
    cols = st.columns(5)
    headers = ['B', 'I', 'N', 'G', 'O']
    for i, header in enumerate(headers):
        cols[i].markdown(f"### {header}")
    
    for row in range(5):
        cols = st.columns(5)
        for col in range(5):
            value = st.session_state.bingo_card[col][row]
            is_marked = (col, row) in st.session_state.marked_cells
            
            with cols[col]:
                if is_marked:
                    if value == 'FREE':
                        st.markdown(f"## :green[★]")
                    else:
                        st.markdown(f"## :red[{value}]")
                else:
                    st.markdown(f"## {value}")
    
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("抽選", f"{len(st.session_state.called_numbers)}")
    with col2:
        st.metric("マーク", f"{len(st.session_state.marked_cells)}")
    with col3:
        st.metric("ビンゴ", bingo_count)
```

**② `requirements.txt`** (Add file → Create new file)
```
streamlit
