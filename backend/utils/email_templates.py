# backend/utils/email_templates.py

from jinja2 import Environment, FileSystemLoader
import os
from typing import Dict

class EmailTemplate:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), '../templates/email')
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def render(self, template_name: str, context: Dict) -> str:
        """Render email template with context."""
        template = self.env.get_template(f"{template_name}.html")
        return template.render(**context)

# Example profit alert template
PROFIT_ALERT_TEMPLATE = """
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif;">
    <h2>Profit Alert for {{ symbol }}</h2>
    <div style="padding: 20px; background-color: #f8f9fa; border-radius: 5px;">
        <p><strong>Current Profit:</strong> {{ profit_percentage }}%</p>
        <p><strong>Current Price:</strong> ${{ current_price }}</p>
        <p><strong>Entry Price:</strong> ${{ entry_price }}</p>
        
        <h3>Analysis Summary</h3>
        <ul>
            {% for point in analysis_points %}
            <li>{{ point }}</li>
            {% endfor %}
        </ul>
        
        <div style="margin-top: 20px;">
            <a href="{{ dashboard_url }}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                View Dashboard
            </a>
        </div>
    </div>
</body>
</html>
"""