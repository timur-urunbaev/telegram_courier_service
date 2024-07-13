from . import models

def save_data_to_model(data):
    for order in data['orders']:
        products_list = []
        
        if not models.Order.objects.filter(pk=order['id']).exists():
            
            for item in order['items']:

                if not models.Product.objects.filter(pk=item['product']['id']).exists():

                    product_instance = models.Product.objects.create(
                        id=item['product']['id'],
                        name=item['product']['title'],
                        brand=item['product']['brand']['title'],
                    )

                if not models.ProductSet.objects.filter(product=product_instance, quantity=item['quantity']).exists():

                    product_set_instance = models.ProductSet.objects.create(
                        quantity=item['quantity'],
                        product=product_instance
                    )

                    products_list.append(product_set_instance)
            
            order_instance = models.Order.objects.create(
                id=order['id'],
                username=order['userName'],
                userphone=order['userPhone'],
                address=order['shippingCountry'] + ", " +  order['shippingRegion'] + ", " + order['shippingCity'] + ", " +  order['userAddress'],
                price=order['totalPriceAccepted'],
            )

            order_instance.products.set(products_list)
