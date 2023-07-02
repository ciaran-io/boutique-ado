from django.shortcuts import redirect, reverse


def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """

    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    cart[item_id] = cart.get(item_id, quantity)

    if cart[item_id] == quantity:
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart

    redirect_url = request.POST.get('redirect_url')

    return redirect(redirect_url)
