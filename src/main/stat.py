from django.db import connection
from django.template import Template, Context

class SQLLogMiddleware:

    def process_response(self, request, response):
        content_types = ('text/plain', 'text/html')
        if request.META['CONTENT_TYPE'] not in content_types:
            return response
        time = sum([float(q['time']) for q in connection.queries])
        template = Template(
            """
            <center>
            <div class="debug" style="margin-top:25px;">
                <p>
                    <em>Total query count:</em> {{ count }}
                    <br/>
                    <em>Total execution time:</em> {{ time }}
                </p>
            <div>
            </center>
            """
        )
        t = template.render(Context(dict(time=time, count=len(connection.queries))))
        content = response.content.decode('utf-8')
        body = '</body>'
        body_position = content.find(body)
        content = content[:body_position] + t + content[body_position:]
        response.content = content.encode('utf-8')
        return  response

    # def process_response(self, request, response):
    #     time = 0.0
    #     for q in connection.queries:
    #         time += float(q['time'])
    #
    #     """
    #     t = Template(u'''
    #         <p><em>Total query count:</em> {{ count }}<br/>
    #         <em>Total execution time:</em> {{ time }}</p>
    #         <ul class="sqllog">
    #             {% for sql in sqllog %}
    #                 <li>{{ sql.time }}: {{ sql.sql }}</li>
    #             {% endfor %}
    #         </ul>
    #     ''')
    #     """
    #
    #     t = Template('''
    #         <br />
    #         <center>
    #         <p><em>Total query count:</em> {{ count }}<br/>
    #         <em>Total execution time:</em> {{ time }}</p>
    #         </center>
    #     ''')
    #
    #     response.content = "%s%s" % ( response.content, t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time})))
    #     return response