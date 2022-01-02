import scrapy
import os
import requests

class FetcherSpider(scrapy.Spider):
    name = 'fetcher'

    def start_requests(self):
        url = "http://app.artistsachinschoolofarts.com/studentCourse/159"

        # Set the headers here.
        headers =  {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        cookies = {
            #Add Cookies here
        }
        yield scrapy.http.Request(url,cookies=cookies, headers=headers)

    def parse(self, response):
        for vid in response.xpath('//div[contains(@class, "mb-4")]'):
            global section_head, file_location
            temp_head = vid.xpath('.//h3/text()').get()
            if temp_head is not None:
                section_head = temp_head
                file_location = f"Course/{section_head}"
                os.mkdir(file_location)
                print(section_head)
            video_title = vid.xpath('.//p/b/text()').get()
            if video_title is not None:
                filename = f"{file_location}/{video_title}.mp4"
                video_src = vid.xpath('.//source/@src').get()
                print(f"Downloading {video_title}: {video_src}")
                video = requests.get(video_src, stream=True)
                with open(filename, "wb+") as f:
                    f.write(video.content)
        pass
