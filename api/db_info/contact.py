import smtplib
import os

from sqlalchemy.orm import Session
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from . import models, schemas

def contact_reported_email(db: Session, new_item: schemas.ItemCreate):
    stored_reports = [
        item for item in db.query(models.Item).filter(models.Item.tag == new_item.tag).all()
        if item.report_email != None
    ]
    for report in stored_reports:
        notified_mails = []
        if report.report_email not in notified_mails:
            
            subject = "O teu item foi UAchado!"
            message = f"""
                Um item parecido ao que reportaste acabou de ser UAchado em um dos nossos pontos.\n
                Dá uma olhada, pode ser que seja teu!\n\n
                
                Item: {report.tag}\n
                Descrição: {report.description}\n\n
        
                na UA, nada se perde, tudo se UAcha\n\n
                
                Cumprimentos\n
                Equipa do UAchado
            """
            send_email(report.report_email, subject, message)

            notified_mails.append(report.report_email)

def contact_new_report(report: schemas.ItemReport):
    
    subject = "O teu report foi adicionado!"
    message = f"""
        O teu relatório de perda acabou de chegar ao UAchado.\n\n
        
        Item: {report.tag}\n
        Descrição: {report.description}\n
        Email: {report.report_email}\n\n
        
        Assim que encontrarmos um item que possa ser o teu entraremos em contato.\n
        Tem atenção à tua caixa de correio. O nosso mail pode ser reencaminhado para o teu spam.\n\n
        
        na UA, nada se perde, tudo se UAcha\n\n
        
        Cumprimentos\n
        Equipa do UAchado
    """

    send_email(report.report_email, subject, message)

def contact_netrieved_email(item: schemas.Item):
    
    subject = "UAchaste o teu item!"
    message = f"""
        Acabaste de levantar um item!\n\n
        
        Item: {item.tag}\n
        Descrição: {item.description}\n
        Email: {item.retrieved_email}\n
        Data: {item.retrieved_date}\n\n
        
        Qualquer dúvida entra em contacto com a equipa do UAchado em uachado.app@gmail.com!\n\n
        
        Obrigado por utilizes o UAchado!\n
        na UA, nada se perde, tudo se UAcha\n\n
        
        Cumprimentos\n
        Equipa do UAchado
    """

    send_email(item.retrieved_email, subject, message)

def send_email(email: str, subject: str, message: str):
    try:
        username = os.environ.get("EMAIL_USERNAME")
        password = os.environ.get("EMAIL_PASSWORD")
        
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
            
        with smtplib.SMTP(os.environ.get("SMTP_SERVER"), int(os.environ.get("SMTP_PORT", int()))) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            print(f"INFO:\tEMAIL SENT TO: {email}")
    except smtplib.SMTPServerDisconnected:
        print("ERROR:\tServer disconnected unexpectedly.")
    except Exception as e:
        print(f"Error:\t{e}")