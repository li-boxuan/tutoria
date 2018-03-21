from django.http import HttpResponse
from django.views import generic
from account.models import SubjectTag, Course
import json


class IndexView(generic.TemplateView):
    template_name = 'index.html'
    # context_object_name = 'index_context'


def get_keywords(req):
    if req.is_ajax():
        query = req.GET.get('term', '')
        tags = SubjectTag.objects.filter(tag__icontains=query)[:10]
        courses = Course.objects.filter(course_name__icontains=query)[:10]
        results = []
        for course in courses:
            cjs = {}
            cjs['id'] = course.course_code
            cjs['label'] = course.course_name
            cjs['value'] = course.course_name
            results.append(cjs)
        for tag in tags:
            tjs = {}
            tjs['id'] = tag.pk
            tjs['label'] = tag.tag
            tjs['value'] = tag.tag
            results.append(tjs)
        data = json.dumps(results)
    else:
        data = 'fail'
    return HttpResponse(data, 'application/json')
