import streamlit as st
import random
from categories import categories  

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
    st.title("لعبة براالسالفة")
    st.write("مرحبًا بك في لعبة برا السالفة! ابدأ بتحديد عدد اللاعبين.")
    st.session_state.num_players = st.number_input("أدخل عدد اللاعبين (3-12):", min_value=3, max_value=12, step=1)
    st.button("ابدأ اللعبة", on_click=lambda: (initialize_players(), set_page('input_players')), key='input_players_button')


def input_players_page():
    st.title("أدخل أسماء اللاعبين")
    for i in range(st.session_state.num_players):
        st.session_state.players[i] = st.text_input(f"اسم اللاعب رقم {i+1}:", value=st.session_state.players[i])
    
    # make sure names above are not empty
    if not all(name.strip() for name in st.session_state.players):
        st.warning("من فضلك أدخل أسماء اللاعبين")
        return
    
    st.button("التالي", on_click=set_page, args=['select_category'], key='select_category_button')

def select_category_page():
    st.title("اختر القائمة")
    st.session_state.selected_category = st.selectbox("اختر قائمة الكلمات:", options=list(categories.keys()))
    st.button("تأكيد القائمة", on_click=assign_roles_and_word, key='assign_roles_and_word_button')

def show_role_page():
    st.title("عرض الدور")
    current_player = st.session_state.players[st.session_state.current_player_index]
    st.write(f"أعط الشاشة إلى: {current_player}")
    st.button("عرض الدور", on_click=set_page, args=['display_role'], key='display_role_button')

def display_role_page():
    current_player = st.session_state.players[st.session_state.current_player_index]
    role = st.session_state.roles[current_player]
    st.title("دورك")
    st.write(f"القائمة: **{st.session_state.selected_category}**")
    st.write(f"مرحبا {current_player}، دورك هو: **{role}**")
    if role == 'داخل السالفة':
        st.write(f"الكلمة السرية هي: **{st.session_state.game_word}**")
    else:
        st.write("مهمتك أن توضح للمجموعة أنك تعرف الموضوع بالإجابة بشكل عام.")
    if st.session_state.current_player_index < len(st.session_state.players) - 1:
        st.button("التالي", on_click=lambda: (st.session_state.update({'current_player_index': st.session_state.current_player_index + 1}), set_page('show_role')), key='show_role_button')
    else:
        st.button("التالي", on_click=set_page, args=['question_or_vote'], key='question_or_vote_button')

def question_or_vote_page():
    st.title("ماذا تريد أن تفعل الآن؟ يجب على اللاعبين الآن أن يطرحوا أسئلة اولا و من ثم التصويت او اختيار جولة اسئلة جديدة.")
    st.button("بدء جولة أسئلة جديدة", on_click=lambda: (st.session_state.update({'question_pairs': generate_question_pairs(st.session_state.players), 'current_pair_index': 0}), set_page('question_time')), key='question_time_button')
    st.button("خلصنا اسئلة، البدء بالتصويت", on_click=set_page, args=['voting'], key='voting_button')
    st.title("اذا لم تعجبك الكلمة، اضغط الزر الاسفل لاعادة الادوار واختيار كلمة جديدة من القائمات")
    st.button("اختيار كلمة جديدة و اعادة الادوار", on_click=lambda: (reset_for_new_round(), set_page('select_category')), key='new_round_button')

def question_time_page():
    st.title("وقت الأسئلة")
    
    # Check if there are pairs to display
    if st.session_state.current_pair_index < len(st.session_state.question_pairs):
        current_pair = st.session_state.question_pairs[st.session_state.current_pair_index]
        st.write(f"{current_pair[0]} قم بسؤال {current_pair[1]}")
        st.button(
            "التالي", 
            on_click=lambda: (
                st.session_state.update({'current_pair_index': st.session_state.current_pair_index + 1}), 
                set_page('question_time') if st.session_state.current_pair_index < len(st.session_state.question_pairs) else set_page('question_or_vote')
            ), 
            key='question_or_vote_button'
        )
    else:
        st.button("الانتقال إلى التصويت", on_click=set_page, args=['voting'], key='voting_button')


def voting_page():
    st.title("التصويت")
    current_player = st.session_state.players[st.session_state.vote_index]
    st.write(f"اللاعب **{current_player}** يصوت الآن.")

    for player in st.session_state.players:
        if player != current_player:
            st.button(f"تصويت ضد {player}", on_click=lambda p=player: (st.session_state.votes.update({current_player: p}), st.session_state.update({'vote_index': st.session_state.vote_index + 1}) if st.session_state.vote_index < len(st.session_state.players) - 1 else set_page('voting_results')), key=player)

def voting_results_page():
    st.title("نتائج التصويت")
    bara_al_salfa = st.session_state.bara_al_salfa

    # Display the results but not in table format 
    for player, voted_for in st.session_state.votes.items():
        st.write(f"- {player} صوت ضد {voted_for}")

    st.write(f"برا السالفة هو **{bara_al_salfa}**")
    
    # Initialize round_scores for all players
    for player in st.session_state.players:
        if player not in st.session_state.round_scores:
            st.session_state.round_scores[player] = 0
    
    for player, voted_for in st.session_state.votes.items():
        if voted_for == bara_al_salfa:
            st.session_state.round_scores[player] += 5
            st.write(f"{player} حصل على 5 نقاط لتصويته الصحيح")
    
    st.write(f"الأن **{bara_al_salfa}** سيقوم بتخمين الكلمة السرية وامكانية الحصول على 10 نقاط.")
    
    st.button("التالي", on_click=set_page, args=['bara_guess'], key='bara_guess_button')

def bara_guess_page():
    st.title("تخمين الكلمة السرية")
    st.write(f"الآن، دور **{st.session_state.bara_al_salfa}** لتخمين الكلمة السرية.")
    generate_guess_options()
    
    for word in st.session_state.guess_word_options:
        st.button(word, on_click=lambda w=word: handle_bara_guess(w), key=word)

def total_scores_page():
    st.title("الكلمة السرية و النقاط الكلية")
    
    # Display the result of the "برة السالفة" player's guess
    st.write(st.session_state.guess_result)  # This should already be set by the handle_bara_guess function
    st.write(f"الكلمة السرية كانت: **{st.session_state.game_word}**")
    
    # Display round scores
    st.write("**النقاط الكلية للجولة الحالية:**")
    for player, score in st.session_state.round_scores.items():
        if player.strip():
            st.write(f"- {player}: {score} نقطة")
            if player in st.session_state.global_scores:
                st.session_state.global_scores[player] += score
            else:
                st.session_state.global_scores[player] = score
    
    # Display total scores for all rounds
    st.write("**النقاط الكلية لجميع الجولات:**")
    for player, score in st.session_state.global_scores.items():
        if player.strip():
            st.write(f"- {player}: {score} نقطة")
    
    # Provide options to start a new round or quit the game
    st.button("لعب جولة أخرى واختيار نفس القائمة او قائمة جديدة", on_click=lambda: (reset_for_new_round(), set_page('select_category')), key='new_round_button')
    st.button("الخروج", on_click=lambda: st.stop(), key='quit_button')


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