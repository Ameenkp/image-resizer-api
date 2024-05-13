import psycopg2


class Database:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(host=host, dbname=database, user=user, password=password)
        self.cursor = self.conn.cursor()

    def store_image(self, depth, image_data):
        # Implement DB-specific logic for storing image data (e.g., BLOB)
        # Replace with appropriate logic for your chosen database
        sql = "INSERT INTO images (depth, image_data) VALUES (%s, %s)"
        self.cursor.execute(sql, (depth, psycopg2.Binary(image_data.tobytes())))
        self.conn.commit()

    def get_images_by_depth(self, depth_min, depth_max):
        sql = "SELECT image_data FROM images WHERE depth BETWEEN %s AND %s"
        self.cursor.execute(sql, (depth_min, depth_max))
        return [row[0] for row in self.cursor.fetchall()]

    def close(self):
        self.cursor.close()
        self.conn.close()
