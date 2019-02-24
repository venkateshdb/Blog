from app import db

class Posts(db.Model):
    """
    content to be posted
    """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.string())
    title = db.Column(db.string(), nullable=False)
    sub_title = db.Column(db.string())
    content = db.Column(db.string(), nullable=False)

    def __init__(self,date,title,sub_title,content):
        self.date = date
        self.title = title
        self.sub_title = sub_title
        self.content = content

    def __repr__(self):
        return "<id {}>".format(self.id)

class auth(db.Model):
    """
    user auth
    """
    __tablename__ = "auth"

    user_id = db.Column(db.sting(), primary_key=True, nullable=False)
    username = db.Column(db.string(), nullable=False)
    password = db.Column(db.string(), nullable=False)

    def __init__(self,user_id,username,password):

        self.user_id = user_id
        self.username = username
        self.password = password

    def __repr__(self):
        return "<user_id {}>".format(self.user_id)
