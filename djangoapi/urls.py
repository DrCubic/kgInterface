from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^getNodesInfo/$', 'kgInterface.views.get_node_info'),
    url(r'^getDisOut/$', 'kgInterface.views.get_diseases_out'),
    url(r'^getMedOut/$', 'kgInterface.views.get_medicines_out'),
    url(r'^getDisRelation/$', 'kgInterface.views.get_diseases_relations'),
    url(r'^getMedRelation/$', 'kgInterface.views.get_medicines_relations'),
    url(r'^getQueryOut/$', 'queryShow.views.get_query_output'),
)
