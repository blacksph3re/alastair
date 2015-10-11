import csv, codecs, cStringIO
from django.core.urlresolvers import resolve
from django.template.defaulttags import register
from .models import Project


@register.filter(name='get_item')
def get_item(dictionary, key):
	return dictionary.get(key)


def prepareContext(request):
	context = {}
	if('activate_project' in request.GET):
		try:
			request.session['active_project']=int(request.GET.get('activate_project'))
		except:
			try:
				del request.session['active_project']
			except:
				pass
	
	try:
		context['active_project'] = Project.objects.get(id=request.session['active_project'])
	except:
		pass
	context['active_page'] = resolve(request.path_info).url_name
	context['pagetitle'] = context['active_page']
	return context

def _smallhelpforunicode(arg):
	if(arg == None):
		return ''
	return unicode(arg)


class UnicodeWriter:
	"""
	A CSV writer which will write rows to CSV file "f",
	which is encoded in the given encoding.
	"""

	def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
		# Redirect output to a queue
		self.queue = cStringIO.StringIO()
		self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
		self.stream = f
		self.encoder = codecs.getincrementalencoder(encoding)()

	def writerow(self, row):
		self.writer.writerow([_smallhelpforunicode(s).encode("utf-8") for s in row])
		# Fetch UTF-8 output from the queue ...
		data = self.queue.getvalue()
		data = data.decode("utf-8")
		# ... and reencode it into the target encoding
		data = self.encoder.encode(data)
		# write to the target stream
		self.stream.write(data)
		# empty queue
		self.queue.truncate(0)

	def writerows(self, rows):
		for row in rows:
			self.writerow(row)