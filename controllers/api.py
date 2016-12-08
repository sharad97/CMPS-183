#Used code from homework assignment and edited

def get_user(email):

    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


def get_posts():
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    posts = []
    has_more = False
    rows = db().select(db.post.ALL, orderby=~db.post.posted_on, limitby=(start_idx, end_idx + 1))
    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            t = dict(
                id=r.id,
                user_email=r.user_email,
                content=r.post_content,
                posted_on=r.posted_on,
                updated_on=r.updated_on,
                posted_by=get_user(r.user_email)
            )
            posts.append(t)
        else:
            has_more = True
    logged_in = auth.user_id is not None
    return response.json(dict(
        posts=posts,
        logged_in=logged_in,
        has_more=has_more,
    ))


@auth.requires_signature()
def add_post():
    user_email = auth.user.email or None
    p_id = db.post.insert(post_content=request.vars.content)
    p = db.post(p_id)
    post = dict(
            id=p.id,
            user_email=p.user_email,
            content=p.post_content,
            posted_on=p.posted_on,
            updated_on=p.updated_on,
            posted_by=get_user(p.user_email)
    )
    print p
    return response.json(dict(post=post))


@auth.requires_signature()
def edit_post():
    post = db(db.post.id == request.vars.id).select().first()
    post.update_record(post_content=request.vars.post_content)
    print post
    return dict()


@auth.requires_signature()
def del_post():
    db(db.post.id == request.vars.post_id).delete()
    return "ok"

