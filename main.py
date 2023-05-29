import sqlite3
import datetime
import os
import time

conn = sqlite3.connect('C:/Users/aeiou/Documents/dbproject/shop.db')
curser = conn.cursor()

# 시작화면
def start():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            print("1. 로그인")
            print("2. 회원가입")
            select = input("번호선택 : ")
            return int(select)
        except Exception as e:
            print("잘못된 번호 입력", str(e))
            time.sleep(1)
            continue

# 메뉴보기
def menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            print("1. 상품 구매하기")
            print("2. 구매내역 보기")
            print("3. 장바구니")
            print("4. 종료하기")
            select = input("번호선택 : ")
            return int(select)
        except Exception as e:
            print("잘못된 번호 입력", str(e))
            time.sleep(1)
            continue

# 아이디 만들기
def create_id():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-----------------------------")
    print("회원가입")
    print("-----------------------------")
    while True:
        try:
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
            print("-----------------------------")
            print("회원가입 완료")
            print("-----------------------------")
            time.sleep(1)
            break
        except Exception as e:
            print("-----------------------------")
            print("이미 존재하는 아이디입니다.", str(e))
            print("-----------------------------")
            time.sleep(1)
            break

# 물품 구매하기
def buy_product(id):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("-----------------------------")
        print("상품 보기")
        print("-----------------------------")
        curser.execute("SELECT * FROM product")
        rows = curser.fetchall()
        for row in rows:
            print("상품번호 : ", row[0])        
            print("이름 : ", row[1])
            print("가격 : ", row[2])
            print("설명 : ", row[3])
            print("-----------------------------")
        print("1. 장바구니에 넣기")
        print("2. 구매하기")
        print("3. 뒤로가기")
        select = input("번호선택 : ")
        
        if select == "1":
            product_id = input("카트에 넣고 싶은 상품번호 입력 : ")
            quantity = input("상품 갯수 입력 : ")
            cart_id = __get_next_id("cart", "cart_id")
            curser.execute("""
                        INSERT INTO cart (cart_id, id, product_id, quantity) VALUES
                        (?, ?, ?, ?)
                        """, (cart_id, id, product_id, quantity))
            conn.commit()
            print("-----------------------------")
            print("장바구니에 상품을 담았습니다.")
            print("-----------------------------")
            time.sleep(1)
            continue
        elif select == "2":
            product_id = input("구매하고 싶은 상품번호 입력 : ")
            quantity = input("상품 갯수 입력 : ")
            order_id = __get_next_id("order_detail", "order_id")
            current_date = datetime.datetime.now()
            formatted_date = current_date.strftime("%y%m%d")
            curser.execute("""
                        INSERT INTO order_detail (order_id, user_id, product_id, quantity, order_date) VALUES
                        (?, ?, ?, ?, ?)
                        """, (order_id, id, product_id, quantity, formatted_date))
            conn.commit()
            print("-----------------------------")
            print("구매완료")
            print("-----------------------------")
            time.sleep(1)
            continue
        elif select == "3":
            print("-----------------------------")
            print("뒤로가기")
            print("-----------------------------")
            time.sleep(1)
            break
        else:
            print("잘못된 번호 입력")
            time.sleep(1)
            menu_start = buy_product(id)
            continue

# 테이블의 고유번호 생성하기
def __get_next_id(table, column):
    curser.execute(f"SELECT MAX({column}) FROM {table}".format(column, table))
    max = curser.fetchone()
    last_order_id = max[0]
    if last_order_id is None:
        return int(1)
    else:      
        next_order_id = last_order_id + 1
        return int(next_order_id)

# 카트에 있는 물품 조회하고 구매하기
def my_cart(id):
    os.system('cls' if os.name == 'nt' else 'clear')
    item_list = []
    print("-----------------------------")
    print("카트에 담은 상품")
    print("-----------------------------")
    curser.execute("""
                   SELECT p.name, c.quantity, p.product_id
                   FROM product as p, cart as c
                   WHERE p.product_id == c.product_id AND c.id == ?
                   """, (id, ))
    rows = curser.fetchall()
    if not rows:
        print("아무 것도 없습니다.")
        print("-----------------------------")
        print("1. 뒤로가기")
        select = input("번호 입력 : ")
        if select == "1":
            time.sleep(1)
            return menu_start
    for row in rows:
        print("상품명 : ", row[0])
        print("갯수 : ", row[1])
        item_list.append((row[2], row[1])) # 상품 고유id와 갯수를 리스트에 저장
        print("-----------------------------")
    print("1. 카트에 담은 물품 구매하기")
    print("2. 뒤로가기")
    select = input("번호선택 : ")
    
    # 카트에 있는 물건 구매하기
    if select == "1":
        for item in item_list:
            product_id = item[0]
            quantity = item[1]
            order_id = __get_next_id("order_detail", "order_id")
            current_date = datetime.datetime.now()
            formatted_date = current_date.strftime("%y%m%d")
            curser.execute("""
                        INSERT INTO order_detail (order_id, user_id, product_id, quantity, order_date) VALUES
                        (?, ?, ?, ?, ?)
                        """, (order_id, id, product_id, quantity, formatted_date))
            conn.commit()
        print("-----------------------------")
        print("장바구니에 있는 품목 구매완료")
        print("-----------------------------")
        curser.execute("""
                       DELETE FROM cart
                       WHERE id == ?
                       """, (id, ))
        conn.commit()
        time.sleep(1)
        return menu_start
    elif select == "2":
        print("-----------------------------")
        print("뒤로가기")
        print("-----------------------------")
        time.sleep(1)
        return menu_start
    else:
        print("잘못된 입력")
        time.sleep(1)
        return my_cart(id)
        
# 구매내역 보기
def my_order(id):
    os.system('cls' if os.name == 'nt' else 'clear')
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
    print("1. 뒤로가기")
    select = input("번호 입력 : ")
    if select == "1":
        print("-----------------------------")
        print("뒤로가기")
        print("-----------------------------")
        time.sleep(1)
        return menu_start

# 로그인 하기
def login():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-----------------------------")
    print("로그인")
    print("-----------------------------")
    id = input("id : ")
    pw = input("pw : ")
    curser.execute("SELECT id FROM user WHERE id = ? AND pw = ?", (id, pw))
    rows = curser.fetchall()
    if len(rows) > 0:
        print("-----------------------------")
        print("로그인 성공")
        print("-----------------------------")
        time.sleep(1)
        return id, 0
    else:
        print("-----------------------------")
        print("로그인 실패")
        print("-----------------------------")
        time.sleep(1)
        return id, 1

# 프로그램 시작
login_result = None

while True:
    user_start = start()
    if user_start == 1:
        id, login_result = login()
    elif user_start == 2:
        create_id()
    else:
        print("잘못된 입력")
        time.sleep(1)
        continue
    if login_result == 0:
        break

# 로그인 성공 후 메뉴작동
if login_result == 0:
    while True:
        menu_start = menu()
        if menu_start == 1:
            buy_product(id)
        elif menu_start == 2:
            my_order(id)
        elif menu_start == 3:
            my_cart(id)
        elif menu_start == 4:
            print("-----------------------------")        
            print("종료")
            print("-----------------------------")
            time.sleep(1)
            break
        else:
            print("-----------------------------")
            print("올바른 번호를 입력해주세요.")
            print("-----------------------------")
            time.sleep(1)
            continue