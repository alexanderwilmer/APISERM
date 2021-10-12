"""

from django.urls import include, path


from django.contrib import admin





# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin',admin.site.urls),
]
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from users import views
from django.urls import resolve

from solicitudes import  views as s
from rest_framework_simplejwt.views import TokenObtainSlidingView,TokenRefreshSlidingView,TokenVerifyView

from users import autenticate as jwt_views 
 

from rest_framework.authtoken import views as tok

#from cotizaciones.views import  ApiSolicitudCotizacionAPIView,ApiSolicitudCotizacionDetails


router = routers.DefaultRouter()

#router.register(r'cotizacion', ApiSolicitudCotizacionAPIView)
#router.register(r'detalle_cotizacion',ApiSolicitudCotizacionDetails)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('general/', include('general.urls')),
    path('', include('solicitudes.urls')),
    #path('cotizacion/', include('cotizaciones.urls')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	#path('api/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    #path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', 
         jwt_views.TokenObtainPairView.as_view(), 
         name ='token_obtain_pair'), 
    path('api/token/refresh/', 
         jwt_views.TokenRefreshView.as_view(), 
         name ='token_refresh'), 
 

]
