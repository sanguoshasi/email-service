import os

from flask import Flask, request, render_template
from email_manager import EmailMgr

# instantiate the extensions

#email_mgr =


def create_app():
    """Flask app factory.
    Useage::
        from application.py import create_app
        def run():
            app = create_app()
            app.run(host='0.0.0.0', port=5000, debug=app.debug)
        if __name__=="__main__":
            run()
    :rtype: :py:class:``flask.Flask``
    :returns: A new :py:class:``flask.Flask`` application instance
    """
    # instantiate the app
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )

    # set config
    app_settings = os.getenv(
        'EMAIL_SERVICE_SETTINGS', 'email_service.config.DevelopmentConfig')
    app.config.from_object(app_settings)

    # set up email_services

    email_mgr = EmailMgr(app.config.get('EMAIL_SERVICES'), app.config.get('DEBUG'))

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/', methods=['POST'])
    def send():
        result = email_mgr.submit_email(request.form, request.files.get('attachment'))
        return render_template('index.html', message=result.message)
    return app
