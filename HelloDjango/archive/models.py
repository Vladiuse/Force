from statistics import mode
from django.db import models
import requests as req
from .screen_maker import load_screenshot
from PIL import Image
from pytils import translit
import random as r
from django.conf import settings

# Create your models here.

class Site(models.Model):
    SITE_DOMAIN = 'http://vladiuse.beget.tech/'
    SITE_URL = 'lands_json.php'

    name = models.CharField(max_length=100, verbose_name='Название Сайта')
    description = models.CharField(max_length=200, verbose_name='Описание сайта', blank=True)
    dir_path = models.CharField(max_length=100, verbose_name='Пусть к сайту', unique=True)
    image = models.ImageField(blank=False)
    category = models.ForeignKey('SiteCategoty',
                                 on_delete=models.SET_NULL,
                                 verbose_name='Категория сайта',
                                 null=True,
                                 blank=True,
                                 )

    languege = models.ForeignKey('Languege',
                                  on_delete=models.SET_NULL,
                                  verbose_name='Язык сайта',
                                  null=True, 
                                  blank=True,
    )
    cataloge = models.ForeignKey('Cataloge',
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
    )
    tag = models.ForeignKey('Tag',
                             on_delete=models.SET_NULL, 
                             null=True, 
                             blank=True
                             )



    def get_sites_list(self):
        url = Site.SITE_DOMAIN + Site.SITE_URL
        res = req.get(url)
        data = res.json()
        dirs = list()
        for file in data:
            if '.' not in file:
                dirs.append(file)
        return dirs

    def update_sites_models(self):
        sites = self.get_sites_list()
        sites_models = Site.objects.all()
        sites_models_dirs = [site.dir_path for site in sites_models]
        # список на удаление
        sites_to_dell = set(sites_models_dirs) - set(sites)
        for s in sites_to_dell:
            site = Site.objects.get(dir_path=s)
            site.delete()
        # список на добавление
        site_to_add = set(sites) - set(sites_models_dirs)
        for s_dir_name in site_to_add:
            # load_screenshot(
            #     url=Site.SITE_DOMAIN + s_dir_name,
            #     path_to_save=f'./media/',
            #     image_name=f'{s_dir_name}.png'
            # )
            new_site = Site(name=s_dir_name, dir_path=s_dir_name)
            new_site.save()
            new_site.load_screenshot()
            new_site.fix_image_size()

    def get_site_url(self):
        return f'{self.SITE_DOMAIN}{self.dir_path}'

    def load_screenshot(self):
        image_name = translit.slugify(str(self.dir_path))
        image_name += str(r.randint(10,99))
        image_name = image_name + '.png'
        load_screenshot(
            url=Site.SITE_DOMAIN + str(self.dir_path),
            path_to_save=settings.MEDIA_ROOT+'/',
            image_name=image_name,
        )
        self.image = image_name
        self.save()

    def fix_image_size(self):
        # super().save()  # saving image first
        img = Image.open(self.image.path) # Open image using self
        if img.height > 700 or img.width > 500:
            new_img = (240, 180)
            img.thumbnail(new_img)
            img.save(self.image.path)  # saving image at the same path

class SiteCategoty(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название категории')

    def __str__(self):
        return self.name


class Languege(models.Model):

    short = models.CharField(max_length=2, verbose_name='Короткое название')
    full = models.CharField(max_length=20, verbose_name='полное название')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.short} - {self.full}'


class Cataloge(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название каталога')
    category = models.ForeignKey(SiteCategoty, on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name


class Tag(models.Model):
    text = models.CharField(max_length=20, verbose_name='Текст')
    smile = models.CharField(max_length=10, verbose_name='Смайлик', blank=True, null=False)
    html_class = models.CharField(max_length=10, verbose_name='Класс HTML')

    def __str__(self):
        return self.text


class Test(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)