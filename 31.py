""" Модели веб-краулинга

На прошлых занятиях мы рассмотрели несколько способов,
 позволяющих обнаруживать на веб-страницах внутренние и внешние ссылки и затем использовать их для сбора данных с сайта.
  Сегодня мы объединим эти базовые методы и создадим более гибкий краулер сайтов, способный переходить по любой ссылке,
  соответствующей заданному
URL-шаблону.
Веб-краулер такого типа хорошо работает для проектов, в которых нужно собрать данные со всего сайта,
а не только из определенных результатов поиска или списка страниц.
 Этот метод хорошо работает и для страниц, имеющих между собой мало общего или совсем ничего.
В отличие от примера сбора данных со страниц с результатами поиска, рассмотренного выше,
данные типы краулеров не требуют структурированного метода поиска ссылок, поэтому атрибуты,
 описывающие страницу поиска, в объекте Website не нужны. Однако, поскольку краулеру не даны конкретные инструкции о том,
 где и как расположены
ссылки, которые он ищет, требуются некие правила, указывающие на то, какие страницы следует выбрать.
 Для этого мы предоставляем targetPattern — регулярное выражение, описывающее нужные URL — и создаем логическую переменную absoluteUrl:
"""

def a1():
    import re

    import requests
    from bs4 import BeautifulSoup

    class Website:
       def __init__(self, name, url, targetPattern, absoluteUrl, titleTag, bodyTag):
           self.name = name
           self.url = url
           self.targetPattern = targetPattern
           self.absoluteUrl = absoluteUrl
           self.titleTag = titleTag
           self.bodyTag = bodyTag

    class Content:
       def __init__(self, url, title, body):
           self.url = url
           self.title = title
           self.body = body

       def print(self):
           print('URL: {}'.format(self.url))
           print('TITLE: {}'.format(self.title))
           print('BODY:\n{}'.format(self.body))


    class Crawler:
       def __init__(self, site):
           self.site = site
           self.visited = []

       def getPage(self, url):
           try:
               req = requests.get(url)
           except requests.exceptions.RequestException:
               return None
           return BeautifulSoup(req.text, 'html.parser')

       def safeGet(self, pageObj, selector):
           selectedElems = pageObj.select(selector)
           if selectedElems is not None and len(selectedElems) > 0:
               return '\n'.join([elem.get_text() for elem in selectedElems])
           return ''

       def parse(self, url):
           bs = self.getPage(url)
           if bs is not None:
               title = self.safeGet(bs, self.site.titleTag)
               body = self.safeGet(bs, self.site.bodyTag)
               if title != '' and body != '':
                   content = Content(url, title, body)
                   content.print()

       def crawl(self):
           """
           Получить ссылки с начальной страницы
           сайта
           """
           bs = self.getPage(self.site.url)
           targetPages = bs.find_all('a', href=re.compile(self.site.targetPattern))
           for targetPage in targetPages:
               targetPage = targetPage.attrs['href']
               if targetPage not in self.visited:
                   self.visited.append(targetPage)
                   if not self.site.absoluteUrl:
                       targetPage = '{}{}'.format(self.site.url, targetPage)
                   self.parse(targetPage)


    reuters = Website('Reuters', 'https://www.reuters.com', '^(/article/)', False, 'h1',
                     'div.StandardArticleBody_body_1gnLA')
    crawler = Crawler(reuters)
    crawler.crawl()


"""
Еще одно изменение, по сравнению с предыдущими примерами: объект Website (в данном случае переменная  reuters),
 в свою очередь, является свойством объекта Crawler.
  Это позволяет удобно хранить в краулере посещенные страницы (visited), но также означает
необходимость создания для каждого сайта нового краулера,
 вместо того чтобы многократно использовать один и тот же для проверки списка сайтов.
Безотносительно того, хотите ли вы, чтобы веб-краулер не зависел от конкретных сайтов,
 или желаете сделать его атрибутом объекта Crawler, это структурное решение
необходимо принимать в соответствии с конкретными потребностями. В общем случае годится любой из данных подходов.
Следует также отметить: веб-краулер станет получать ссылки с начальной страницы, но не продолжит сбор данных после того,
 как все эти страницы будут пройдены. 

В отличие от сбора данных с заданного множества страниц проверка всех внутренних ссылок на сайте может вызвать проблему, 
поскольку вы никогда точно не знаете, что получите.

К счастью, есть несколько основных способов определения типа страницы.
•По URL — все публикации в блогах могут содержать URL (например, http://example.com/blog/title-ofpost).
• По наличию или отсутствию определенных полей — если на странице есть дата, но нет имени автора,
 то эту страницу можно классифицировать как пресс-релиз. При наличии у
страницы заголовка, основного изображения и цены, но при отсутствии основного контента это может быть страница товара.
• По наличию на странице определенных тегов, идентифицирующих страницу, — теги можно использовать, 
даже если мы не собираем данные внутри них. Веб-краулер может искать элемент наподобие <div id="relatedproducts">, 
чтобы идентифицировать страницу как страницу товара, даже если вас не интересуют сопутствующие товары.

Чтобы отслеживать несколько типов страниц, вам понадобится создать на Python несколько типов объектов страниц.
 Это можно сделать следующими двумя способами.
Если страницы похожи (имеют в целом одинаковые типы контента), то можно добавить к существующему объекту веб-страницы атрибут pageType:
"""

class Website:
   def __init__(self, name, url, titleTag, bodyTag, pageType):
       self.name = name
       self.url = url
       self.titleTag = titleTag
       self.bodyTag = bodyTag
       self.pageType = pageType


"""
Если страницы хранятся в SQL-подобной базе данных, то такой тип структуры страниц указывает 
на вероятное хранение этих страниц в одной таблице,
 в которую будет добавлено поле pageType.
Если же страницы или контент, который вы ищете, заметно различаются (содержат поля разных типов),
 то может понадобиться создать отдельные объекты для каждого типа
страниц. Конечно, все веб-страницы будут иметь нечто общее: URL и, вероятно, имя или заголовок.

"""


class Webpage:
   def __init__(self, name, url, titleTag):
       self.name = name
       self.url = url
       self.titleTag = titleTag



"""Веб-краулер не будет использовать этот объект напрямую, однако на него будут ссылаться типы страниц:
"""


class Product(Website):
    """Содержит информацию для веб-скрапинга
    страницы товара"""

    def __init__(self, name, url, titleTag, productNumberTag, priceTag):
        Website.__init__(self, name, url, titleTag)
        self.productNumberTag = productNumberTag
        self.priceTag = priceTag


class Article(Website):
    """Содержит информацию для веб-скрапинга
    страницы статьи"""

    def __init__(self, name, url, titleTag, bodyTag, dateTag):
        Website.__init__(self, name, url, titleTag)
        self.bodyTag = bodyTag
        self.dateTag = dateTag


"""
Страница Product расширяет базовый класс Website, добавляя к нему атрибуты productNumber и price,
относящиеся лишь к товарам, а класс Article добавляет
атрибуты body и date, которые к товарам неприменимы.
Эти два класса можно использовать, например, для веб-скрапинга интернет-магазина,
на сайте которого содержатся не только товары, но и публикации в блоге или пресс-релизы."""



"""2. Работа с библиотекой Scrapy"""

"""Одна из проблем создания веб-краулеров состоит в том, что часто приходится выполнять одни и те же задачи:
 находить все ссылки на странице, оценивать разницу между внутренними и внешними ссылками, переходить на новые страницы. 
 Эти основные стандартные операции полезно знать и уметь писать с нуля, 
 но библиотека Scrapy способна многое из упомянутого сделать автоматически.
Конечно, Scrapy не читает мысли. Вам по-прежнему необходимо описать шаблоны страниц, указать точку,
 с которой следует начать работу, и построить правила для URL искомых страниц.
  Но и в этих случаях библиотека предоставляет чистую основу для построения четко
структурированного кода.

Для установки:
pip install Scrapy

Инициализация нового “паука”. После установки платформы Scrapy необходимо выполнить небольшую настройку для каждого «паука» 
(spider) — проекта Scrapy, который, как и обычный паук, занимается обходом сети.

 Для удобства мы будем называть «пауком» именно проект Scrapy, а краулером — любую программу,
  которая занимается сбором данных во Всемирной паутине, независимо от того, использует она Scrapy или нет.
Чтобы создать нового «паука» в текущем каталоге, нужно ввести в командной строке следующую команду:
scrapy startproject wikiSpider

В результате в каталоге будет создан новый подкаталог, а в нем — проект под названием wikiSpider. 
Внутри этого каталога находится следующая файловая структура:
scrapy.cfg
wikiSpider
— spiders
— __init.py__
— items.py
— middlewares.py
— pipelines.py
— settings.py
— __init.py__
Поначалу в эти файлы Python записывается код-заглушка, что позволяет быстро создать новый проект «паука».

Чтобы создать веб-краулер, нужно добавить в дочерний каталог wikiSpider новый файл
wikiSpider/wikiSpider/articles.py. Затем в этом файле articles.py нужно написать следующее:"""



import scrapy


class ArticleSpider(scrapy.Spider):
   name = 'article'

   def start_requests(self):
       urls = ['http://en.wikipedia.org/wiki/Python_%28programming_language%29',
               'https://en.wikipedia.org/wiki/Functional_programming', 'https://en.wikipedia.org/wiki/Monty_Python']
       return [scrapy.Request(url=url, callback=self.parse) for url in urls]

   def parse(self, response):
       url = response.url
       title = response.css('h1::text').extract_first()
       print('URL is: {}'.format(url))
       print('Title is: {}'.format(title))


"""
Имя этого класса (ArticleSpider) отличается от имени каталога (wikiSpider), что указывает на следующее: 
данный класс отвечает за просмотр только страниц статей в рамках более широкой категории wikiSpider, 
которую мы впоследствии сможем использовать для поиска других типов страниц.
Для больших сайтов с разными типами контента можно создать отдельные элементы Scrapy для каждого типа 
(публикации в блогах, пресс-релизы, статьи и т.п.). У каждого из этих типов будут свои поля,
 но все они станут работать в одном проекте Scrapy. Имя каждого «паука» должно быть уникальным в рамках проекта.
Следует обратить внимание еще на две важные вещи:
функции start_requests и parse.
Функция start_requests — это предопределенная Scrapy точка входа в программу, используемая для генерации объектов Request,
 которые в Scrapy применяются для сбора
данных с сайта.
Функция parse — это функция обратного вызова, определяемая пользователем, которая передается
 в объект Request с помощью callback=self.parse. Позже мы рассмотрим более мощные трюки,
 которые возможны благодаря функции parse, но пока что она просто выводит заголовок страницы.

Для запуска «паука» article нужно перейти в каталог
wikiSpider/wikiSpider и выполнить следующую команду:
scrapy runspider articles.py

По умолчанию Scrapy выводит довольно подробные данные. Веб-скрапер проходит по трем страницам, указанным в списке urls,
 собирает с них информацию и завершает работу.

«Паук», созданный выше, не очень-то похож на веб-краулер, так как ограничен лишь списком предоставленных ему URL.
 Он не умеет самостоятельно искать новые страницы. 
 Чтобы превратить этого «паука» в полноценный веб-краулер, 
 нужно задействовать предоставляемый Scrapy класс CrawlSpider.
"""


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ArticleSpider(CrawlSpider):
   name = 'articles'
   allowed_domains = ['wikipedia.org']
   start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
   rules = [Rule(LinkExtractor(allow=r'.*'), callback='parse_items', follow=True)]

   def parse_items(self, response):
       url = response.url
       title = response.css('h1::text').extract_first()
       text = response.xpath('//div[@id="mwcontent-text"]//text()').extract()
       lastUpdated = response.css('li#footerinfo-lastmod::text').extract_first()
       lastUpdated = lastUpdated.replace('This page was last edited on ', '')
       print('URL is: {}'.format(url))
       print('title is: {} '.format(title))
       print('text is: {}'.format(text))
       print('Last updated:{}'.format(lastUpdated))


"""######################################################################################################### na sled zanutie
Этот новый «паук» ArticleSpider является наследником класса CrawlSpider. 
Вместо функции start_requests он предоставляет списки start_urls и allowed_domains,
 которые сообщают «пауку», с чего начать обход сети и следует ли переходить по ссылке или игнорировать ее,
в зависимости от имени домена.

Предоставляется и список rules, в котором содержатся дальнейшие инструкции: по каким ссылкам переходить,
а какие — игнорировать (в данном случае с помощью регулярного выражения .* мы разрешаем переходить по всем URL).
Помимо заголовка и URL на каждой странице, здесь добавлено извлечение еще пары элементов.
С помощью селектора XPath извлекается текстовый контент каждой страницы.
XPath часто используется для извлечения текста, включая содержимое дочерних тегов (например, тега <a>,
расположенного внутри текстового блока). Если для этого использовать CSS-селектор, то контент всех дочерних тегов будет игнорироваться.
Анализируется также строка с датой последнего изменения из нижнего колонтитула страницы, которая сохраняется в переменной lastUpdated.

Чтобы запустить этот пример, нужно перейти в каталог wikiSpider/wikiSpider и выполнить следующую команду:
scrapy runspider articles.py

При запуске этот «паук» проходит по сайту wikipedia.org, переходя по всем ссылкам домена wikipedia.org,
 выводя заголовки страниц и игнорируя все внешние ссылки (ведущие на другие сайты)

Пока данный веб-краулер работает неплохо, однако у него есть несколько ограничений.
 Вместо того чтобы посещать только страницы статей «Википедии», он вполне может
переходить на страницы, не относящиеся к статьям.

Рассмотрим внимательнее следующую строку кода, где используются объекты Scrapy Rule и LinkExtractor:
rules = [Rule(LinkExtractor(allow=r'.*'),callback='parse_items',follow=True)]
В данной строке содержится список объектов Scrapy Rule, определяющих правила, по которым фильтруются все найденные ссылки. 
При наличии нескольких правил каждая
ссылка проверяется на соответствие им в порядке их перечисления. Первое подходящее правило — то, 
которое используется для определения способа обработки ссылки. Если
ссылка не соответствует ни одному из правил, то игнорируется.
Правило может быть описано следующими четырьмя аргументами:
•link_extractor — единственный обязательный аргумент —объект LinkExtractor;
• callback — функция обратного вызова, которая должна использоваться для анализа контента страницы;
• cb_kwargs — словарь аргументов, передаваемых в функцию обратного вызова. Имеет вид
{arg_name1:arg_value1,arg_name2:arg_value2} и может быть удобным инструментом 
для многократного использования одних и тех же функций синтаксического анализа в незначительно различающихся задачах;
• follow — указывает на то, хотите ли вы, чтобы веб-краулер обработал также страницы по ссылкам, найденным на данной странице.
 Если функция обратного вызова не указана, то по умолчанию используется значение True (в конце концов,
  при отсутствии действий с этой страницей логично предположить,
   что вы по крайней мере захотите применить ее для продолжения сбора данных с сайта).
    Если предусмотрена функция обратного вызова, то по умолчанию используется значение False.

Учитель:  Простой класс LinkExtractor предназначен исключительно для распознавания и возврата ссылок,
 обнаруженных в HTML-контенте страницы на основе предоставленных этому классу правил. Имеет ряд аргументов,
  которые можно использовать для того, чтобы принимать или отклонять ссылки на основе CSS-селекторов и XPath,
   тегов (можно искать ссылки не только в тегах <a>!), доменов и др. От класса LinkExtractor можно унаследовать свой,
    в котором можно добавить нужные аргументы.

Несмотря на всю гибкость свойств класса LinkExtractor, самыми распространенными аргументами, которые вы, скорее всего,
 будете использовать, являются следующие:
•allow — разрешить проверку всех ссылок, соответствующих заданному регулярному выражению;
• deny — запретить проверку всех ссылок, соответствующих заданному регулярному выражению.
Используя два отдельных класса Rule и LinkExtractor с общей функцией синтаксического анализа, можно создать «паука», 
который бы собирал данные в «Википедии», идентифицируя все страницы статей и помечая остальные страницы флагом (articleMoreRules.py):
"""


from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ArticleSpider(CrawlSpider):
   name = 'articles'
   allowed_domains = ['wikipedia.org']
   start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
   rules = [Rule(LinkExtractor(allow='^(/wiki/)((?!:).)*$'), callback='parse_items', follow=True,
                 cb_kwargs={'is_article': True}),
            Rule(LinkExtractor(allow='.*'), callback='parse_items', cb_kwargs={'is_article': False})]

   def parse_items(self, response, is_article):
       print(response.url)
       title = response.css('h1::text').extract_first()
       if is_article:
           url = response.url
           text = response.xpath('//div[@id="mw-content-text"]''//text()').extract()
           lastUpdated = response.css('li#footer-info-lastmod''::text').extract_first()
           lastUpdated = lastUpdated.replace('This page was ''last edited on ', '')
           print('Title is: {}'.format(title))
           print('title is: {}'.format(title))
           print('text is: {}'.format(text))
       else:
           print('This is not an article:{}'.format(title))


"""
Правила применяются к каждой ссылке в том порядке, в котором они представлены в списке. 
Все страницы статей (страницы, URL которых начинается с /wiki/ и не содержит двоеточий) передаются в функцию parse_items 
с аргументом is_article=True. Все остальные ссылки (не на статьи) передаются в функцию parse_items с аргументом is_article=False.
Конечно, если вы хотите собирать информацию только со страниц статей и игнорировать все остальные, 
то такой подход был бы непрактичным. Намного проще игнорировать все
страницы, которые не соответствуют структуре URL страниц со статьями, 
и вообще не определять второе правило (и переменную is_article). Однако бывают случаи, когда
подобный подход может быть полезен — например, если информация из URL или данные, собранные при краулинге,
 влияют на способ синтаксического анализа страницы.

Мы уже рассмотрели множество способов поиска, синтаксического анализа и краулинга сайтов с помощью Scrapy,
 однако эта платформа также предоставляет полезные инструменты для упорядочения собранных элементов
  и их хранения в созданных пользователем объектах с четко определенными полями.
Чтобы упорядочить всю собираемую информацию, нужно создать объект Article.
 Определим этот новый элемент с именем Article в файле items.py.
"""


import scrapy

class Article(scrapy.Item):
   url = scrapy.Field()
   title = scrapy.Field()
   text = scrapy.Field()
   lastUpdated = scrapy.Field()

"""
Мы определили три поля, в которые будут собираться данные с каждой страницы: заголовок, URL и дату последнего редактирования страницы.

Если мы собираем данные для страниц разных типов, то нужно определить каждый тип как отдельный класс в items.py. 
Если собираемые объекты Item имеют очень большие размеры или если мы захотим перенести в их Item дополнительные
функции синтаксического анализа, то можно разместить каждый такой объект в отдельном файле. Однако,
поскольку наши объекты Item невелики, будем хранить их в одном файле.
Обратите внимание на изменения, которые были внесены в класс ArticleSpider в файле articleItems.py, 
чтобы можно было создать новый объект Article:
"""

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article


class ArticleSpider(CrawlSpider):
   name = 'articleItems'
   allowed_domains = ['wikipedia.org']
   start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
   rules = [Rule(LinkExtractor(allow='(/wiki/)((?!:).)*$'), callback='parse_items', follow=True), ]

   def parse_items(self, response):
       article = Article()
       article['url'] = response.url
       article['title'] = response.css('h1::text').extract_first()
       article['text'] = response.xpath('//div[@id="mw-contenttext"]//text()').extract()
       lastUpdated = response.css('li#footerinfo-lastmod::text').extract_first()
       article['lastUpdated'] = lastUpdated.replace('This page was last edited on ', '')
       return article


"""
Использование объектов Item в Scrapy не только обеспечивает хорошую упорядоченность кода и представление объектов в удобно читаемом виде.
 У объектов Item есть множество инструментов для вывода и обработки данных.

В Scrapy объекты Item позволяют определить, какие фрагменты информации из посещенных страниц следует сохранять.
 Scrapy может сохранять эту информацию различными способами, такими как файлы форматов CSV, JSON или XML, с помощью следующих команд:
scrapy runspider articleItems.py -o articles.csv -t csv
scrapy runspider articleItems.py -o articles.json -t json
scrapy runspider articleItems.py -o articles.xml -t xml

Каждая из этих команд запускает веб-скрапер articleItems и записывает полученные данные в заданном файле в указанном формате.
 Если такого файла еще не существует, то он будет создан.
Вы могли заметить, что в «пауке» ArticleSpider, созданном в предыдущих примерах,
 переменная текстовых данных представляет собой не одну строку, а их список. Каждая
строка в нем соответствует тексту, расположенному в одном из элементов HTML,
 тогда как контент тега <div id="mwcontent-text">, из которого мы собираем текстовые данные,
представляет собой множество дочерних элементов. Scrapy хорошо управляет этими усложненными значениями. 
Например, при сохранении данных в формате CSV списки преобразуются в строки, а запятые экранируются, 
так что список текстовых фрагментов в формате CSV занимает одну ячейку.
В XML каждый элемент этого списка сохраняется в отдельном дочернем теге:
<items>
<item>
<url>https://en.wikipedia.org/wiki/Benevole
nt_dictator_for_life</url>
<title>Benevolent dictator for life</title>
<text>
<value>For the political term, see
</value>
<value>Benevolent dictatorship</value>
...
</text>
<lastUpdated> 13 December 2017, at 09:26.
</lastUpdated>
</item>
....
В формате JSON списки так и сохраняются в виде списков. И конечно же, мы можем обрабатывать объекты Item самостоятельно,
 записывая их в файл или базу данных любым
удобным способом, просто добавив соответствующий код в функцию синтаксического анализа в веб-краулере.
"""