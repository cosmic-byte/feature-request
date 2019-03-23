
def save_changes(session):
    try:
        session.commit()
    except:
        session.rollback()
        raise

