from nameko.rpc import rpc
from dependencies import database, session


class userService:

    name = 'user_service'
    database = database.DatabaseProvider()

    @rpc
    def login(self, email, password):
        user = self.database.login(email, password)
        return user

    @rpc
    def register(self, nrp, nama, email, password):
        user = self.database.register(nrp, nama, email, password)
        return user


class storageService:

    name = 'storage_service'
    database = database.DatabaseProvider()

    @rpc
    def upload_files(self, filename, title, abstract, id_user):
        news = self.database.upload_files(filename, title, abstract, id_user)
        return news

    @rpc
    def download_file(self, file_id, id_user):
        news = self.database.download_file(file_id, id_user)
        return news

    @rpc
    def view_file(self, id_user):
        news = self.database.view_file(id_user)
        return news


class SessionService:

    name = 'session_service'
    session_provider = session.SessionProvider()

    @rpc
    def set_session_data(self, username):
        session = self.session_provider.set_session_data(username)
        return session

    @rpc
    def delete_session(self, username):
        session = self.session_provider.delete_session(username)
        return session

    @rpc
    def get_session_data(self, session_id):
        session = self.session_provider.get_session_data(session_id)
        return session
