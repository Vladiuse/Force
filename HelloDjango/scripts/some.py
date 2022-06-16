from archive.models import Site, SiteCategoty, Siteremote, Cataloge, Languege, Siteremote
sites = Siteremote.objects.filter(name='KMA')
for s in sites:
    s.load_screenshot()
# print(Site.objects.get(path="https://blog-feed.org/prostaline-vesti/?ufl=14293"))
