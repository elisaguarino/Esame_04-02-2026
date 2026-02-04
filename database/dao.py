from database.DB_connect import DBConnect
from model.artista import Artista
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

    @staticmethod
    def get_all_artisti():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from artists a """
        cursor.execute(query)

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_ruoli():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select distinct a.role as ruolo
                    from authorship a"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["ruolo"])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_artisti_ruoli(ruolo):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.artist_id 
                    from authorship a 
                    where a.`role` = %s"""
        cursor.execute(query, (ruolo,))

        for row in cursor:
            result.append(row["artist_id"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_edge(ruolo):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select a.artist_id ,COUNT(distinct o.object_id ) as peso
                    from authorship a ,objects o 
                    where o.object_id =a.object_id 
                    and o.object_id in (select o.object_id 
                                        from objects o 
                                        where curator_approved =1)
                    and a.`role` = %s
                    group by a.artist_id """
        cursor.execute(query,(ruolo,))


        for row in cursor:
            result.append((row["artist_id"], row["peso"]))

        cursor.close()
        conn.close()
        return result