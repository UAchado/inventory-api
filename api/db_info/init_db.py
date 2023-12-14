from sqlalchemy.orm import Session

from db_info import models

def init(db: Session):
    
    description = 'description_opt'
    tags = {
        "auscultadoresfones": "Auscultadores/Fones",
        "carregadores": "Carregadores",
        "portateis": 'Portáteis',
        "tablets": "Tablets",
        "telemoveis": "Telemóveis",
    }
    
    states = {
        "stored": "stored"
    }

    initial_items_on_db = [
        models.Item(description='description_opt', tag=tags["tablets"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["carregadores"], image='carregador.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["carregadores"], image='carregador.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["telemoveis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["tablets"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["telemoveis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["telemoveis"], image='telemovel.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["telemoveis"], image='telemovel.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["carregadores"], image='carregador.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image='auscultadores.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["telemoveis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["portateis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["tablets"], image='tablet.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["portateis"], image='portateis.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["carregadores"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["tablets"], image='tablet.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["telemoveis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["telemoveis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["tablets"], image='tablet.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image='auscultadores.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image='auscultadores.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image='auscultadores.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["carregadores"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["tablets"], image='tablet.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["portateis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description='description_opt', tag=tags["tablets"], image='tablet.jpeg', state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
    ]

    for entry in initial_items_on_db:
        db.add(entry)
    db.commit()