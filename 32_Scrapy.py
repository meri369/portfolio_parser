'''Методические указания
Урок 32.1 Работа с библиотекой Scrapy
Задачи урока:
Работа с библиотекой Scrapy

0. Подготовка к уроку

До начала урока преподавателю необходимо:
Просмотреть, как ученики справились с домашним заданием
Прочитать методичку

1. Работа с библиотекой Scrapy

Учитель:  Несмотря на то что Scrapy является однопоточной библиотекой, она способна выполнять и обрабатывать несколько запросов асинхронно
благодаря чему работает
быстрее, чем веб-скраперы, рассмотренные ранее.
Впрочем, когда речь идет о веб-скрапинге, быстрее не всегда значит лучше.
Веб-сервер сайта, на котором выполняется веб-скрапинг, должен обработать каждый ваш запрос.

Важно трезво оценивать, насколько приемлема создаваемая вами нагрузка на сервер,
поскольку многие сайты имеют возможность и желание заблокировать то, что посчитают злостным веб-скрапингом.


С учетом всего этого использование динамического конвейера в Scrapy позволяет еще более повысить скорость работы веб-скрапера,
так как вся обработка данных будет
выполняться в то время, пока веб-скрапер ожидает ответа на запросы,
вместо того чтобы дожидаться окончания обработки данных и только потом выполнять очередной запрос.
Такой тип оптимизации иногда бывает просто необходим — если обработка данных занимает много времени или требуется выполнить вычисления,
создающие значительную нагрузку на процессор.
Чтобы создать динамический конвейер,перейдем к файлу settings.py.
В нем содержатся следующие строки кода, заблокированные символами комментариев:
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
# 'wikiSpider.pipelines.WikispiderPipeline':
300,
#}

Уберем символы комментариев из последних трех строк и получим следующее:
ITEM_PIPELINES = {
'wikiSpider.pipelines.WikispiderPipeline':
300,
}

Таким образом, мы создали класс Python wikiSpider.pipelines.Wikispider Pipeline, который
будет служить для обработки данных, а также указали целое число,
соответствующее порядку запуска конвейера при наличии нескольких классов обработк. Здесь можно
использовать любое целое число, однако обычно это цифры от 0 до 1000. Конвейер запускается в порядке возрастания.
Теперь нужно добавить класс конвейера в «паука» и переписать нашего исходного «паука» таким образом, чтобы он собирал данные,
а конвейер выполнял нелегкую задачу по их
обработке. Было бы заманчиво создать в исходном «пауке» метод parse_items, который бы возвращал ответ,
и позволить конвейеру создавать объект Article:'''

def parse_items(self, response):
    return response

'''
Однако фреймворк Scrapy такого не допускает: должен возвращаться объект Item (или Article, который является расширением Item).
Итак, сейчас назначение parse_items
состоит в том, чтобы извлечь необработанные данные и обработать по минимуму — лишь бы можно было передать их в конвейер
'''
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article


class ArticleSpider(CrawlSpider):
   name = 'articlePipelines'
   allowed_domains = ['wikipedia.org']
   start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
   rules = [Rule(LinkExtractor(allow='(/wiki/)((?!:).)*$'), callback='parse_items', follow=True), ]

   def parse_items(self, response):
       article = Article()
       article['url'] = response.url
       article['title'] = response.css('h1::text').extract_first()
       article['text'] = response.xpath('//div[@id="mw-contenttext"]//text()').extract()
       article['lastUpdated'] = response.css('li#''footer-infolastmod::text').extract_first()
       return article




'''Конечно, теперь нужно связать файл pipelines.py с измененным «пауком», добавив конвейер.
При первоначальной инициализации проекта Scrapy был создан
файл wikiSpider/wikiSpider/pipelines.py:
# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/itempipeline.html'''
class WikispiderPipeline(object):
    def process_item(self, item, spider):
        return item

'''Этот класс-заглушку следует заменить нашим новым кодом конвейера.
В предыдущих примерах мы собирали два поля в необработанном формате — lastUpdated (плохо
отформатированный строковый объект, представляющий дату) и text («грязный» массив строковых фрагментов),
— но для них можно использовать дополнительную обработку.

Вместо кода-заглушки в wikiSpider/wikiSpider/pipelines.py поставим следующий код:
'''
from datetime import datetime
from wikiSpider.items import Article
from string import whitespace


class WikispiderPipeline(object):
   def process_item(self, article, spider):
       dateStr = article['lastUpdated']
       article['lastUpdated'] = article['lastUpdated'].replace('This page was last editedon', '')
       article['lastUpdated'] = article['lastUpdated'].strip()
       article['lastUpdated'] = datetime.strptime(article['lastUpdated'], '%d %B %Y, %H:%M.')
       article['text'] = [line for line in article['text'] if line not in whitespace]
       article['text'] = ''.join(article['text'])
       return article



'''У класса WikispiderPipeline есть метод process_item, который принимает объект Article,
преобразует строку lastUpdated в объект datetime Python, очищает текст и трансформирует его из списка строк в одну строку.
Метод process_item является обязательным для любого класса конвейера.
В Scrapy этот метод используется для асинхронной передачи объектов Item, собранных «пауком».
Анализируемый объект Article, который возвращается в данном случае, будет сохранен или выведен Scrapy,
если, например, мы решим выводить элементы в формате JSON или CSV.

Теперь можно выбрать, где обрабатывать данные: в методе parse_items в «пауке» или в методе process_items в конвейере.
В файле settings.py можно создать несколько конвейеров, каждый из которых будет выполнять свою задачу.
Однако Scrapy передает все элементы, независимо от их типа,
во все конвейеры по порядку.
Синтаксический анализ элементов конкретных типов лучше реализовать в «пауке»
и только потом передавать данные в конвейер. Но если этот
анализ занимает много времени, то можно переместить его в конвейер (где он будет выполняться асинхронно) и добавить проверку типа элемента:
'''
def process_item(self, item, spider):
   if isinstance(item, Article):
       # обработка объектов Article




'''При написании проектов Scrapy, особенно крупных, важно учитывать, где и какую обработку вы собираетесь делать.

Отладочная информация, генерируемая Scrapy, бывает полезна, однако, как вы могли заметить,
часто чересчур многословна. Вы можете легко настроить уровень ведения
журнала, добавив в файл settings.py проекта Scrapy следующую строку:
LOG_LEVEL = 'ERROR'
В Scrapy принята стандартная иерархия уровней ведения журнала:
•CRITICAL;
• ERROR;
• WARNING;
• DEBUG;
• INFO.
В случае уровня ведения журнала ERROR будут отображаться только события типов CRITICAL и ERROR;
при ведении журнала на уровне INFO будут отображаться все события и т.д.
Кроме управления ведением журнала через файл settings.py, также можно управлять тем,
куда попадают записи из командной строки. Чтобы они выводились не на терминал, а в отдельный файл журнала,
нужно указать этот файл при запуске Scrapy из командной строки:
scrapy crawl articles -s LOG_FILE=wiki.log

Эта команда создает в текущем каталоге новый файл журнала (если такого еще нет) и делает в него все журнальные записи,
оставляя терминал только для данных, выводимых операторами Python, которые вы сами добавили в программу.

Учитель:  Давайте теперь рассмотрим еще один паук для сайта https://quotes.toscrape.com/ и постараемся его подробнее разобрать.

Для начала создаем новый проект с помощью команды
scrapy startproject quotes

Теперь перейдем в папку spiders проекта и создадим там новый файл quotes_spider.py.'''
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
   name = "quotes"

   def start_requests(self):
       urls = [
           'https://quotes.toscrape.com/page/1/',
           'https://quotes.toscrape.com/page/2/',
       ]
       for url in urls:
           yield scrapy.Request(url=url, callback=self.parse)

   def parse(self, response):
       page = response.url.split("/")[-2]
       filename = f'quotes-{page}.html'
       Path(filename).write_bytes(response.body)
       self.log(f'Сохраняем файл {filename}')




'''Наш паук является подклассом scrapy.Spider и определяет некоторые атрибуты и методы:
name: идентифицирует Паука. Оно должно быть уникальным в пределах проекта, то есть вы не можете задать одно и то же имя для разных Пауков.
start_requests(): должен возвращать итерацию запросов (вы можете вернуть список запросов или написать функцию-генератор),
с которых начинает сканировать Spider. Последующие запросы будут генерироваться последовательно из этих первоначальных запросов.
parse(): метод, который будет вызываться для обработки ответа, загруженного для каждого из сделанных запросов.
Параметр ответа является экземпляром, который содержит содержимое страницы и имеет дополнительные полезные методы для его обработки.

Метод parse() обычно анализирует ответ, извлекая очищенные данные в виде словарей,
а также находит новые URL-адреса для отслеживания и создает Request из них новые запросы.

Запустим нашего паука. Для этого не забудем перейти в основной каталог нашего паука и вводим команду
scrapy crawl quotes

Результат
…
{'BOT_NAME': 'quotes',
 'FEED_EXPORT_ENCODING': 'utf-8',
 'NEWSPIDER_MODULE': 'quotes.spiders',
 'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
 'ROBOTSTXT_OBEY': True,
…

После выполнения кода у нас появились 2 новых html файла с содержанием указанных нами ранее страниц.

Что же у нас в этот момент происходит скрыто от наших глаз. Scrapy планирует объекты, возвращаемые методом start_requests паука..
Получив ответ для каждого из них, он создает экземпляры Response объектов и вызывает метод обратного вызова,
связанный с запросом (в данном случае метод parse), передавая ответ в качестве аргумента.

Вместо реализации метода start_requests(), который генерирует Request объекты из URL-адресов,
можно просто определить start_urls атрибут класса со списком URL-адресов.
Затем этот список будет использоваться реализацией start_requests() по умолчанию для создания первоначальных запросов паука:
'''
from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
   name = "quotes"
   start_urls = [
       'https://quotes.toscrape.com/page/1/',
       'https://quotes.toscrape.com/page/2/',
   ]

   def parse(self, response):
       page = response.url.split("/")[-2]
       filename = f'quotes-{page}.html'
       Path(filename).write_bytes(response.body)






'''Метод parse() будет вызываться для обработки каждого запроса этих URL-адресов, даже если мы явно не указали Scrapy делать это.
Это происходит потому, что parse() это метод обратного вызова Scrapy по умолчанию,
который вызывается для запросов без явно назначенного обратного вызова.

Также мы с вами можем извлекать данные с помощью селекторов CSS. 
Давайте переделаем наш код под данный вариант'''
import scrapy


class QuotesSpider(scrapy.Spider):
   name = "quotes"
   start_urls = [
       'http://quotes.toscrape.com/'
   ]

   def parse(self, response):
       for quote in response.css("div.quote"):
           print({
               'text': quote.css("span.text::text").extract_first(),
               'author': quote.css("small.author::text").extract_first(),
               'tags': quote.css("div.tags > a.tag::text").extract()
           })


С помощью XPATH
import scrapy


class QuotesSpider(scrapy.Spider):
   name = "quotes"
   start_urls = [
       'http://quotes.toscrape.com/'
   ]

   def parse(self, response):
       for quote in response.xpath('//div[@class="quote"]'):
           print({
               'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
               'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
               'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
           })




'''В данном случае мы выводим все в консоль, но на практике конечно же, вы наверное будете сохранять это в отдельный файл.
Поэтому давайте переделаем немного наш код, а именно вместо print мы
 поставим yield'''
import scrapy


class QuotesSpider(scrapy.Spider):
   name = "quotes"
   start_urls = [
       'https://quotes.toscrape.com/page/1/',
       'https://quotes.toscrape.com/page/2/',
   ]

   def parse(self, response):
       for quote in response.css('div.quote'):
           yield {
               'text': quote.css('span.text::text').get(),
               'author': quote.css('small.author::text').get(),
               'tags': quote.css('div.tags a.tag::text').getall(),
           }




'''Теперь запишем наш результат в json файл командой
scrapy crawl quotes -O quotes.json

Отлично. Теперь переделаем код так, чтобы он перебирал все страницы с сайта'''
import scrapy


class QuotesSpider(scrapy.Spider):
   name = "quotes"
   start_urls = [
       'https://quotes.toscrape.com/page/1/',
   ]

   def parse(self, response):
       for quote in response.css('div.quote'):
           yield {
               'text': quote.css('span.text::text').get(),
               'author': quote.css('small.author::text').get(),
               'tags': quote.css('div.tags a.tag::text').getall(),
           }

       next_page = response.css('li.next a::attr(href)').get()
       if next_page is not None:
           next_page = response.urljoin(next_page)
           yield scrapy.Request(next_page, callback=self.parse)




'''Теперь, после извлечения данных, метод parse() ищет ссылку на следующую страницу,
строит полный абсолютный URL-адрес с помощью метода urljoin()(поскольку ссылки могут быть относительными)
и выдает новый запрос на следующую страницу, регистрируя себя как обратный вызов для обработки.
извлечение данных для следующей страницы и продолжение сканирования всех страниц.

Здесь мы видим механизм следующих ссылок Scrapy: когда вы возвращаете запрос в методе обратного вызова,
Scrapy запланирует отправку этого запроса и зарегистрирует метод обратного вызова, который будет выполнен после завершения этого запроса.
Используя это, мы можем создавать сложные поисковые роботы,
которые переходят по ссылкам в соответствии с определенными вами правилами и извлекают различные типы данных в
зависимости от посещаемой страницы.

В нашем примере он создает своего рода цикл, переходя по всем ссылкам на следующую страницу,
пока не найдет ни одной — удобно для сканирования блогов, форумов и других сайтов с нумерацией страниц.

Давайте рассмотрим еще один пример.'''
import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }




'''и запустим
 scrapy crawl author -O quotes.json

Этот паук запустится с главной страницы, он будет переходить по всем ссылкам на страницы авторов,
вызывая обратный вызов parse_author для каждого из них, а также ссылки пагинации с обратным вызовом parse.

Обратный вызов parse_author определяет вспомогательную функцию для извлечения и очистки данных из запроса CSS
и выдает словарь Python с данными автора.
Вы можете предоставить аргументы командной строки своим паукам, используя опцию -a при их запуске:
scrapy crawl quotes -O quotes-humor.json -a tag=humor

Эти аргументы передаются методу  __init__ паука и по умолчанию становятся атрибутами паука.
'''

import scrapy


class QuotesSpider(scrapy.Spider):
   name = "quotes"

   def start_requests(self):
       url = 'https://quotes.toscrape.com/'
       tag = getattr(self, 'tag', None)
       if tag is not None:
           url = url + 'tag/' + tag
       yield scrapy.Request(url, self.parse)

   def parse(self, response):
       for quote in response.css('div.quote'):
           yield {
               'text': quote.css('span.text::text').get(),
               'author': quote.css('small.author::text').get(),
           }

       next_page = response.css('li.next a::attr(href)').get()
       if next_page is not None:
           yield response.follow(next_page, self.parse)




'''Если мы передадим tag=humor, как аргумент этому пауку, мы заметим, что он будет посещать только URL-адреса с тегом humor.

Дополнительно
Если на уроке остается время, то ученикам можно предложить начать прорешивать домашнее задание.

Домашняя работа
Реализовать в парсере из прошлого домашнего задания вывод не в консоль, в журнал scrapy, а также настроить отладочную информацию на Error

'''




