from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling
import json
import os

UPLOAD_FOLDER = "/uploads/"


class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def login(self, email, password):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `user` WHERE email = %s AND password = %s"
        cursor.execute(sql, [email, password])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            response['status'] = 'success'
            response['message'] = 'Login Success!'
            result['id_user'] = row[0][0]
            result['status_code'] = 200
        else:
            response['status'] = 'error'
            response['message'] = 'Your email and Password are Not Defined!'
            result['status_code'] = 404

        cursor.close()
        result['response'] = response
        return result

    def register(self, nrp, nama, email, password):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `user` WHERE email = %s"
        cursor.execute(sql, [email])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 0:
            sql = "INSERT INTO `user` (`id`, `nrp`, `nama`, `email`, `password`, `id_role`) VALUES (NULL, %s, %s, %s, %s, 1)"
            cursor.execute(sql, [nrp, nama, email, password])
            self.connection.commit()

            response['status'] = 'success'
            response['message'] = 'Register Success!'
            result['status_code'] = 200
        else:
            response['status'] = 'error'
            response['message'] = 'Your email is already registered!'
            result['status_code'] = 404

        cursor.close()
        result['response'] = response
        return result

    def upload_files(self, filename, title, abstract, id_user):
        result = {}
        cursor = self.connection.cursor()
        sql = "INSERT INTO `files`(`id`, `filename`, `judul`, `abstrak`,  `access_user`) VALUES (NULL, %s, %s, %s, %s)"
        cursor.execute(sql, [filename, title, abstract, int(id_user)])
        self.connection.commit()

        result['status_code'] = 200
        result['status'] = "success"
        cursor.close()
        return result

    def download_file(self, file_id, id_user):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `files` WHERE id = %s AND access_user = %s"
        cursor.execute(sql, [int(file_id), int(id_user)])
        row = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count == 1:
            response['status'] = 'success'
            result['filename'] = row[0][1]
            result['status_code'] = 200
        else:
            response['status'] = 'error'
            response['message'] = 'Paper not found!'
            result['status_code'] = 404

        cursor.close()
        result['response'] = response
        return result

    def view_file(self, id_user):
        result = {}
        response = {}
        cursor = self.connection.cursor()
        sql = "SELECT id_role FROM user WHERE id = %s"
        cursor.execute(sql, [int(id_user)])
        row = cursor.fetchone()

        sql2 = ''
        if row[0] == 2:
            sql2 += "SELECT * FROM `files`"
            cursor.execute(sql2)
        else:
            sql2 += "SELECT * FROM `files` f WHERE access_user = %s "
            cursor.execute(sql2, [int(id_user)])

        row2 = cursor.fetchall()
        row_count = cursor.rowcount

        if row_count > 0:
            result['status_code'] = 200
            response['status'] = "success"
            response['paper'] = []

            if row[0] == 2:
                cursor.execute(sql2)
            else:
                cursor.execute(sql2, [int(id_user)])

            for row in cursor.fetchall():
                response['paper'].append(
                    {"id_paper": row[0], "filename": row[1], "title": row[2], "abstract": row[3]})
        else:
            result['status_code'] = 404
            response['status'] = "error"
            response['message'] = 'There are still no paper'

        cursor.close()
        result['response'] = response
        return result


class DatabaseProvider(DependencyProvider):

    connection_pool = None

    def setup(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=32,
                pool_reset_session=True,
                host='127.0.0.1',
                database='soa_research_paper',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
