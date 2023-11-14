
import os 
import pymongo 
import smtplib 
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(filename='app.log', level=logging.INFO)


class Database:
    mongo_username =os.getenv("MONGO_INITDB_ROOT_USERNAME")
    mongo_password =  os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    mongo_host = os.getenv("MONGO_HOST")
    mongo_port =  int(os.getenv("MONGO_PORT"))

    def __init__(self):
        self.data = []

    def connect(self):
        try:
            connection_string = f"mongodb://{self.mongo_username}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/"
            client = pymongo.MongoClient(connection_string)
            db = client[os.getenv("MONGO_DATABASE_NAME")]
            self.collection = db[os.getenv("MONGO_COLLECTION_NAME")]
            logging.info("Successfully connected to the database.")

        except Exception as e:  
            logging.error(f"Error connecting to the database: {e}")


    def get_data(self):
        cursor = self.collection.find()
        for doc in cursor:
            self.data.append(doc)

class AlertGenerator:
    def __init__(self):
        self.alerts = []

    def generate_alerts(self, data):
        customers = {}
        for record in data:
            customer_id = record["order_vendor_dbname"]
            order_status = record["shipping_status"]
            if customer_id not in customers:
                customers[customer_id] = []
            customers[customer_id].append(record)
        for customer_id, records in customers.items():
            returned_or_cancelled = 0
            for record in records:
                order_status = record["shipping_status"]
                order_date = record["shipping_date"]
                if order_status in ["returned", "completed"]:
                    returned_or_cancelled += 1
                if returned_or_cancelled == 3:
                    alert = f"Alert: Customer {customer_id} has 3 or more orders returned or cancelled in the month of {order_date.month}. The orders are: {records}"
                    self.alerts.append(alert)
                    returned_or_cancelled = 0
        
    def send_email(self):
        try:
            server = smtplib.SMTP(os.getenv("EMAIL_SERVER"), os.getenv("EMAIL_PORT"))
            server.starttls()
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
            sender = os.getenv("EMAIL_USER")
            receiver = os.getenv("EMAIL_ADMIN")
            subject = "Customer Alerts for Returned or Cancelled Orders"
            body = "\n".join(self.alerts)
            message = f"From: {sender}\nTo: {receiver}\nSubject: {subject}\n\n{body}"
            server.sendmail(sender, receiver, message)
            server.quit()
            logging.info("Email sent successfully.")

        except Exception as e:
            logging.error(f"Error sending the email: {e}")
 
if __name__ == "__main__":
    database = Database()
    database.connect()
    database.get_data()
    alert_generator = AlertGenerator()

    alert_generator.generate_alerts(database.data)
    if alert_generator.alerts:
        alert_generator.send_email()
        logging.info("Email sent")
    else:
        logging.info("No alerts to send.")

