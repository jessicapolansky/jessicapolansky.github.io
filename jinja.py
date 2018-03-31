from jinja2 import \
  Environment, PackageLoader, select_autoescape
ENV = Environment(
  loader=PackageLoader('myapp', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
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
      name = self.get_query_argument('name', '')
    self.render_template("hello.html", {'name': 'World'})
