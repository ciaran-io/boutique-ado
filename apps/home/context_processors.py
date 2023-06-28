def navigation_lists(request):
    navigation_list = [
        {'name': 'All products', 'url': '#',
         'sublist': [
             {'name': 'By price', 'url': '#'},
             {'name': 'By rating', 'url': '#'},
             {'name': 'By category', 'url': '#'},
         ]},
        {'name': 'Clothing', 'url': '#',
         'sublist': [
             {'name': 'Jeans', 'url': 'dresses/'},
             {'name': 'Shirts', 'url': 'tops/'},
             {'name': 'All Clothing',
              'url': '#'},

         ]},
        {'name': 'Homeware', 'url': '#',
         'sublist': [
             {'name': 'Bed & Bath', 'url': '#'},
             {'name': 'Shirts', 'url': '#'},
             {'name': 'All Homeware',
              'url': '#'},

         ]},
        {'name': 'Special offers', 'url': '#',
         'sublist': [
             {'name': 'New Arrivals', 'url': '#'},
             {'name': 'Deals', 'url': '#'},
             {'name': 'Clearance', 'url': '#'},
             {'name': 'All Specials', 'url': '#'},
         ]},
    ]
    return {'navigation_list': navigation_list}
