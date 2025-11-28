# database.py - ПОЛНЫЙ ИСПРАВЛЕННЫЙ КОД
import pymysql
from PyQt6.QtWidgets import QMessageBox
import sys


class Database:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='shoes',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Успешное подключение к базе данных")
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            QMessageBox.critical(None, "Ошибка", f"Не удалось подключиться к базе данных: {e}")
            sys.exit(1)

    def check_user(self, login, password):
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM user WHERE login = %s AND password = %s"
                cursor.execute(sql, (login, password))
                user = cursor.fetchone()
                
                print(f"Поиск пользователя: login={login}, password={password}")
                if user:
                    print(f"Найден пользователь: {user}")
                    print(f"Роль пользователя: {user.get('role', 'Не указана')}")
                else:
                    print("Пользователь не найден")
                
                return user
        except Exception as e:
            print(f"Ошибка при проверке пользователя: {e}")
            return None

    def get_products(self, filters=None):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                SELECT p.*, pt.name as type_name, c.name as category_name, 
                       pr.name as producer_name, s.name as supplier_name
                FROM product p
                LEFT JOIN product_type pt ON p.id_type = pt.id
                LEFT JOIN category c ON p.id_category = c.id
                LEFT JOIN producer pr ON p.id_producer = pr.id
                LEFT JOIN supplier s ON p.id_supplier = s.id
                WHERE 1=1
                """
                params = []

                if filters:
                    if filters.get('search'):
                        search_term = f'%{filters["search"]}%'
                        sql += """
                        AND (p.article LIKE %s OR p.description LIKE %s 
                             OR pt.name LIKE %s OR c.name LIKE %s 
                             OR pr.name LIKE %s OR s.name LIKE %s)
                        """
                        params.extend([search_term] * 6)
                    
                    if filters.get('supplier'):
                        sql += " AND p.id_supplier = %s"
                        params.append(filters['supplier'])
                    
                    if filters.get('type'):
                        sql += " AND p.id_type = %s"
                        params.append(filters['type'])
                    if filters.get('category'):
                        sql += " AND p.id_category = %s"
                        params.append(filters['category'])
                    if filters.get('producer'):
                        sql += " AND p.id_producer = %s"
                        params.append(filters['producer'])
                    
                    if filters.get('sort') == 'amount_asc':
                        sql += " ORDER BY p.amount ASC"
                    elif filters.get('sort') == 'amount_desc':
                        sql += " ORDER BY p.amount DESC"

                cursor.execute(sql, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении товаров: {e}")
            return []

    def get_orders(self):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                SELECT o.*, s.name as status_name, u.name as user_name, 
                       u.surname as user_surname, pvz.city as pvz_city,
                       pvz.street as pvz_street
                FROM `order` o
                LEFT JOIN status s ON o.id_status = s.id
                LEFT JOIN user u ON o.id_user = u.id
                LEFT JOIN pvz ON o.id_pvz = pvz.id
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении заказов: {e}")
            return []

    def get_product_types(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM product_type")
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении типов товаров: {e}")
            return []

    def get_categories(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM category")
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении категорий: {e}")
            return []

    def get_producers(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM producer")
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении производителей: {e}")
            return []

    def get_pvz_list(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM pvz")
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении ПВЗ: {e}")
            return []

    def get_statuses(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM status")
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении статусов: {e}")
            return []

    def get_suppliers(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM supplier")
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении поставщиков: {e}")
            return []

    def add_product(self, product_data):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                INSERT INTO product (article, description, id_type, id_category, 
                                   id_producer, id_supplier, price, discount, amount, unit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'шт.')
                """
                cursor.execute(sql, (
                    product_data['article'], product_data['description'],
                    product_data['id_type'], product_data['id_category'],
                    product_data['id_producer'], product_data['id_supplier'],
                    product_data['price'], product_data['discount'], product_data['amount']
                ))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при добавлении товара: {e}")
            return False

    def update_product(self, product_id, product_data):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                UPDATE product 
                SET article=%s, description=%s, id_type=%s, id_category=%s,
                    id_producer=%s, id_supplier=%s, price=%s, discount=%s, amount=%s
                WHERE id=%s
                """
                cursor.execute(sql, (
                    product_data['article'], product_data['description'],
                    product_data['id_type'], product_data['id_category'],
                    product_data['id_producer'], product_data['id_supplier'],
                    product_data['price'], product_data['discount'], product_data['amount'],
                    product_id
                ))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при обновлении товара: {e}")
            return False

    def delete_product(self, product_id):
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM product WHERE id=%s"
                cursor.execute(sql, (product_id,))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при удалении товара: {e}")
            return False

    def add_order(self, order_data):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                INSERT INTO `order` (identificator_code, date_order, date_delivery, id_pvz, id_status, id_user)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    order_data['identificator_code'], order_data['date_order'],
                    order_data['date_delivery'], order_data['id_pvz'],
                    order_data['id_status'], order_data['id_user']
                ))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при добавлении заказа: {e}")
            return False

    def update_order(self, order_id, order_data):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                UPDATE `order` 
                SET identificator_code=%s, date_order=%s, date_delivery=%s, id_pvz=%s, id_status=%s, id_user=%s
                WHERE id=%s
                """
                cursor.execute(sql, (
                    order_data['identificator_code'], order_data['date_order'],
                    order_data['date_delivery'], order_data['id_pvz'],
                    order_data['id_status'], order_data['id_user'],
                    order_id
                ))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при обновлении заказа: {e}")
            return False

    def delete_order(self, order_id):
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM `order` WHERE id=%s"
                cursor.execute(sql, (order_id,))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при удалении заказа: {e}")
            return False