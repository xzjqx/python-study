import argparse
import re
from multiprocessing import Pool
import requests
import bs4

root_url = 'http://pyvideo.org'
index_url = root_url + '/category/50/pycon-us-2014'

def get_video_page_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text,"lxml")
    return [a.attrs.get('href') for a in soup.select('div.col-md-3 a[href^=/video]')]

def get_video_data(video_page_url):
    video_data = {}
    response = requests.get(root_url + video_page_url)
    soup = bs4.BeautifulSoup(response.text,"lxml")
    video_data['title'] = soup.select('div#videobox h3')[0].get_text()
    video_data['speakers'] = [a.get_text() for a in soup.select('div#sidebar a[href^=/speaker]')]
    video_data['youtube_url'] = soup.select('div#sidebar a[href^=http://www.youtube.com]')[0].get_text()
    response = requests.get(video_data['youtube_url'])
    soup = bs4.BeautifulSoup(response.text,"lxml")
    #video_data['views'] = int(re.sub('[^0-9]', '',
    #                                 soup.select('.watch-view-count')[0].get_text().split()[0]))
    #video_data['likes'] = int(re.sub('[^0-9]', '',
    #                                 soup.select('.likes-count')[0].get_text().split()[0]))
    #video_data['dislikes'] = int(re.sub('[^0-9]', '',
    #                                    soup.select('.dislikes-count')[0].get_text().split()[0]))
    return video_data

def parse_args():
    parser = argparse.ArgumentParser(description='Show PyCon 2014 video statistics.')
    #parser.add_argument('--sort', metavar='FIELD', choices=['views', 'likes', 'dislikes'],
    #                    default='views',
    #                    help='sort by the specified field. Options are views, likes and dislikes.')
    parser.add_argument('--max', metavar='MAX', type=int, help='show the top MAX entries only.')
    parser.add_argument('--csv', action='store_true', default=False,
                        help='output the data in CSV format.')
    parser.add_argument('--workers', type=int, default=8,
                        help='number of workers to use, 8 by default.')
    return parser.parse_args()

def show_video_stats(options):
    pool = Pool(options.workers)
    video_page_urls = get_video_page_urls()
    results = sorted(pool.map(get_video_data, video_page_urls), key=lambda video: video[options.sort],
                     reverse=True)
    max = options.max
    if max is None or max > len(results):
        max = len(results)
    if options.csv:
        print(u'"title","speakers", "views","likes","dislikes"')
    else:
        print(u'Views  +1  -1 Title (Speakers)')
    for i in range(max):
        if options.csv:
            print(u'"{0}","{1}",{2},{3},{4}'.format(
                results[i]['title'], ', '.join(results[i]['speakers']), results[i]['views'],
                results[i]['likes'], results[i]['dislikes']))
        else:
            print(u'{3} ({4})'.format(
                results[i]['title'],
                ', '.join(results[i]['speakers'])))

if __name__ == '__main__':
    show_video_stats(parse_args())