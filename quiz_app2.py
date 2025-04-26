import streamlit as st
import random
import math

# ページタイトル
st.title("数学問題アプリ")

# セッションステート初期化
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'num_questions' not in st.session_state:
    st.session_state.num_questions = 10
if 'last_genre' not in st.session_state:
    st.session_state.last_genre = ""

# ジャンル選択
genre = st.sidebar.selectbox("出題ジャンルを選んでください", (
    "3元一次方程式", "たすき掛け因数分解", "虚数計算", "集合", "展開", "二次方程式", "有効数字"
))

# 出題数選択
num_questions = st.sidebar.slider("問題数を選んでください", 5, 30, 10)

# ジャンルか問題数が変わったら問題を再生成
if genre != st.session_state.last_genre or num_questions != st.session_state.num_questions:
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.user_answers = []
    st.session_state.last_genre = genre
    st.session_state.num_questions = num_questions

# 問題作成関数
def generate_linear_equation():
    a, b, c, d, e, f, g, h, i, j, k, l = [random.randint(1, 9) for _ in range(12)]
    D = a*(f*k - g*j) - b*(e*k - g*i) + c*(e*j - f*i)
    if D == 0:
        return generate_linear_equation()
    Dx = d*(f*k - g*j) - b*(h*k - g*l) + c*(h*j - f*l)
    Dy = a*(h*k - g*l) - d*(e*k - g*i) + c*(e*l - h*i)
    Dz = a*(f*l - h*j) - b*(e*l - h*i) + d*(e*j - f*i)
    x = round(Dx / D, 2)
    y = round(Dy / D, 2)
    z = round(Dz / D, 2)
    question = f"{a}x+{b}y+{c}z={d}, {e}x+{f}y+{g}z={h}, {i}x+{j}y+{k}z={l}"
    answer = f"{x},{y},{z}"
    return question, answer

def generate_factorization():
    a, b, c, d = [random.randint(1, 9) for _ in range(4)]
    question = f"{a * c}x²+{(a*d + b*c)}x+{b*d}"
    answer = f"({a}x+{b})({c}x+{d})"
    return question, answer

def generate_imaginary():
    a, b = random.randint(1, 10), random.randint(1, 10)
    question = f"{a}i × {b}i"
    answer = f"{-a*b}"
    return question, answer

def generate_set():
    A = set(random.sample(range(1, 11), 5))
    B = set(random.sample(range(1, 11), 5))
    question = f"A={A}, B={B}, A∩B"
    answer = f"{A&B}"
    return question, answer

def generate_expand():
    a, b, c = random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)
    question = f"({a}x+{b})({c}x+{b})"
    answer = f"{a*c}x²+{(a*b+c*b)}x+{b*b}"
    return question, answer

def generate_quadratic():
    a, b, c = random.randint(1, 5), random.randint(1, 10), random.randint(1, 10)
    D = b**2 - 4*a*c
    if D < 0:
        return generate_quadratic()
    x1 = round((-b + math.sqrt(D)) / (2*a), 2)
    x2 = round((-b - math.sqrt(D)) / (2*a), 2)
    question = f"{a}x²+{b}x+{c}=0"
    answer = f"{x1},{x2}"
    return question, answer

def generate_significant_figures():
    num = round(random.uniform(10, 1000), 3)
    question = f"{num} を有効数字2桁で表せ"
    answer = f"{round(num, -int(math.floor(math.log10(abs(num))))+1)}"
    return question, answer

# 初回のみ問題生成
if not st.session_state.questions:
    for _ in range(num_questions):
        if genre == "3元一次方程式":
            q, a = generate_linear_equation()
        elif genre == "たすき掛け因数分解":
            q, a = generate_factorization()
        elif genre == "虚数計算":
            q, a = generate_imaginary()
        elif genre == "集合":
            q, a = generate_set()
        elif genre == "展開":
            q, a = generate_expand()
        elif genre == "二次方程式":
            q, a = generate_quadratic()
        elif genre == "有効数字":
            q, a = generate_significant_figures()
        st.session_state.questions.append(q)
        st.session_state.answers.append(a)

# 問題表示
st.subheader(f"{genre}の問題")
for i in range(num_questions):
    st.write(f"問題{i+1}: {st.session_state.questions[i]}")
    ans = st.text_input(f"答え{i+1}", key=f"answer_{i}")
    if len(st.session_state.user_answers) < num_questions:
        st.session_state.user_answers.append(ans)
    else:
        st.session_state.user_answers[i] = ans

# 採点ボタン
if st.button("採点する"):
    score = 0
    correct_count = 0
    mistakes = []

    st.write("採点結果：")
    for i in range(num_questions):
        user_answer = st.session_state.user_answers[i].replace(" ", "")
        correct_answer = str(st.session_state.answers[i]).replace(" ", "")
        if user_answer == correct_answer:
            st.write(f"問題{i+1}: 正解！")
            score += 4
            correct_count += 1
        else:
            st.write(f"問題{i+1}: ❌ 不正解。正解は {st.session_state.answers[i]}")
            mistakes.append(f"問題{i+1}: あなたの答え {user_answer} → 正解 {st.session_state.answers[i]}")

    st.write(f"合計得点: {score}点（{num_questions*4}点満点）")
    st.write(f"正答数: {correct_count} / {num_questions}")
    st.write(f"正答率: {round(correct_count/num_questions*100, 1)}%")

    if mistakes:
        st.subheader("間違えた問題と解説")
        for m in mistakes:
            st.write(m)
