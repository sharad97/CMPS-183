#Gets username from email
#got this code from homework assginment
def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])




#Index file
@auth.requires_login()
def index():
    """
    This is your main controller.  Here you do almost nothing; you just cause index.html to be served.
    """
    return dict()




# Uploads Imaage
# I got the idea from "http://stackoverflow.com/questions/6334360/web2py-how-should-i-display-an-uploaded-image-that-is-stored-in-a-database" and
# "http://stackoverflow.com/questions/26987446/file-uploading-in-web2py"
def download(): return response.download(request, db)
def link(): return response.download(request, db, attachment=False)

@auth.requires_login()
def picture():
    image_form = FORM(
        INPUT(_name='image_title', _type='text'),
        INPUT(_name='image_file', _type='file')
    )
    if image_form.accepts(request.vars, formname='image_form'):
        response.flash = T('Posted')
        image = db.image.file1.store(image_form.vars.image_file.file, image_form.vars.image_file.filename)
        id = db.image.insert(file1=image, title=image_form.vars.image_title)
    images = db().select(db.image.ALL)
    return dict(images=images)

#Post comments for images
#Got Idea from "http://stackoverflow.com/questions/3517072/modify-crud-form-in-web2py-before-sending-to-view",
# "http://web2py.com/books/default/chapter/29/07/forms-and-validators, and web2py examples"
@auth.requires_login()
def image_comments():
    image = db.image(request.args(0)) or redirect(URL('picture'))
    if auth.user:
        db.comment1.parent_comment1.default = request.args(1)
        db.comment1.image.default = image.id
        db.comment1.posted_on.default = request.now
        db.comment1.posted_by.default = auth.user.id
        form = crud.create(db.comment1)
    comments = db(db.comment1.image==image.id).select(orderby=db.comment1.posted_on)
    return locals()

#Display all pictures
@auth.requires_login()
#Pictures
def picture1():
    images = db(db.image).select(orderby=~db.image.posted_on)
    return dict(images=images)




#send message to users
#Got I idea from "http://stackoverflow.com/questions/16351995/web2py-email-authentication" and
#"http://stackoverflow.com/questions/23268198/flash-message-not-getting-displayed-even-after-form-gets-processed"
@auth.requires_login()
def mail():
    form = SQLFORM(db.mail)
    if form.process().accepted:
        response.flash = T('Sent')
    return dict(form=form)

#message list received
#Got idea from "http://stackoverflow.com/questions/36939157/adding-links-to-sqlform-grid-web2py"
@auth.requires_login()
def message():
    U = db.mail.Receiver == auth.user_id
    form = SQLFORM.grid(U, orderby=~db.mail.Posted_on, deletable=True, create=False, editable=False,
                        selectable=None, csv = False, searchable=False, details=True)
    return locals()




# Upload youtube video link and display
# Got idea from "http://stackoverflow.com/questions/31360539/python-module-installed-properly-but-standard-function-not-working-in-web2py"
# -*- coding: utf-8 -*
def authorize(table, record_id):
    myrecord = db[table][record_id]
    if not ((myrecord.user_id == auth.user_id) or (auth.has_membership(role="manager"))):
        session.flash = T('Unauthorized User')
        redirect(URL('default', 'video1'))


if request.function in ["show", "subtitles", "slides"]:
    #Got this file from http://popcornjs.org/download
    #It is a HTML5 Media Framework
    response.files.append(URL(c='static', f="js/popcorn_complete.js"))
    response.files.append(URL(c='static', f="js/jquery.scrollTo.min.js"))
    response.files.append(URL(c='static', f="css/video.css"))

@auth.requires_login()
def video1():
    videos = db(db.video).select(orderby=~db.video.posted_on)
    return dict(videos=videos)

@auth.requires_login()
def show():
    video = db.video[request.args(1)]
    video_id = request.args(0)
    if auth.user:
        db.comment2.parent_comment2.default = request.args(1)
        db.comment2.video.default = video.id
        db.comment2.posted_on.default = request.now
        db.comment2.posted_by.default = auth.user.id
        form = crud.create(db.comment2)
    comments = db(db.comment2.video == video.id).select(orderby=db.comment2.posted_on)
    return locals()

@auth.requires_login()
def video():
    action = request.args(0)
    video_id = request.args(1)
    db.video.user_id.writable = False
    if action == "update":
        video = db.video[video_id]
        authorize("video", video.id)
        form = crud.update(db.video, video_id)
    else:
        form = crud.create(db.video)
    return dict(form=form, video_id=video_id)




# Displays list of games and video from youtube Url
# Got idea from "http://stackoverflow.com/questions/31360539/python-module-installed-properly-but-standard-function-not-working-in-web2py"
# -*- coding: utf-8 -*-
if request.function in ["gameshow", "subtitles", "slides"]:
    response.files.append(URL(c='static', f="js/popcorn_complete.js"))
    response.files.append(URL(c='static', f="js/jquery.scrollTo.min.js"))
    response.files.append(URL(c='static', f="css/video.css"))

@auth.requires_login()
def games():
    games = db(db.game).select()
    return dict(games=games)

@auth.requires_login()
def gameshow():
    game = db.game[request.args(1)]
    game_id = request.args(0)
    if auth.user:
        db.comment3.parent_comment3.default = request.args(1)
        db.comment3.game.default = game.id
        db.comment3.posted_on.default = request.now
        db.comment3.posted_by.default = auth.user.id
        form = crud.create(db.comment3)
    comments = db(db.comment3.game == game.id).select(orderby=db.comment3.posted_on)
    return locals()

@auth.requires_membership('manager')
@auth.requires_login()
def game():
    action = request.args(0)
    game_id = request.args(1)
    db.game.user_id.writable = False
    if action == "update":
        game = db.game[game_id]
        authorize("game", game.id)
        form = crud.update(db.game, game_id)
    else:
        form = crud.create(db.game)
    return dict(form=form, game_id=game_id)




# Displays list of anime and video from youtube Url
# Got idea from "http://stackoverflow.com/questions/31360539/python-module-installed-properly-but-standard-function-not-working-in-web2py"
# -*- coding: utf-8 -*-
if request.function in ["animeshow", "subtitles", "slides"]:
    response.files.append(URL(c='static', f="js/popcorn_complete.js"))
    response.files.append(URL(c='static', f="js/jquery.scrollTo.min.js"))
    response.files.append(URL(c='static', f="css/video.css"))

@auth.requires_login()
def animes():
    animes = db(db.anime).select()
    return dict(animes=animes)

@auth.requires_login()
def animeshow():
    anime = db.anime[request.args(1)]
    anime_id = request.args(0)
    if auth.user:
        db.comment4.parent_comment4.default = request.args(1)
        db.comment4.anime.default = anime.id
        db.comment4.posted_on.default = request.now
        db.comment4.posted_by.default = auth.user.id
        form = crud.create(db.comment4)
    comments = db(db.comment4.anime == anime.id).select(orderby=db.comment4.posted_on)
    return locals()

@auth.requires_membership('manager')
@auth.requires_login()
def anime():
    action = request.args(0)
    anime_id = request.args(1)
    db.anime.user_id.writable = False
    if action == "update":
        anime = db.anime[anime_id]
        authorize("anime", anime.id)
        form = crud.update(db.anime, anime_id)
    else:
        form = crud.create(db.anime)
    return dict(form=form, anime_id=anime_id)




#Display profile
@auth.requires_login()
def profile():
    form = ''
    pics = db(db.auth_user.id == auth.user_id).select().first()
    url = URL('download')
    form = SQLFORM(db.auth_user, readonly=True, upload=url,  record=pics)
    return dict(pics=pics, form=form)




#About
def about():
    return dict()




def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()