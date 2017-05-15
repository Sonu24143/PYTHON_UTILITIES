#!/usr/bin/python

import web

urls = (
  '/SayHello', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates/' , base="Layout")

class Index(object):
    def GET(self):
	form = web.input (name="Nobody" , place="")
        greeting = "Hello , %s! . You are from %s" % (form.name , form.place)
        return render.sonu(greeting = greeting)

if __name__ == "__main__":
    app.run()
