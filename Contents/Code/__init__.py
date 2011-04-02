THE_WB_ROOT       = 'http://www.thewb.com'
THE_WB_SHOWS_LIST = 'http://www.thewb.com/shows/full-episodes'

ART  = 'art-default.jpg'
ICON = 'icon-default.jpg'

####################################################################################################
def Start():
  Plugin.AddPrefixHandler('/video/thewb', MainMenu, 'The WB', ICON, ART)
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

  MediaContainer.art = R(ART)
  MediaContainer.title1 = 'The WB'
  MediaContainer.viewGroup = 'InfoList'

  DirectoryItem.thumb = R(ICON)
  WebVideoItem.thumb = R(ICON)

  HTTP.CacheTime = CACHE_1HOUR
  HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13'

####################################################################################################
def MainMenu():
  dir = MediaContainer()
  content = HTML.ElementFromURL(THE_WB_SHOWS_LIST)

  for item in content.xpath('//div[@id="show-directory"]//div/div/ul/li'):
    title = item.xpath('./a')[0].text
    link = THE_WB_ROOT + item.xpath('./a')[0].get('href')
    dir.Append(Function(DirectoryItem(Eplist, title=title), pageUrl=link))

  return dir

####################################################################################################
def Eplist(sender, pageUrl):
  dir = MediaContainer(title2=sender.itemTitle)
  content = HTML.ElementFromURL(pageUrl)

  for item in content.xpath('//li[@id="full_ep_car1"]//div/div[@class="overlay_thumb_area"]'):
    title = item.xpath('./a/img')[0].get('alt')
    link = THE_WB_ROOT + item.xpath('./a')[0].get('href')
    thumb = item.xpath('./a/img')[0].get('src')
    dir.Append(WebVideoItem(url=link, title=title))

  return dir
