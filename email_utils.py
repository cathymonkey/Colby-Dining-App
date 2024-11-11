import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "colbydining.feedback@gmail.com" 
        self.sender_password = "snft lurw wmsw uzov"  
        
    def send_feedback_email(self, name, email, feedback_type, message):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = "ztariq26@colby.edu"  # Replace with recipient email
            msg['Subject'] = f"Colby Dining Feedback - {feedback_type}"
            
            body = f"""
            New feedback received from Colby Dining website:
            
            Name: {name}
            Email: {email}
            Type: {feedback_type}
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Message:
            {message}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False