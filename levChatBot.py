import pandas as pd


class levChatBot:
    def __init__(self, filepath):
        # Q와 A를 ChatbotData.csv 로 부터 로드
        self.questions, self.answers = self.load_data(filepath)        

    def lev_calc_distance(self, a, b):
        '''
        a: 입력한 질문
        b: 로드된 질문 리스트
        '''
        # 교수님 레벤슈타인 거리 사용 코드
        if a == b: return 0 # 같으면 0을 반환
        a_len = len(a) # a 길이
        b_len = len(b) # b 길이
        if a == "": return b_len
        if b == "": return a_len

        matrix = [[] for i in range(a_len+1)] # 리스트 컴프리헨션을 사용하여 1차원 초기화
        for i in range(a_len+1): # 0으로 초기화
            matrix[i] = [0 for j in range(b_len+1)]  # 리스트 컴프리헨션을 사용하여 2차원 초기화
        # 0일 때 초깃값을 설정
        for i in range(a_len+1):
            matrix[i][0] = i
        for j in range(b_len+1):
            matrix[0][j] = j
        
        
        for i in range(1, a_len+1):
            ac = a[i-1]
            
            for j in range(1, b_len+1):
                bc = b[j-1] 
                
                cost = 0 if (ac == bc) else 1 
                # 매트릭스의 각 원소에 대해 각각 비교
                matrix[i][j] = min([
                    matrix[i-1][j] + 1,     
                    matrix[i][j-1] + 1,     
                    matrix[i-1][j-1] + cost 
                ])
                
        return matrix[a_len][b_len]
        
    def load_data(self, filepath):        
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문 리스트
        answers = data['A'].tolist()   # 답변 리스트
        return questions, answers

    def find_best_answer(self, input_sentence):
        # 레벤슈타인 거리 계산
        lev_distances = []
        # 질문에 대한 각 레베슈타인 거리를 계산
        for q in self.questions:
            lev_distances.append(self.lev_calc_distance(input_sentence, q))        

        best_match_index = lev_distances.index(min(lev_distances))
        
        # 거리에 따른 질문을 찾기, 유사한 질문의 인덱스를 함께 출력
        return best_match_index, self.answers[best_match_index]
    
# CSV 파일 경로 지정
filepath = 'ChatbotData.csv'

# 챗봇 인스턴스를 생성
chatbot = levChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    index_lev_dis, response = chatbot.find_best_answer(input_sentence) 
       
    print(f'Chatbot:{response}  [cf) 레베슈타인 질문 인덱스 번호:{index_lev_dis}]') #질문 인덱스와 함께 출력