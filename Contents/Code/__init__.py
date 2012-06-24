RE_EP_DETAILS = Regex('Season (?P<season>[0-9]+): Ep\. (?P<episode>[0-9]+) \((?P<minutes>[0-9]{1,2}):(?P<seconds>[0-9]{2})\)')
RE_DURATION = Regex('\((?P<minutes>[0-9]{1,2}):(?P<seconds>[0-9]{2})\)')

THE_WB_ROOT       = 'http://www.thewb.com'
THE_WB_SHOWS_LIST = 'http://www.thewb.com/shows/full-episodes'

ART  = 'art-default.jpg'
ICON = 'icon-default.jpg'

####################################################################################################
def Start():
    Plugin.AddPrefixHandler('/video/thewb', MainMenu, 'The WB', ICON, ART)

    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = 'The WB'

    DirectoryObject.thumb = R(ICON)

    HTTP.CacheTime = CACHE_1HOUR
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13'

####################################################################################################
def MainMenu():
    oc = ObjectContainer()
    content = HTML.ElementFromURL(THE_WB_SHOWS_LIST)

    for item in content.xpath('//div[@id="show-directory"]//div/div/ul/li'):
        title = item.xpath('./a')[0].text
        link = THE_WB_ROOT + item.xpath('./a')[0].get('href')
        oc.add(DirectoryObject(key=Callback(EpList, pageUrl=link, title=title), title=title))

    return oc

####################################################################################################
def EpList(pageUrl, title):
    oc = ObjectContainer(title2=title)
    content = HTML.ElementFromURL(pageUrl)

    for item in content.xpath('//li[@id="full_ep_car1"]//div[@class="overlay"]'):
        video_title = item.xpath('.//img')[0].get('alt')
        if video_title.split(title)[1] != '':
            video_title = video_title.split(title)[1]
        summary = item.xpath('.//p[@class="overlay_extra overlay_spacer_top"]')[0].text
        link = THE_WB_ROOT + item.xpath('.//a')[0].get('href')
        thumb = item.xpath('.//img')[0].get('src')
        try:
            details = RE_EP_DETAILS.search(item.xpath('.//span[@class="type"]')[0].text.strip()).groupdict()
            season = int(details['season'])
            index = int(details['episode'])
        except:
            details = RE_DURATION.search(item.xpath('.//span[@class="type"]')[0].text.strip()).groupdict()
            season = None
            index = None
        
        duration = (int(details['minutes'])*60 + int(details['seconds']))*1000
        
        if season and index:
            oc.add(EpisodeObject(url=link, title=video_title, show=title, season=season, index=index, duration=duration, summary=summary, thumb=Resource.ContentsOfURLWithFallback(url=thumb, fallback=ICON)))
        else:
            oc.add(VideoClipObject(url=link, title=video_title, duration=duration, summary=summary, thumb=Resource.ContentsOfURLWithFallback(url=thumb, fallback=ICON)))

    return oc
