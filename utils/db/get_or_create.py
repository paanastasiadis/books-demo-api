def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        # session.commit()
        return instance

def get_instance(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    return instance
