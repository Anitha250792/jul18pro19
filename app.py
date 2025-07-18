from flask import Flask, render_template, request
from markupsafe import Markup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    email_title = ""
    email_body = ""
    rendered_email = None

    if request.method == 'POST':
        email_title = request.form.get('email_title', '')
        email_body = request.form.get('email_body', '')

        # Example placeholders to replace in email body
        placeholders = {
            'user_name': 'John Doe',
            'date': 'July 18, 2025',
            'company': 'ACME Corp',
        }

        # Render the email body safely using Jinja2 template engine
        # Use from_string and pass placeholders as context
        from jinja2 import Template, StrictUndefined

        try:
            template = Template(email_body, undefined=StrictUndefined)
            rendered_body = template.render(**placeholders)
        except Exception as e:
            rendered_body = f"<p style='color:red;'>Error rendering template: {e}</p>"

        # Mark safe so Jinja2 doesn't autoescape rendered html
        rendered_email = Markup(rendered_body)

    return render_template('index.html',
                           email_title=email_title,
                           email_body=email_body,
                           rendered_email=rendered_email)
                           
if __name__ == '__main__':
    app.run(debug=True)
