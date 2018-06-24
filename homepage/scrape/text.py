import nogil

vals=[
      "http://example.com",
	  "https://curl.haxx.se/",
      "http://example.com",
      "www.haxx.se",
      "www.haxx.se"]
      "http://example.com",
	  "https://curl.haxx.se/",
      "http://example.com",
      "www.haxx.se",
      "www.haxx.se",
      "http://example.com",
	  "https://curl.haxx.se/",
      "http://example.com",
      "www.haxx.se",
      "www.haxx.se",
      "http://example.com",
	  "https://curl.haxx.se/",
      "http://example.com",
      "www.haxx.se",
      "www.haxx.se"

]
resp=nogil.greet(vals)


urls=[
    'https://www.konga.com/v1/json/search?q=laptop&from=9',
    'https://www.jumia.com.ng/catalog/?q=laptop&page=1',
    'https://www.konga.com/v1/json/search?q=laptop&from=1',
    'https://www.konga.com/v1/json/search?q=laptop&from=18',
    'https://www.konga.com/v1/json/search?q=laptop&from=27',
    'https://www.konga.com/v1/json/search?q=laptop&from=36',
    'https://www.jumia.com.ng/catalog/?q=laptop&page=2',
]


        urls = [url.replace('values', query) for url in urls]

        #rs = (grequests.get(u) for u in urls)
        #response = (grequests.map(rs))
        response=nogil.greet(urls)
        my_list = []
        for data in response:
            if 'konga' in data:
                tree = json.loads(data)
                list1 = tree['data']
                for l, m in enumerate(list1['products']):
                    vals = {}
                    vals['title'] = list1['products'][l]['fields']['name']
                    vals['link'] = 'https://www.konga.com/'+list1['products'][l]['fields']['url_key']
                    vals['image'] = 'https://images.konga.com/v2/media/catalog/product'+list1['products'][l]['fields']['image_thumbnail_path']+'?scale_mode=aspect_fit&h=250&w=250'
                    value = list1['products'][l]['fields']['price']

                    vals['price'] = value
                    my_list.append(vals)
    
            elif 'jumia' in data:
                tree = etree.HTML(data)
                list1 = tree.xpath('/html/body/main/section/section[2]/div')
                for y, z in enumerate(list1, 1):
                    vals = {}
                    vals['title'] = tree.xpath('/html/body/main/section/section[2]/div['+str(y)+']/a/h2/span[2]/text()')[0]
                    vals['link'] = tree.xpath('/html/body/main/section/section[2]/div[' + str(y)+']/a/@href')[0]
                    vals['image'] = tree.xpath('/html/body/main/section/section[2]/div[' + str(y) 
                                +']/a/div[2]/img/@data-src')[0]+'?scale_mode=aspect_fit&h=250&w=250'

                    value = re.sub("[^0-9]", "", str(tree.xpath('/html/body/main/section/section[2]/div['+str(y)
                                +']/a/div[3]/span/span[1]/span[2]/text()')))

                    if len(value) < 2:
                        vals['title'] = 'none'
                    else:
                        men = int(value)
                    vals['price'] = int(men)

                    my_list.append(vals)

            else:
                pass
        
        list1=Product.objects.filter(title__icontains=query).values()
        for value in list1:
            vals={}
            vals['title']=value["title"]
            vals['link'] = 'archive/'+str(value["id"])
            vals['price'] = value["price"]
            vals['image'] = '/media/'+value["preview"]+'?scale_mode=aspect_fit&h=250&w=250'

            my_list.append(vals)
        
        i = set()
        for a, b in enumerate(my_list):
            if not re.search(query, b["title"], re.IGNORECASE):
                i.add(a)
        for no in sorted(i, reverse=True):
            del my_list[no]
        my_list.sort(key=itemgetter('price'))
        return render(request, 'scratch/value.html', {'my_list': my_list, 'query': query})

