#!/usr/bin/python
import web

urls = (
  '/hello', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/' , base="Layout")

class Index(object):
    def GET(self):
        return render.hello_post_form()

    def POST(self):
        form = web.input(name="Nobody", place="Earth")
        if form.place == "":
	    form.place="Earth"
	if form.name == "":
	    form.name="Human"	
        greeting = "Hi %s, you are from %s" % (form.name, form.place)
        return render.sonu(greeting = greeting)

if __name__ == "__main__":
    app.run()
