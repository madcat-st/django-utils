# -*- coding: utf-8 -*-
# Django helper stuff -- by madcat. MIT License.
from django.utils.safestring import mark_safe
from django.template import loader, Template, RequestContext, Context


def apply_tweakpage (f,DEFAULT_TEMPLATE):

    setdefaulttempl = True
    tweakpage = f.tweakpage

    try: template_name = f.template_name
    except: template_name = None

    if len(tweakpage)>4 and len(tweakpage.strip())>2:
        if template_name:
            tn = template_name
        else:
            tn = DEFAULT_TEMPLATE
        templ = '{%extends "'+tn+'" %}{%load addons%} ' + tweakpage
        setdefaulttempl = False
        try: t = Template(templ)
        except: setdefaulttempl = True

    if setdefaulttempl:
        if template_name:
            t = loader.select_template((template_name, DEFAULT_TEMPLATE))
        else:
            t = loader.get_template(DEFAULT_TEMPLATE)

    return t

def render_var (request,f):
    if f == '': return ''
    T = Template('{% load addons %}'+f)

    url = request.path
    if url.startswith('/album'):
      bits = url.split('/')
      url = '/'+bits[1]+'/'+bits[2]+'/'

    con = RequestContext(request, {'url':url} )
    return mark_safe(T.render(con))

def render_noreq (f, C = None):
    if f == '': return ''
    T = Template('{% load addons %}'+f)
    if not C:
     C = Context({})
    return mark_safe(T.render(C))

def gr (x, g=0):
    try: y=x.group(g)
    except: return x
    return y

def make_sort_index(base_url, si, s ):
    result=''
    namsort = ''
    for x in si:
        if x[0] == s:
            result+= u'<ul><li>%s</ul>'%x[1]
            namsort = x[1]
        else: result+= u'<a href="%s%s/">%s</a><br>'%(base_url, x[0], x[1])
    return result, namsort

def make_page_index(base_url,  current , total):
    if total ==1: return ''
    result = ''
    cur=int(current)
    if cur>1: result+=u'<a href="%s%d/"> &lt;&lt;&lt; Предыдущая &lt;&lt;&lt; </a>' % (base_url,cur-1)
    count= 1
    for c in xrange (total):
        if count==cur: result=result+ '<span class="curpage">%d</span>'%count
        else: result=result+ u'<a href="%s%d/"> %d </a>' % (base_url , count, count )
        count+=1
    if cur<total:result+=u'<a href="%s%d/"> &gt;&gt;&gt; Следующая &gt;&gt;&gt; </a>'%(base_url,cur+1)
    return result

def make_raz_index(objects,  current):
    #if objects==None return ''
    result = '<ul>'
    try: cur=current.get_absolute_url()
    except: cur = ''

    for c in objects:
        x = c.get_absolute_url()
        if x==cur: result+= '<ul><li>%s</li></ul>'%c.name
        else: result+= u'<li><a href="%s">%s</a></li>' % (x,c.name)
    result += '</ul>'
    return result

def get_pages_total(ipp, count):
    res = count / ipp
    if count % ipp !=0:
        res+=1
    return res

def get_index (ipp,page):
    i = int(ipp)
    p = int(page)
    if p<1: p=1
    return (i*(p-1)),(i*p)

class FileIterWrapper(object):
  def __init__(self, flo, chunk_size = 1024**2):
    self.flo = flo
    self.chunk_size = chunk_size

  def next(self):
    data = self.flo.read(self.chunk_size)
    if data:
      return data
    else:
      raise StopIteration

  def __iter__(self):
    return self

# ex: return HttpResponse(FileIterWrapper(open('/path/to/big/file.bin')))
