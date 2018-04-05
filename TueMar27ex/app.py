import tornado.ioloop
import tornado.web
import tornado.log
import os
import boto3
from jinja2 import \
Environment, PackageLoader, select_autoescape
ENV = Environment(
  loader=PackageLoader('myapp', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)
client = boto3.client(
  'ses',
  region_name='us-west-2',
  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
  aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
)
class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))
    
class MainHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("home.html", {'name': 'World'})
class Successhandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("form-success.html", {})
    
    
class FormHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template("form.html", {})
    
  def post(self):
    email = self.get_body_argument('email')
    error = ''
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    # self.render_template("form.html", {'error': error})
    
    if email:
      response = client.send_email(
      Destination={
        'ToAddresses': ['jessica.polansky@gmail.com'],
      },
      Message={
        'Body': {
          'Text': {
            'Charset': 'UTF-8',
            'Data': '{} wants to talk to you.'.format(email),
          },
        },
        'Subject': {'Charset': 'UTF-8', 'Data': 'Test email'},
      },
      Source='mailer@jessicapolansky.com',
      )
      self.redirect('/form-success')
    else:
      error = "Please enter an email address for us to reply to you!"
      self.redirect('/form', {'error': error} )   
      
    
    

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/form", FormHandler),
    (r"/form-success", Successhandler),
    (
      r"/static/(.*)",
      tornado.web.StaticFileHandler,
      {'path': 'static'}
    ),
  ], autoreload=True)
  
if __name__ == "__main__":
  app = make_app()
  app.listen(8000)
  tornado.ioloop.IOLoop.current().start()