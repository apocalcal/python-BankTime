import heapq
import random

MAX_QUEUE_SIZE = 100

class Element:
    def __init__(self, id, arrival_time, service_time, priority):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

class PriorityQueueType:
    def __init__(self):
        self.data = []
    
    def is_empty(self):
        return not bool(self.data)

    def enqueue(self, item):
        heapq.heappush(self.data, item)

    def dequeue(self):
        if not self.is_empty():
            return heapq.heappop(self.data)
        else:
            error("Priority Queue is empty.")

def error(message):
    print(message)
    exit(1)

def init_queue(q):
    q.data = []

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
    q = PriorityQueueType()
    random.seed()
    client = int(input("고객이 올 확률을 입력하세요 (0~9, 10%면 1로 입력) : "))

    # A, B 창구가 닫혀 있는 총 시간
    total_a_closed_time = 0
    total_b_closed_time = 0

    for clock in range(minutes + 1):
        print("\n====================================현재시각=%d분======================================" % clock)
        print("<현재> A창구 출입여부 %d, B창구 출입여부 %d (0: 닫힘, 1: 열림)" % (a_counter, b_counter))

        if random.randint(0, 9) < client:
            priority = random.randint(1, 5)
            customer = Element(total_customers, clock, random.randint(1, 20), priority)
            total_customers += 1
            q.enqueue(customer)
            print(f"고객 {customer.id}이 {clock}분에 우선순위 {customer.priority}로 들어옵니다. 고객 업무처리시간={customer.service_time}")

        if a_service_time > 0:
            print("고객 %d이 A창구에서 업무처리중입니다." % a_service_customer)
            a_service_time -= 1
           

            if a_service_time == 0:
                print("(A창구가 %d분부터 열립니다.)" % (clock + 1))
                a_counter = True
        elif a_counter:
            if not q.is_empty():
                customer = q.dequeue()
                a_service_customer = customer.id
                a_service_time = customer.service_time
                wait_time = clock - customer.arrival_time
                print(f"고객 {customer.id}이 {clock}분에 A창구에서 업무를 시작합니다. 대기시간은 {wait_time}분이었습니다.")
                a_counter = False
                total_wait += wait_time
                ab_customers += 1

        if b_service_time > 0:
            print("고객 %d이 B창구에서 업무처리중입니다." % b_service_customer)
            b_service_time -= 1
            

            if b_service_time == 0:
                print("(B창구가 %d분부터 열립니다.)" % (clock + 1))
                b_counter = True
        elif b_counter:
            if not q.is_empty():
                customer = q.dequeue()
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
