from django.shortcuts import render,HttpResponse,redirect

# Create your views

from lxml import etree
from operator import itemgetter
import json
import re
from homepage.scrape import nogil


def home(request):
    return render(request,"Homepage/index.html")


def get_search(request):
    query = request.GET.get('q')
    print(query)

    # check if a valid name is entered and display alert message if not
    if query is None or query == "":
        return redirect('/')
    else:
        urls = [
            'https://www.konga.com/v1/json/search?q=values&from=9',
            'https://www.jumia.com.ng/catalog/?q=values&page=1',
            'https://www.konga.com/v1/json/search?q=values&from=1',
            'https://www.konga.com/v1/json/search?q=values&from=18',
            'https://www.konga.com/v1/json/search?q=values&from=27',
            'https://www.konga.com/v1/json/search?q=values&from=36',
            'https://www.konga.com/v1/json/search?q=values&from=45',
            'https://www.konga.com/v1/json/search?q=values&from=54',
            'https://www.konga.com/v1/json/search?q=values&from=63',
            'https://www.konga.com/v1/json/search?q=values&from=72',
            'https://www.konga.com/v1/json/search?q=values&from=81',
            'https://www.jumia.com.ng/catalog/?q=values&page=2',
            'http://www.kara.com.ng/catalogsearch/result/index?cat=0&q=values'
        ]
        if len(query) > 1:
            query1 = query.replace(" ", "+")
        urls = [url.replace('values', query1) for url in urls]
        print(urls)

        response = nogil.greet(urls)
        my_list = []
        for data in response:

            # to search through jumia catalogue
            if 'konga' in data:
                tree = json.loads(data)
                list1 = tree['data']
                for l, m in enumerate(list1['products']):
                    vals = {}
                    vals['title'] = list1['products'][l]['fields']['name']
                    vals['link'] = 'https://www.konga.com/' + list1['products'][l]['fields']['url_key']
                    vals['image'] = 'https://images.konga.com/v2/media/catalog/product' + \
                                    list1['products'][l]['fields'][
                                        'image_thumbnail_path']
                    value = list1['products'][l]['fields']['price']
                    vals['preview'] = "../../static/img/konga.jpg"
                    vals['price'] = value
                    my_list.append(vals)

            # to search through jumia catalogue
            elif 'jumia' in data:
                tree = etree.HTML(data)
                list1 = tree.xpath("/html/body/main/section/section[2]/div[@class='sku -gallery']")
                for y, z in enumerate(list1, 2):
                    vals = {}
                    vals['title'] = str(
                        tree.xpath('/html/body/main/section/section[2]/div[' + str(y) + ']/a/h2/span[2]/text()')).strip(
                        "[']")
                    vals['link'] = str(
                        tree.xpath('/html/body/main/section/section[2]/div[' + str(y) + ']/a/@href')).strip("[']")
                    vals['image'] = str(tree.xpath(
                        '/html/body/main/section/section[2]/div[' + str(y) + ']/a/div[2]/img/@data-src')).strip("[']")

                    value = re.sub("[^0-9]", "", str(tree.xpath('/html/body/main/section/section[2]/div[' + str(y)
                                                                + ']/a/div[3]/span/span[1]/span[2]/text()')))
                    vals['preview'] = "../../static/img/jumia.jpg"
                    if len(value) < 2:
                        vals['title'] = 'none'
                    else:
                        men = int(value)
                    vals['price'] = int(men)

                    my_list.append(vals)

            elif 'kara' in data:
                tree = etree.HTML(data)
                list1 = tree.xpath('//div[@class="category-products"]/ul/li')
                for i, j in enumerate(list1, 1):
                    vals = {}
                    vals['title'] = tree.xpath('//div[@class="category-products"]/ul/li[' + str(i) + ']/a/@title')[0]
                    vals['link'] = tree.xpath('//div[@class="category-products"]/ul/li[' + str(i) + ']/a/@href')[0]
                    vals['image'] = \
                    tree.xpath('//div[@class="category-products"]/ul/li[' + str(i) + ']/a/img/@data-src')[0]
                    vals['preview'] = "../../static/img/kara.jpg"
                    lon = str(tree.xpath('//div[@class="category-products"]/ul/li[' + str(
                        i) + ']/div/div[1]/p[2]/span[2]/text()')).strip("['n\₦]")
                    if lon == "":
                        lon = str(tree.xpath('//div[@class="category-products"]/ul/li[' + str(
                            i) + ']/div/div[1]/span/span/text()')).strip("['n\₦]")
                    lon = float(lon.replace(",", ""))
                    vals['price'] = int(lon)

                    my_list.append(vals)

            else:
                pass

        # Remove unwanted search items and sort items in descending order
        i = set()
        for a, b in enumerate(my_list):
            if not re.search(query, b["title"], re.IGNORECASE):
                i.add(a)
        for no in sorted(i, reverse=True):
            del my_list[no]
        my_list.sort(key=itemgetter('price'))
        print(query1)
        args = {'my_list': my_list, 'query': query}
        return render(request, 'homepage/searchpage.html', args)


