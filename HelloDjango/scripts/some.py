from archive.models import Site, SiteCategoty, Siteremote, Cataloge, Languege, Siteremote
with open('/home/vlad/PycharmProjects/Force/HelloDjango/scripts/Lands SPY - KMA.csv', ) as file:
    count = 0
    for line in file:

        dir_name, id, name, url, lang, cat, some, category_id = line.split(',')
        desc = lang
        if lang.count('(') == 1:
            lang = lang[lang.find('(')+ 1:lang.find(')')]
        try:
            site_category = SiteCategoty.objects.get(pk=category_id)
        except:
            print(category_id, 'категория не найдена')
            site_category = None
        try:
            cataloge = Cataloge.objects.get(name=dir_name)
        except:
            cataloge = Cataloge(name=name, category=site_category)
            cataloge.save()
        try:
            lang = Languege.objects.get(short=lang)
        except:
            print(lang, 'lang not fotud')
            lang = None

        remote_site = Siteremote(
            name=name,
            path=url,
            description=desc,
            languege=lang,
            cataloge=cataloge,
            category=site_category,
        )
        count += 1
        remote_site.save()
        remote_site.load_screenshot()
        print(dir_name, name)
    print(count)
