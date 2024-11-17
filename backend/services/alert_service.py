# backend/services/alert_service.py

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import asyncio
from typing import Dict, List
import logging
from datetime import datetime

class AlertService:
    def __init__(self):
        self.email_recipients = ["polis.srikanth@gmail.com"]
        self.smtp_settings = {
            "server": "smtp.gmail.com",
            "port": 587,
            "username": "your-email@gmail.com",  # Configure with your email
            "password": "your-app-password"      # Use app-specific password
        }
        
    async def monitor_profits(self, symbol: str, current_price: float, entry_price: float, 
                            threshold: float, analysis: Dict):
        """Monitor profits and send alerts when threshold is reached."""
        try:
            profit_percentage = (current_price - entry_price) / entry_price
            
            if profit_percentage >= threshold:
                alert_data = {
                    'symbol': symbol,
                    'profit_percentage': profit_percentage * 100,
                    'current_price': current_price,
                    'entry_price': entry_price,
                    'threshold': threshold * 100,
                    'analysis': analysis
                }
                
                await self.send_profit_alert(alert_data)
                
        except Exception as e:
            logging.error(f"Error monitoring profits: {str(e)}")
    
    async def send_profit_alert(self, data: Dict):
        """Send profit alert email."""
        try:
            subject = f"Profit Alert: {data['symbol']} reached {data['profit_percentage']:.2f}% profit"
            
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Profit Target Reached</h2>
                    <div style="padding: 20px; background-color: #f8f9fa; border-radius: 5px;">
                        <p><strong>Stock:</strong> {data['symbol']}</p>
                        <p><strong>Profit:</strong> {data['profit_percentage']:.2f}%</p>
                        <p><strong>Current Price:</strong> ${data['current_price']:.2f}</p>
                        <p><strong>Entry Price:</strong> ${data['entry_price']:.2f}</p>
                        <p><strong>Threshold:</strong> {data['threshold']:.1f}%</p>
                        
                        <h3>Analysis Summary</h3>
                        <ul>
                            <li>Market Sentiment: {data['analysis'].get('sentiment', 'N/A')}</li>
                            <li>Volume Analysis: {data['analysis'].get('volume', 'N/A')}</li>
                            <li>Technical Indicators: {data['analysis'].get('technical', 'N/A')}</li>
                        </ul>
                        
                        <div style="margin-top: 20px; padding: 10px; background-color: #e9ecef; border-radius: 3px;">
                            <p><strong>Recommendation:</strong> Consider taking profits based on your trading strategy.</p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.smtp_settings['username']
            msg['To'] = ', '.join(self.email_recipients)
            
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_settings['server'], self.smtp_settings['port']) as server:
                server.starttls()
                server.login(self.smtp_settings['username'], self.smtp_settings['password'])
                server.send_message(msg)
            
            logging.info(f"Profit alert sent for {data['symbol']}")
            
        except Exception as e:
            logging.error(f"Error sending profit alert: {str(e)}")