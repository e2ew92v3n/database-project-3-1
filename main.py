import sqlite3
import datetime

conn = sqlite3.connect('C:/Users/aeiou/Documents/dbproject/shop.db')
curser = conn.cursor()

def start():
    print("1. 로그인")
    print("2. 회원가입")
    select = input("번호선택 : ")
    return int(select)

def menu():
    print("1. 상품 구매하기")
    print("2. 구매내역 보기")
    print("3. 장바구니")
    print("4. 종료하기")
    select = input("번호선택 : ")
    return int(select)

def creat_id():
    print("-----------------------------")
    print("아이디 생성")
    print("-----------------------------")
    id = input("아이디 : ")
    pw = input("비밀번호 : ")
    name = input("이름 : ")
    email = input("이메일 : ")
    phone = input("전화번호 : ")
    adress = input("주소 : ")
    curser.execute("""
                   INSERT INTO user(id, pw, name, email, phone, adress) VALUES
                   (?, ?, ?, ?, ?, ?)
                   """, (id, pw, name, email, phone, adress))
    conn.commit()
    start()
    
def buy_product(id):
    curser.execute("SELECT * FROM product")
    rows = curser.fetchall()
    for row in rows:
        print("상품번호 : ", row[0])        
        print("이름 : ", row[1])
        print("가격 : ", row[2])
        print("설명 : ", row[3])
        print("-----------------------------")
    product_id = input("구매하고 싶은 상품번호 입력 : ")
    quantity = input("상품번호 갯수 입력 : ")
    order_id = __get_next_order_id()
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%y%m%d")
    curser.execute("""
                   INSERT INTO order_detail (order_id, user_id, product_id, quantity, order_date) VALUES
                   (?, ?, ?, ?, ?)
                   """, (order_id, id, product_id, quantity, formatted_date))
    conn.commit()
    print("구매완료")
    print("-----------------------------")
    
def __get_next_order_id():
    curser.execute("SELECT MAX(order_id) FROM order_detail")
    max = curser.fetchone()
    last_order_id = max[0]
    next_order_id = last_order_id + 1
    return int(next_order_id)

def my_order(id):
    print("-----------------------------")
    print("나의 구매내역")
    print("-----------------------------")
    curser.execute("""
                SELECT p.name, o.quantity, o.order_date
                FROM product as p, order_detail as o
                WHERE p.product_id == o.product_id AND o.user_id == ?
                   """, (id, ))
    rows = curser.fetchall()
    for row in rows:
        print("상품명 : ", row[0])        
        print("갯수 : ", row[1])
        print("주문날짜 : ", row[2])
        print("-----------------------------")

def login():
    id = input("id : ")
    pw = input("pw : ")
    curser.execute("SELECT id FROM user WHERE id = ? AND pw = ?", (id, pw))
    rows = curser.fetchall()
    if len(rows) > 0:
        print("-----------------------------")
        print("로그인 성공")
        print("-----------------------------")
        return id, 0
    else:
        print("-----------------------------")
        print("로그인 실패")
        print("-----------------------------")
        return id, 1
    
while True:
    user_start = start()
    if user_start == 1:
        id, login_result = login()
    elif user_start == 2:
        creat_id()
    if login_result == 0:
        break

while True:
    menu_start = menu()    
    if menu_start == 1:
        buy_product(id)
    elif menu_start == 2:
        my_order(id)
    elif menu_start == 3:
        None
    elif menu_start == 4:
        print("-----------------------------")        
        print("종료")
        print("-----------------------------")
        break