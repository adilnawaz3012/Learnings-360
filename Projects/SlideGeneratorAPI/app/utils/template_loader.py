from app.models.schemas import Template, AspectRatio
import os
import json

TEMPLATES_DIR = "app/templates"
templates_db = {}

def load_templates():
    if not templates_db:
        # Load templates from files
        for filename in os.listdir(TEMPLATES_DIR):
            if filename.endswith(".json"):
                with open(os.path.join(TEMPLATES_DIR, filename)) as f:
                    data = json.load(f)
                    template = Template(**data)
                    templates_db[template.id] = template
    return templates_db

def get_template(template_id: str):
    templates = load_templates()
    return templates.get(template_id, templates["default"])