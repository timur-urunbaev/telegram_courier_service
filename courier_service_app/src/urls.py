from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    ######## User URLS ########
    path('couriers/', view=views.courier_list, name='courier_list'),
    path('couriers/<int:telegram_id>/', view=views.courier_detail, name='courier_detail'),
    ######## Order URLS ########
    path('bulavka/orders', view=views.fetch_and_display_data, name='fetch_and_display'),
    path('orders/', view=views.get_all_available_orders, name='order_list'),
    path('orders/page/<int:page>/', view=views.get_available_orders, name='page_order_list'),
    path('orders/<int:order_id>/', view=views.order_detail, name='order_detail'),
    path('orders/active/<str:telegram_id>/', view=views.get_my_active, name='order_active'),
    path('orders/history/<str:telegram_id>/', view=views.get_my_history, name='order_history'),
    path('orders/takeorder/', view=views.assign_courier_to_order, name='take_order'),
    path('orders/cancel/', view=views.remove_courier_from_order, name='cancel_order'),
    path('orders/finish/', view=views.finish_delivery, name='finish_delivery'),
    ######## PRODUCTS URLS ########
    path('orders/<int:order_id>/products/', view=views.get_orders_product_set, name='get_product_sets'),
    path('products/<product_id>/', view=views.get_product, name='get_products'),
    ######## Branch URLS ########
    path('branches/', view=views.get_branches, name='branch_list'),
    ######## JWT URLS ########
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]