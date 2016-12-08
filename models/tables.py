import datetime

def get_first_name():
    name = "Unidentified user"
    if auth.user:
        name = auth.user.first_name
    return name

def get_first_email():
    email = "None"
    if auth.user:
        email = auth.user.email
    return email

def get_user_info():
    value = "None"
    if auth.user:
        value = auth.user.id
    return value

User = db.auth_user
user = db.auth_user

alphabetical = User.first_name|User.last_name

def name_of(user): return "%(first_name)s %(last_name)s" %user

def get_user_email():
    return auth.user.email if auth.user else None




#For index page.
#Posting text.
db.define_table("post",
                Field("user_email", default=auth.user.email if auth.user_id else None, readable=False,writable=False),
                Field("posted_by", default=get_user_email),
                Field("post_content", 'text', requires=IS_NOT_EMPTY()),
                Field("posted_on", "datetime", default=datetime.datetime.utcnow(),readable=False,writable=False),
                Field("updated_on", "datetime", update=datetime.datetime.utcnow(),readable=False,writable=False),
                )




#For Profile Page
db.define_table('profile',
                Field("Name"),
                Field("creator", db.auth_user, default=auth.user_id, readable=False,writable=False),
                Field("bio", "text"),
                Field("job", "text"),
                Field("Profile_pic", "upload",requires=IS_EMPTY_OR(IS_IMAGE(error_message="Please! upload an image file.")))
                )
db.auth_user.Profile_pic.requires = IS_EMPTY_OR(IS_IMAGE(error_message="Please! upload an image file."))




#For image upload page
#Comments on each immage
db.define_table("image",
                Field("title"),
                Field("file1", "upload"),
                Field("posted_on","datetime",default=datetime.datetime.utcnow(),writable=True),
                Field("posted_by","reference auth_user",readable=False,writable=False),
                format="%(title)s")
db.define_table("comment1",
                Field("image","reference image",readable=False,writable=False),
                Field("parent_comment1","reference comment1",readable=False,writable=False),
                Field("body","text",notnull=True),
                Field("posted_on","datetime",readable=False,writable=False),
                Field("posted_by","reference auth_user",readable=False,writable=False))




#For send mail to other user
db.define_table("mail",
                Field("User", db.auth_user, default=get_user_info(), writable=False),
                Field("Receiver", db.auth_user, requires=IS_EMPTY_OR(IS_IN_DB(db(db.auth_user), 'auth_user.id', '%(first_name)s'))),
                Field("Message","text",requires=IS_NOT_EMPTY()),
                Field("Posted_on","datetime",default = datetime.datetime.utcnow(),writable=False)
                )
db.mail.id.readable = False




# coding: utf8
# For Video Post
SERVICES = {"youtube": T("Youtube")}
db.define_table("video",
                Field("title"),
                Field("service", requires=IS_IN_SET(SERVICES), default="static", comment=T("Choose Youtube")),
                Field("code", comment=T("Paste Youtube URL")),
                Field("abstract", "text"),
                Field("thumbnail", "upload", default=''),
                Field("user_id", "reference auth_user", label=T("User"), default=auth.user_id),
                Field("posted_on","datetime", default=datetime.datetime.utcnow(), writable=False),
                Field("posted_by","reference auth_user", readable=False,writable=False),
                format="%(title)s")

db.define_table('comment2',
                Field("video","reference video",readable=False,writable=False),
                Field("parent_comment2","reference comment2",readable=False,writable=False),
                Field("body",'text',notnull=True),
                Field("posted_on","datetime",readable=False,writable=False),
                Field("posted_by","reference auth_user",readable=False,writable=False))




#For game lists and its content
db.define_table("game",
                Field("title"),
                Field("description", "text"),
                Field("service", requires=IS_IN_SET(SERVICES), default="static",
                      comment=T("Choose how the content should be retrieved")),
                Field("code", comment=T("Used with services like Youtube for identifying streams")),
                Field("rating", "text"),
                Field("thumbnail", "upload",default=''),
                Field('posted_on','datetime',default=datetime.datetime.utcnow(),writable=False),
                Field("user_id", "reference auth_user", label=T("User"), default=auth.user_id),
                Field('posted_by','reference auth_user',readable=False,writable=False),
                format="%(title)s"
                )
db.define_table('comment3',
                Field('game','reference game',readable=False,writable=False),
                Field('parent_comment3','reference comment3',readable=False,writable=False),
                Field('body','text',notnull=True),
                Field('posted_on','datetime',readable=False,writable=False),
                Field('posted_by','reference auth_user',readable=False,writable=False)
                )




#For game lists and its content
db.define_table("anime",
                Field("title"),
                Field("description", "text"),
                Field("service", requires=IS_IN_SET(SERVICES), default="static",
                      comment=T("Choose how the content should be retrieved")),
                Field("code", comment=T("Used with services like Youtube for identifying streams")),
                Field("rating", "text"),
                Field("thumbnail", "upload",default=''),
                Field('posted_on','datetime',default=datetime.datetime.utcnow(),writable=False),
                Field("user_id", "reference auth_user", label=T("User"), default=auth.user_id),
                Field('posted_by','reference auth_user',readable=False,writable=False),
                format="%(title)s"
                )
db.define_table('comment4',
                Field('anime','reference anime',readable=False,writable=False),
                Field('parent_comment4','reference comment4',readable=False,writable=False),
                Field('body','text',notnull=True),
                Field('posted_on','datetime',readable=False,writable=False),
                Field('posted_by','reference auth_user',readable=False,writable=False)
                )