# backend/services/email_service.py

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from typing import List, Dict
import logging
from datetime import datetime
from ..utils.email_templates import EmailTemplate

class EmailService:
    def __init__(self):
        self.smtp_settings = {
            'server': 'smtp.gmail.com',
            'port': 587,
            'username': 'your-email@gmail.com',
            'password': 'your-app-password'  # Use app-specific password
        }
        self.default_recipient = "polis.srikanth@gmail.com"
        self.template_engine = EmailTemplate()
    
    async def send_alert(
        self,
        subject: str,
        content: Dict,
        template_name: str,
        recipients: List[str] = None
    ):
        """Send email alert."""
        try:
            if recipients is None:
                recipients = [self.default_recipient]
            
            # Generate HTML content
            html_content = self.template_engine.render(
                template_name,
                content
            )
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_settings['username']
            msg['To'] = ', '.join(recipients)
            
            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            with smtplib.SMTP(
                self.smtp_settings['server'],
                self.smtp_settings['port']
            ) as server:
                server.starttls()
                server.login(
                    self.smtp_settings['username'],
                    self.smtp_settings['password']
                )
                server.send_message(msg)
            
            logging.info(f"Alert email sent: {subject}")
            
        except Exception as e:
            logging.error(f"Email send error: {str(e)}")
            raise
    
    async def send_profit_alert(
        self,
        symbol: str,
        profit_data: Dict,
        analysis: Dict
    ):
        """Send profit alert email."""
        try:
            content = {
                'symbol': symbol,
                'profit': profit_data,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat(),
                'actions': [
                    {
                        'text': 'View Details',
                        'url': f'/dashboard/stocks/{symbol}'
                    },
                    {
                        'text': 'Take Profit',
                        'url': f'/dashboard/trade/{symbol}'
                    }
                ]
            }
            
            await self.send_alert(
                subject=f"Profit Alert: {symbol} reached {profit_data['percentage']}% profit",
                content=content,
                template_name='profit_alert'
            )
            
        except Exception as e:
            logging.error(f"Profit alert error for {symbol}: {str(e)}")
            raise
    
    async def send_risk_alert(
        self,
        symbol: str,
        risk_data: Dict,
        analysis: Dict
    ):
        """Send risk alert email."""
        try:
            content = {
                'symbol': symbol,
                'risk': risk_data,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat(),
                'actions': [
                    {
                        'text': 'Review Position',
                        'url': f'/dashboard/stocks/{symbol}'
                    }
                ]
            }
            
            await self.send_alert(
                subject=f"Risk Alert: {symbol} risk level increased",
                content=content,
                template_name='risk_alert'
            )
            
        except Exception as e:
            logging.error(f"Risk alert error for {symbol}: {str(e)}")
            raise
    
    async def send_daily_summary(
        self,
        portfolio_data: Dict,
        performance: Dict
    ):
        """Send daily portfolio summary."""
        try:
            content = {
                'portfolio': portfolio_data,
                'performance': performance,
                'timestamp': datetime.now().isoformat(),
                'actions': [
                    {
                        'text': 'View Portfolio',
                        'url': '/dashboard/portfolio'
                    }
                ]
            }
            
            await self.send_alert(
                subject="Daily Portfolio Summary",
                content=content,
                template_name='daily_summary'
            )
            
        except Exception as e:
            logging.error(f"Daily summary error: {str(e)}")
            raise