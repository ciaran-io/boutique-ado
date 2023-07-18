from django.shortcuts import redirect, reverse


def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    cart = request.session.get('cart', {})

    if item_id in cart:
        if size:
            cart[item_id]['items_by_size'].setdefault(size, 0)
            cart[item_id]['items_by_size'][size] += quantity
        else:
            cart[item_id] += quantity
    else:
        if size:
            cart[item_id] = {'items_by_size': {size: quantity}}
        else:
            cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)
