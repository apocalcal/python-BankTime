import random

MAX_QUEUE_SIZE = 100

# 고객 정보를 담는 클래스
class Element:
    def __init__(self, id, arrival_time, service_time):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time

# 큐의 타입을 정의하는 클래스, 원형 리스트를 사용하여 큐를 생성
class QueueType:
    def __init__(self):
        self.data = [None] * MAX_QUEUE_SIZE
        self.front = self.rear = 0

# 에러 메시지를 출력하고 프로그램을 종료하는 함수
def error(message):
    print(message)
    exit(1)

# 큐 초기화 함수
def init_queue(q):
    q.front = q.rear = 0

# 큐가 비어 있는지 확인하는 함수
def is_empty(q):
    return q.front == q.rear

# 큐가 꽉 차 있는지 확인하는 함수
def is_full(q):
    return (q.rear + 1) % MAX_QUEUE_SIZE == q.front

# 큐에 요소(고객)를 추가하는 함수
def enqueue(q, item):
    if is_full(q):
        print("포화상태입니다. 새로운 고객을 추가하지 않습니다.")
    else:
        q.rear = (q.rear + 1) % MAX_QUEUE_SIZE
        q.data[q.rear] = item

# 큐에서 요소(고객)를 제거하는 함수
def dequeue(q):
    if is_empty(q):
        error("공백상태입니다.")
    else:
        q.front = (q.front + 1) % MAX_QUEUE_SIZE
        return q.data[q.front]

def main():
    minutes = int(input("몇 분까지의 시뮬레이션을 보시겠습니까? : "))
    
    total_wait = 0
    total_customers = 0
    ab_customers = 0
    a_service_time = 0
    b_service_time = 0
    a_service_customer = 0
    b_service_customer = 0
    a_counter = True
    b_counter = True
    q = QueueType()
    init_queue(q)
    random.seed()
    client = int(input("고객이 올 확률을 입력하세요 (0~9, 10%면 1로 입력) : ")) #사용자가 직접 고객이 올 확률을 입력할 수 있음

    # A, B 창구가 닫혀 있는 총 시간
    total_a_closed_time = 0
    total_b_closed_time = 0

    for clock in range(minutes + 1):
        print("\n====================================현재시각=%d분======================================" % clock)
        print("<현재> A창구 출입여부 %d, B창구 출입여부 %d (0: 닫힘, 1: 열림)" % (a_counter, b_counter))
        # 사용자가 설정한 확률에 따라 고객이 도착하는지 확인
        if random.randint(0, 9) < client:
            # 새로운 고객 생성 및 큐에 추가
            customer = Element(total_customers, clock, random.randint(1, 20))
            total_customers += 1
            enqueue(q, customer)
            print("고객 %d이 %d분에 들어옵니다. 고객 업무처리시간=%d" % (customer.id, customer.arrival_time, customer.service_time))
        #A 창구에서 업무 처리 중인 경우
        if a_service_time > 0:
            print("고객 %d이 A창구에서 업무처리중입니다." % a_service_customer)
            a_service_time -= 1
            # A 창구가 업무 처리를 마친 경우
            if a_service_time == 0:
                print("(A창구가 %d분부터 열립니다.)" % (clock + 1))
                a_counter = True
        elif a_counter:
            # A 창구가 비어 있고 대기 중인 고객이 있다면
            if not is_empty(q):
                 # 대기 중인 고객을 A 창구에서 업무 처리 시작
                customer = dequeue(q)
                a_service_customer = customer.id
                a_service_time = customer.service_time
                wait_time = clock - customer.arrival_time
                print(f"고객 {customer.id}이 {clock}분에 A창구에서 업무를 시작합니다. 대기시간은 {wait_time}분이었습니다.")
                a_counter = False
                total_wait += wait_time
                ab_customers += 1
        # B창구에서 업무처리 중인 경우(A창구와 구성 동일함)
        if b_service_time > 0:
            print("고객 %d이 B창구에서 업무처리중입니다." % b_service_customer)
            b_service_time -= 1

            if b_service_time == 0:
                print("(B창구가 %d분부터 열립니다.)" % (clock + 1))
                b_counter = True
        elif b_counter:
            if not is_empty(q):
                customer = dequeue(q)
                b_service_customer = customer.id
                b_service_time = customer.service_time
                wait_time = clock - customer.arrival_time
                print(f"고객 {customer.id}이 {clock}분에 B창구에서 업무를 시작합니다. 대기시간은 {wait_time}분이었습니다.")
                b_counter = False
                total_wait += wait_time
                ab_customers += 1

        # A, B 창구의 닫힌 시간을 누적
        total_a_closed_time += 1 if not a_counter else 0
        total_b_closed_time += 1 if not b_counter else 0

    # 평균 대기 시간 계산
    if total_customers > 0:
        average_wait_time = total_wait / ab_customers
    else:
        average_wait_time = 0

    print("\n최종 결과:")
    print("전체 대기 시간 = %d분" % total_wait)
    print("평균 대기 시간 = %.2f분" % average_wait_time)
    print("업무 완료 고객 = %d명" % ab_customers)
    print("시뮬레이션이 종료되었습니다.")

if __name__ == "__main__":
    main()
