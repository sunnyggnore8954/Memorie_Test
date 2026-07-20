from datetime import datetime
import random
import matplotlib.pyplot as plt
import os
import time
import openai


# 간병 챗봇 코드
openai.api_key = 'sk-acYvDPSvm5B_3E8B3gpCKhLcH3Fs2XufMaM8y3Zan0T3BlbkFJrqRRrbRSEfrsbnJ-WjGqDhmCLkwVwRkeTESZLmeTAA'

#챗봇 역할 정의
messages_history = [{"role": "system", "content": "간병 챗봇은 간병 팁을 제공하거나, 심리 상담을 진행하는 챗봇입니다. 사용자로부터 간병에 관한 질문, 고민등의 키워드를 입력받으면 그에 맞게 대답해주세요. \
                만약 치매 간병, 심리 상담 이외에 질문을 한다면 답변을 하지마세요. 친절하고, 상냥하고, 공감을 많이 해주세요. 사람같은 말투로 답변해주세요."}]

def chatbot_response(prompt):
    messages_history.append({"role": "user", "content": prompt})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages_history,
            max_tokens=2000,
            temperature=1
        )

        # 챗봇 응답 처리
        answer = response['choices'][0]['message']['content'].strip()
        messages_history.append({"role": "assistant", "content": answer})
        return answer

    #예외 처리
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

def chatbot_menu():
    print("안녕하세요? 간병 챗봇입니다 질문을 입력해주세요. *종료하시려면 '종료'를 입력하세요.*")

#대화 반복
    while True:
        prompt = input("사용자: ")

        answer = chatbot_response(prompt)
        print(f"간병 챗봇: {answer}")

        if prompt == '종료':
            print("간병 챗봇을 종료합니다. 메인 메뉴로 돌아갑니다.")
            break

#치매 환자 상태 검사 코드
def test1(name, location, birthday):
    nowtime = datetime.now()
    korweekend = {
        "Monday": "월요일",
        "Tuesday": "화요일",
        "Wednesday": "수요일",
        "Thursday": "목요일",
        "Friday": "금요일",
        "Saturday": "토요일",
        "Sunday": "일요일"
    }

    weekend = korweekend[nowtime.strftime("%A")]
    hour = nowtime.strftime("%I시")
    month = nowtime.strftime("%m월")
    year = nowtime.year
    season = ["봄", "여름", "가을", "겨울"][(nowtime.month % 12) // 3]
    MMSE_K_test_word_list = ["사과", "책", "꽃", "나무", "컴퓨터", "고양이", "우유", "가방", "전화기", "시계"]
    MMSE_K_test_question_10words = random.sample(MMSE_K_test_word_list, 3)

    #MMSE-K 검사 항목
    MMSE_K_test_questions = [
        "오늘이 무슨 요일인가요?",
        "지금 몇 시인가요?",
        "당신의 이름은 무엇인가요?",
        "지금 당신의 거주지역은 어디인가요?",
        "당신의 생년월일은 언제인가요?",
        "올해가 몇 년도인가요?",
        "오늘이 몇 월인가요?",
        "오늘의 계절은 무엇인가요?",
        "100에서 7을 뺀 값을 말해주세요",
        "기억해야 할 세 가지 물건을 입력해주세요: "
    ]

    answers = [
        weekend,
        hour,
        name,
        location,
        birthday,
        str(year),
        month,
        season
    ]

    #MMSE-k 검사 시작
    print("\nMMSE-K 검사를 시작합니다.")
    print(f"기억해야 할 단어들: {MMSE_K_test_question_10words}")

    MMSE_k_test_score = 0
    for turn, question in enumerate(MMSE_K_test_questions):
        MMSE_K_test_user_answer = input(f"MMSE-K 질문 {turn + 1}: {question}\n")

        if turn == 8:  
            MMSE_K_question_9_answer = "93"

            if MMSE_K_test_user_answer == MMSE_K_question_9_answer:
                MMSE_k_test_score += 1

        elif turn == 9:
            MMSE_K_test_user_answer = MMSE_K_test_user_answer.split(",")
            MMSE_K_test_user_answer = set(MMSE_K_test_user_answer)
            MMSE_K_test_question_10words = set(MMSE_K_test_question_10words)
            question10 = len(MMSE_K_test_user_answer & MMSE_K_test_question_10words)

            if question10 == 3:
                MMSE_k_test_score += 1

        else:
            if MMSE_K_test_user_answer == answers[turn]:
                MMSE_k_test_score += 1
                
    #MMSE-k 검사 점수
    print(f"MMSE-K 점수: {MMSE_k_test_score}/10")
    return MMSE_k_test_score

#RAVLT 검사 항목
def test2():
    RAVLT_test_list = ["바나나", "책", "시계", "연필", "모자", "자동차", "커피", "열쇠", "전화기", "가방"]
    RAVLT_test_word = random.sample(RAVLT_test_list, 5)
    
    #RAVLT 검사 시작
    print("\nRAVLT 검사를 시작합니다.")
    print(f"다음 단어들을 기억해주세요 (5초 동안 표시됩니다): {RAVLT_test_word}")
    time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    RAVLT_test_user_answer = input("기억나는 단어들을 입력하세요 (쉼표로 구분): ").split(",")
    RAVLT_test_score = 0

    for word in RAVLT_test_user_answer:
        if word in RAVLT_test_word:
            RAVLT_test_score += 1

    print(f"RAVLT 점수: {RAVLT_test_score}/5")
    return RAVLT_test_score

def alzheimer_test():
    name = input("이름을 입력하세요: ")
    location = input("거주지를 입력하세요: ")
    birthday = input("생년월일을 입력하세요 (예: 1990-01-01): ")

    mmse_k_score = test1(name, location, birthday)
    ravlt_score = test2()
    total = mmse_k_score + ravlt_score

    graphgroup = ["MMSE-K", "RAVLT", "Total"]
    graphscore = [mmse_k_score, ravlt_score, total]

    print(f"총 점수: {total}/15")
    plt.bar(graphscore, graphgroup, color=["red", "blue", "green"])
    plt.title("alzheimer test score")
    plt.ylabel("Score")
    plt.ylim(0, 15)
    plt.show()

#치매 환자 상태 검사 & 간병 챗봇 중 선택
def select():
    while True:
        print("\n[메인 메뉴]")
        print("1. 치매 환자 상태 검사")
        print("2. 간병 챗봇")
        print("3. 종료")
        choice = input("선택하세요 (1/2/3): ")

        if choice == '1':
            alzheimer_test()

        elif choice == '2':
            chatbot_menu()

        elif choice == '3':
            print("프로그램을 종료합니다.")
            break

        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    select()
