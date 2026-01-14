from django.urls import path
from .views import (NeedCreateView, NeedDetailView, NeedListView, AcceptNeedView, CancelNeedView, CompleteNeedView )


urlpatterns = [
    path('need/create/', NeedCreateView.as_view(), name='create_need'),
    path("need/<int:pk>/", NeedDetailView.as_view(), name="need_detail"),
    path('needs/', NeedListView.as_view(), name='need_list'),
    path("need/<int:need_id>/accept/", AcceptNeedView.as_view(), name="accept_need"),
    path("need/<int:need_id>/cancel/", CancelNeedView.as_view(), name="cancel_need"),
    path("need/<int:need_id>/complete/", CompleteNeedView.as_view(), name="complete_need"),
]

