from sqlalchemy.orm import Session

from db_info import models

def init(db: Session):

    initial_items_on_db = [
        models.Item(description='description_opt', tag='Tablets', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Carregadores', image='carregador.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Carregadores', image='carregador.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Telemóveis', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Tablets', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Telemóveis', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Telemóveis', image='telemovel.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Telemóveis', image='telemovel.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Carregadores', image='carregador.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image='auscultadores.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Telemóveis', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Portáteis', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Tablets', image='tablet.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Portáteis', image='portateis.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Carregadores', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Tablets', image='tablet.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Telemóveis', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Telemóveis', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Tablets', image='tablet.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image='auscultadores.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image='auscultadores.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image='auscultadores.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Auscultadores/Fones', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Carregadores', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Tablets', image='tablet.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Portáteis', image=None, state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag='Tablets', image='tablet.jpeg', state='stored', dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
    ]

    for entry in initial_items_on_db:
        db.add(entry)
    db.commit()