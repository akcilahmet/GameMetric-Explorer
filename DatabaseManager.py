import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as er:
            print(f"Database connect: {er}")


    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def insert_category(self, category_name):
        try:
            self.cursor.execute('INSERT INTO categories (category_name) VALUES (%s)', (category_name,))
            self.connection.commit()
        except mysql.connector.Error as er:
            print(f"Database insert_category: {er}")


    def insert_game_metric(self, game_name, category_name, update_date, downloads, revenue, ratings):
        try:
            # Mevcut veriyi kontrol et
            self.cursor.execute('SELECT * FROM dailygamemetrics WHERE game_name = %s AND update_date = %s',
                                (game_name, update_date))
            existing_data =self.cursor.fetchone()

            if not existing_data:
                self.cursor.execute(
                    'INSERT INTO dailygamemetrics (game_name,category_name,update_date,downloads,revenue,ratings) VALUES (%s,%s,%s,%s,%s,%s)',
                    (game_name, category_name, update_date, downloads, revenue, ratings))
                self.connection.commit()
            else:
                print("This data already exists")
        except mysql.connector.Error as er:
            print(f"Database inster_gamemetric: {er}")


    def update_game_metric(self, game_name, update_date, new_downloads, new_revenue, new_ratingss):
        try:
            self.cursor.execute(
                'UPDATE dailygamemetrics SET downloads=%s ,revenue=%s, ratings=%s WHERE game_name=%s AND update_date=%s',
                (new_downloads, new_revenue, new_ratingss, game_name, update_date))
            self.connection.commit()
        except mysql.connector.Error as er:
            print(f"Database update_game_metric: {er}")


    def delete_game_metric(self, game_name, update_date):
        try:
            self.cursor.execute('DELETE FROM dailygamemetrics WHERE  game_name=%s AND update_date=%s',
                                (game_name, update_date))
            self.connection.commit()
        except mysql.connector.Error as er:
            print(f"Database delete_game_metric: {er}")

    def check_connection(self):
        return self.connection.is_connected()

