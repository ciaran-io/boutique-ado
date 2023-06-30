from django.urls import reverse

# Define the categories to be used in the navigation menu
# Clothing menu items
all_clothing_categories = ['activewear', 'essentials', 'jeans', 'shirts']
active_essentials_categories = ['activewear', 'essentials']

# Homeware menu items
all_homeware_categories = ['bed_bath', 'kitchen_dining']

# Special offers menu items
new_arrivals_categories = ['new_arrivals', 'deals', 'clearance']

# Convert lists to strings
all_clothing_categories_query = ','.join(all_clothing_categories)
active_essentials_categories_query = ','.join(active_essentials_categories)
all_homeware_categories_query = ','.join(all_homeware_categories)
new_arrivals_categories_query = ','.join(new_arrivals_categories)


def create_menu_item(name, url):
    return {'name': name, 'url': url}


def create_sublist(items):
    return [create_menu_item(name, url) for name, url in items]


def navigation_lists(request):
    navigation_list = [
        # All products menu & sub-menu
        {
            'name': 'All products',
            'url': '#',
            'sublist': create_sublist([
                ('By Price', 'price&direction=asc'),
                ('By Rating', 'rating&direction=desc'),
                ('By Category', 'category&direction=asc'),
            ])
        },
        # Clothing menu & sub-menu
        {
            'name': 'Clothing',
            'url': '#',
            'sublist': create_sublist([
                ('Activeware & Essentials',
                 f'{active_essentials_categories_query}'),
                ('Jeans', 'jeans'),
                ('Shirts', 'shirts'),
                ('All Clothing', f'{all_clothing_categories_query}')
            ])
        },
        # Homeware menu & sub-menu
        {
            'name': 'Homeware',
            'url': '#',
            'sublist': create_sublist([
                ('Bed & Bath', 'bed_bath'),
                ('Kitchen & Dining', 'kitchen_dining'),
                ('All Homeware', f'{all_homeware_categories_query}')
            ])
        },
        # Special offers menu & sub-menu
        {
            'name': 'Special offers',
            'url': '#',
            'sublist': create_sublist([
                ('New Arrivals', 'new_arrivals'),
                ('Deals', 'deals'),
                ('Clearance', 'clearance'),
                ('All Specials', f'{new_arrivals_categories_query}')
            ])
        },
    ]
    return {'navigation_list': navigation_list}
