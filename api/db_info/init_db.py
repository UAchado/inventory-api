from sqlalchemy.orm import Session

from db_info import models

def init(db: Session):
    
    description = "description_opt"
    tags = {
        "auscultadoresfones": "Auscultadores/Fones",
        "carregadores": "Carregadores",
        "portateis": 'Portáteis',
        "tablets": "Tablets",
        "telemoveis": "Telemóveis",
    }
    images = {
        "auscultadores": "auscultadores.jpeg",
        "carregador": "carregador.jpeg",
        "portateis": "portateis.jpeg",
        "tablet": "tablet.jpeg",
        "telemovel": "telemovel.jpeg",
    }
    states = {
        "stored": "stored"
    }

    initial_items_on_db = [
        models.Item(description=description, tag=tags["tablets"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["carregadores"], image=images["carregador"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["carregadores"], image=images["carregador"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["telemoveis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["tablets"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["telemoveis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["telemoveis"], image=images["telemovel"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["telemoveis"], image=images["telemovel"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["carregadores"], image=images["carregador"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=images["auscultadores"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["telemoveis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["portateis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["tablets"], image=images["tablet"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["portateis"], image=images["portateis"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["carregadores"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["tablets"], image=images["tablet"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["telemoveis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["telemoveis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["tablets"], image=images["tablet"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=images["auscultadores"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=images["auscultadores"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=images["auscultadores"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["auscultadoresfones"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["carregadores"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["tablets"], image=images["tablet"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["portateis"], image=None, state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
        models.Item(description=description, tag=tags["tablets"], image=images["tablet"], state=states["stored"], dropoff_point_id=1, report_email=None, retrieved_email=None, retrieved_date=None),
    ]

    for entry in initial_items_on_db:
        db.add(entry)
    db.commit()