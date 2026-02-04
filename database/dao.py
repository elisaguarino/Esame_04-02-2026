from database.DB_connect import DBConnect

class DAO:

    @staticmethod
    def get_authorship():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor()
        query = """ SELECT * 
                    FROM authorship"""
        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result
#prova