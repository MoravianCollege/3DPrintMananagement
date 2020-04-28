
# How to add worker
    # worker = Workers(name=current_user.name, email=current_user.email, is_Admin=False, is_Active=True)
    # db.session.add(worker)
    # db.session.commit()
# How to delete worker
    # db.session.delete(Workers.query.filter_by(email=current_user.email).first())
    # db.session.commit()
# How to query for a worker
#    worker = Workers.query.filter_by(email=current_user.email).first()
#    if worker is not None:
#        return "yes"

# How to get boolean field of table
    # worker = Workers.query.filter_by(email=current_user.email).first()
    # if worker is not None:
    #     print(worker.is_Active)