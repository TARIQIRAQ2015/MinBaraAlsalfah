import streamlit as st
import random
from categories import categories  

# تعيين نمط CSS مخصص
st.markdown("""
<style>
    /* تخصيص الخط والألوان الرئيسية */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700&display=swap');
    
    * {
        font-family: 'Noto Kufi Arabic', sans-serif !important;
    }
    
    /* تنسيق العنوان الرئيسي */
    h1 {
        color: #2c3e50;
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
        background: linear-gradient(45deg, #3498db, #2ecc71);
        border-radius: 10px;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* تنسيق الأزرار */
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(45deg, #3498db, #2ecc71);
        color: white;
        font-weight: bold;
        border: none;
        padding: 15px;
        margin: 5px 0;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* تنسيق مربعات النص */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #3498db;
        padding: 10px;
    }
    
    /* تنسيق القوائم المنسدلة */
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #3498db;
    }
    
    /* تنسيق النص العادي */
    p {
        font-size: 18px;
        color: #2c3e50;
        line-height: 1.6;
    }
    
    /* تنسيق البطاقات */
    .card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* تنسيق النتائج والنقاط */
    .score {
        font-size: 24px;
        font-weight: bold;
        color: #2ecc71;
    }
    
    /* تنسيق التحذيرات */
    .stAlert {
        border-radius: 10px;
    }
    
    /* تنسيق خاص للاعب برا السالفة */
    .bara-player {
        color: #e74c3c;
        font-weight: bold;
    }
    
    /* تنسيق خاص للكلمة السرية */
    .secret-word {
        color: #9b59b6;
        font-weight: bold;
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state when the app starts
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'players' not in st.session_state:
    st.session_state.players = []
if 'num_players' not in st.session_state:
    st.session_state.num_players = 0
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'roles' not in st.session_state:
    st.session_state.roles = {}
if 'bara_al_salfa' not in st.session_state:
    st.session_state.bara_al_salfa = None
if 'game_word' not in st.session_state:
    st.session_state.game_word = None
if 'current_player_index' not in st.session_state:
    st.session_state.current_player_index = 0
if 'votes' not in st.session_state:
    st.session_state.votes = {}
if 'round_scores' not in st.session_state:
    st.session_state.round_scores = {}
if 'global_scores' not in st.session_state:
    st.session_state.global_scores = {}
if 'guess_word_options' not in st.session_state:
    st.session_state.guess_word_options = []
if 'round_complete' not in st.session_state:
    st.session_state.round_complete = False
if 'question_pairs' not in st.session_state:
    st.session_state.question_pairs = []
if 'current_pair_index' not in st.session_state:
    st.session_state.current_pair_index = 0
if 'vote_index' not in st.session_state:
    st.session_state.vote_index = 0
if 'guess_result' not in st.session_state:
    st.session_state.guess_result = ''

# Function to reset state for a new round
def reset_for_new_round():
    st.session_state.current_player_index = 0
    st.session_state.current_pair_index = 0
    st.session_state.vote_index = 0
    st.session_state.round_complete = False
    st.session_state.votes = {}
    st.session_state.round_scores = {player: 0 for player in st.session_state.players if player.strip()}

# Function to assign roles and choose the secret word
def assign_roles_and_word():
    st.session_state.game_word = random.choice(categories[st.session_state.selected_category])
    st.session_state.bara_al_salfa = random.choice(st.session_state.players)
    st.session_state.roles = {player: 'برة السالفة' if player == st.session_state.bara_al_salfa else 'داخل السالفة' for player in st.session_state.players}
    st.session_state.question_pairs = generate_question_pairs(st.session_state.players)
    set_page('show_role')

# Function to generate questions paris for the round
def generate_question_pairs(players):
    random.shuffle(players)
    pairs = [(players[i], players[(i + 1) % len(players)]) for i in range(len(players))]
    return pairs

# Function to generate guess options for "برة السالفة"
def generate_guess_options():
    category_words = categories[st.session_state.selected_category]
    st.session_state.guess_word_options = random.sample(
        [word for word in category_words if word != st.session_state.game_word], 7
    ) + [st.session_state.game_word]
    random.shuffle(st.session_state.guess_word_options)

# Function to handle the guessing of the secret word by "برة السالفة"
def handle_bara_guess(guess):
    if guess == st.session_state.game_word:
        st.session_state.round_scores[st.session_state.bara_al_salfa] += 10
        st.session_state.guess_result = "صحيح! لقد خمنت الكلمة السرية بشكل صحيح وحصلت على 10 نقاط."
    else:
        st.session_state.guess_result = "خطأ! لم تخمن الكلمة السرية بشكل صحيح."
    set_page('total_scores')

# Callback function to set the page
def set_page(page):
    st.session_state.page = page

# Ensure players list is initialized based on the number of players
def initialize_players():
    st.session_state.players = ['' for _ in range(st.session_state.num_players)]
    st.session_state.global_scores = {player: 0 for player in st.session_state.players if player.strip()}

# Page layouts
def home_page():
    st.markdown("<h1>🎮 لعبة برا السالفة</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p style='text-align: center; font-size: 20px;'>
            مرحباً بك في لعبة برا السالفة! 🎉<br>
            لعبة اجتماعية ممتعة تجمع بين الذكاء والمرح
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.number_input("👥 أدخل عدد اللاعبين (3-12):", min_value=3, max_value=12, step=1, key="num_players")
        st.button("🎮 ابدأ اللعبة", on_click=lambda: (initialize_players(), set_page('input_players')))

def input_players_page():
    st.markdown("<h1>✍️ أدخل أسماء اللاعبين</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        for i in range(st.session_state.num_players):
            st.text_input(f"🎮 اللاعب {i+1}:", value=st.session_state.players[i], key=f"player_{i}")
            st.session_state.players[i] = st.session_state[f"player_{i}"]
    
    if not all(name.strip() for name in st.session_state.players):
        st.warning("⚠️ من فضلك أدخل أسماء جميع اللاعبين")
        return
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("👉 التالي", on_click=set_page, args=['select_category'])

def select_category_page():
    st.markdown("<h1>📚 اختر القائمة</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.selectbox("🎯 اختر قائمة الكلمات:", options=list(categories.keys()), key="category_select")
        st.session_state.selected_category = st.session_state.category_select
        st.button("✅ تأكيد القائمة", on_click=assign_roles_and_word)

def show_role_page():
    st.markdown("<h1>👀 عرض الدور</h1>", unsafe_allow_html=True)
    current_player = st.session_state.players[st.session_state.current_player_index]
    
    st.markdown(f"""
    <div class="card">
        <p style='text-align: center; font-size: 24px;'>
            🎮 أعط الشاشة إلى: <span class='bara-player'>{current_player}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("👁️ عرض الدور", on_click=set_page, args=['display_role'])

def display_role_page():
    current_player = st.session_state.players[st.session_state.current_player_index]
    role = st.session_state.roles[current_player]
    
    st.markdown("<h1>🎭 دورك في اللعبة</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card">
        <p>القائمة: <span style='color: #3498db; font-weight: bold;'>{st.session_state.selected_category}</span></p>
        <p>مرحباً <span class='bara-player'>{current_player}</span></p>
        <p>دورك هو: <span style='color: #e74c3c; font-weight: bold;'>{role}</span></p>
    """, unsafe_allow_html=True)
    
    if role == 'داخل السالفة':
        st.markdown(f"""
        <p>الكلمة السرية هي: <span class='secret-word'>{st.session_state.game_word}</span></p>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p style='color: #e67e22; font-weight: bold;'>مهمتك أن توضح للمجموعة أنك تعرف الموضوع بالإجابة بشكل عام.</p>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.session_state.current_player_index < len(st.session_state.players) - 1:
            st.button("👉 التالي", on_click=lambda: (st.session_state.update({'current_player_index': st.session_state.current_player_index + 1}), set_page('show_role')))
        else:
            st.button("🎮 بدء اللعب", on_click=set_page, args=['question_or_vote'])

def question_or_vote_page():
    st.markdown("<h1>🤔 ماذا تريد أن تفعل الآن؟</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p style='text-align: center;'>
            يجب على اللاعبين الآن أن يطرحوا أسئلة أولاً ثم التصويت أو اختيار جولة أسئلة جديدة
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("❓ بدء جولة أسئلة جديدة", on_click=lambda: (st.session_state.update({'question_pairs': generate_question_pairs(st.session_state.players), 'current_pair_index': 0}), set_page('question_time')))
    with col2:
        st.button("🗳️ خلصنا أسئلة، البدء بالتصويت", on_click=set_page, args=['voting'])
    
    st.markdown("""
    <div class="card" style='margin-top: 20px;'>
        <p style='text-align: center; color: #e74c3c;'>
            إذا لم تعجبك الكلمة، اضغط الزر أدناه لإعادة الأدوار واختيار كلمة جديدة
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("🔄 اختيار كلمة جديدة وإعادة الأدوار", on_click=lambda: (reset_for_new_round(), set_page('select_category')))

def question_time_page():
    st.markdown("<h1>❓ وقت الأسئلة</h1>", unsafe_allow_html=True)
    
    if st.session_state.current_pair_index < len(st.session_state.question_pairs):
        current_pair = st.session_state.question_pairs[st.session_state.current_pair_index]
        
        st.markdown(f"""
        <div class="card">
            <p style='text-align: center; font-size: 20px;'>
                🎮 <span class='bara-player'>{current_pair[0]}</span> 
                يسأل 
                <span class='bara-player'>{current_pair[1]}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.button("👉 السؤال التالي", on_click=lambda: (
                st.session_state.update({'current_pair_index': st.session_state.current_pair_index + 1}),
                set_page('question_time') if st.session_state.current_pair_index < len(st.session_state.question_pairs) else set_page('question_or_vote')
            ))
    else:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.button("🗳️ الانتقال إلى التصويت", on_click=set_page, args=['voting'])

def voting_page():
    st.markdown("<h1>🗳️ التصويت</h1>", unsafe_allow_html=True)
    current_player = st.session_state.players[st.session_state.vote_index]
    
    st.markdown(f"""
    <div class="card">
        <p style='text-align: center; font-size: 20px;'>
            اللاعب <span class='bara-player'>{current_player}</span> يصوت الآن
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    for i, player in enumerate(st.session_state.players):
        if player != current_player:
            with col1 if i % 2 == 0 else col2:
                st.button(f"🎯 تصويت ضد {player}", on_click=lambda p=player: (
                    st.session_state.votes.update({current_player: p}),
                    st.session_state.update({'vote_index': st.session_state.vote_index + 1})
                    if st.session_state.vote_index < len(st.session_state.players) - 1
                    else set_page('voting_results')
                ))

def voting_results_page():
    st.markdown("<h1>📊 نتائج التصويت</h1>", unsafe_allow_html=True)
    bara_al_salfa = st.session_state.bara_al_salfa
    
    st.markdown("""
    <div class="card">
        <h3 style='text-align: center; color: #3498db;'>تفاصيل التصويت</h3>
    """, unsafe_allow_html=True)
    
    for player, voted_for in st.session_state.votes.items():
        st.markdown(f"""
        <p>🎯 <span class='bara-player'>{player}</span> صوت ضد <span class='bara-player'>{voted_for}</span></p>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <p style='margin-top: 20px; text-align: center; font-size: 24px;'>
            برا السالفة هو <span class='bara-player'>{bara_al_salfa}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize round_scores for all players
    for player in st.session_state.players:
        if player not in st.session_state.round_scores:
            st.session_state.round_scores[player] = 0
    
    st.markdown("""
    <div class="card" style='margin-top: 20px;'>
        <h3 style='text-align: center; color: #2ecc71;'>النقاط المكتسبة</h3>
    """, unsafe_allow_html=True)
    
    for player, voted_for in st.session_state.votes.items():
        if voted_for == bara_al_salfa:
            st.session_state.round_scores[player] += 5
            st.markdown(f"""
            <p>🎉 <span class='bara-player'>{player}</span> حصل على <span class='score'>5</span> نقاط لتصويته الصحيح</p>
            """, unsafe_allow_html=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card" style='margin-top: 20px;'>
        <p style='text-align: center; font-size: 20px;'>
            الآن <span class='bara-player'>{bara_al_salfa}</span> سيقوم بتخمين الكلمة السرية للحصول على <span class='score'>10</span> نقاط إضافية
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("🎯 تخمين الكلمة", on_click=set_page, args=['bara_guess'])

def bara_guess_page():
    st.markdown("<h1>🎯 تخمين الكلمة السرية</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card">
        <p style='text-align: center; font-size: 20px;'>
            الآن، دور <span class='bara-player'>{st.session_state.bara_al_salfa}</span> لتخمين الكلمة السرية
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    generate_guess_options()
    
    col1, col2 = st.columns(2)
    for i, word in enumerate(st.session_state.guess_word_options):
        with col1 if i % 2 == 0 else col2:
            st.button(f"🎯 {word}", on_click=lambda w=word: handle_bara_guess(w))

def total_scores_page():
    st.markdown("<h1>🏆 النتائج النهائية</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card">
        <p style='text-align: center; font-size: 24px;'>{st.session_state.guess_result}</p>
        <p style='text-align: center; margin-top: 10px;'>
            الكلمة السرية كانت: <span class='secret-word'>{st.session_state.game_word}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card" style='margin-top: 20px;'>
        <h3 style='text-align: center; color: #3498db;'>نقاط الجولة الحالية</h3>
    """, unsafe_allow_html=True)
    
    for player, score in st.session_state.round_scores.items():
        if player.strip():
            st.markdown(f"""
            <p>🎮 <span class='bara-player'>{player}</span>: <span class='score'>{score}</span> نقطة</p>
            """, unsafe_allow_html=True)
            if player in st.session_state.global_scores:
                st.session_state.global_scores[player] += score
            else:
                st.session_state.global_scores[player] = score
    
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card" style='margin-top: 20px;'>
        <h3 style='text-align: center; color: #2ecc71;'>النقاط الإجمالية</h3>
    """, unsafe_allow_html=True)
    
    # Sort players by score
    sorted_players = sorted(st.session_state.global_scores.items(), key=lambda x: x[1], reverse=True)
    
    for player, score in sorted_players:
        if player.strip():
            st.markdown(f"""
            <p>👑 <span class='bara-player'>{player}</span>: <span class='score'>{score}</span> نقطة</p>
            """, unsafe_allow_html=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔄 جولة جديدة", on_click=lambda: (reset_for_new_round(), set_page('select_category')))
    with col2:
        st.button("🚪 خروج", on_click=lambda: st.stop())

# Page routing with callback functions
def page_router():
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'input_players':
        input_players_page()
    elif st.session_state.page == 'select_category':
        select_category_page()
    elif st.session_state.page == 'show_role':
        show_role_page()
    elif st.session_state.page == 'display_role':
        display_role_page()
    elif st.session_state.page == 'question_or_vote': 
        question_or_vote_page()
    elif st.session_state.page == 'question_time':
        question_time_page()
    elif st.session_state.page == 'voting':
        voting_page()
    elif st.session_state.page == 'voting_results':
        voting_results_page()
    elif st.session_state.page == 'bara_guess':
        bara_guess_page()
    elif st.session_state.page == 'total_scores':
        total_scores_page()

# Run the page router
page_router()