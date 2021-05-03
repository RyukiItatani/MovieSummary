from django.shortcuts import render
from .form import UserForm
from django.views.generic import TemplateView
from youtube_transcript_api import YouTubeTranscriptApi
import json
import requests
import time

class IndexView(TemplateView):
    def __init__(self):
        self.params = {
            'form':UserForm(),
            'caption':'',
            'summary':'',
            'error':''
        }
    def get(self,request):
        return render(request,'polls/index.html',self.params)
    def post(self,request):
        def TakeVideoId(url):
            pos = url.find('=') + 1
            VideoId = url[pos:]
            return VideoId

        def GetCaption(VideoId):
            caption = ''
            transcript_list = YouTubeTranscriptApi.get_transcript(VideoId,languages=['ja'])
            for transcript in transcript_list:
                caption += transcript['text'] + '。'
            return caption
        def GetSummary(text):
            key = '************************************'
            endpoint = "https://clapi.asahi.com/extract"
            length = 200
            rate = 0.3
            auto_paragraph = True
            input_json = json.dumps({"text":text,"rate":rate,"auto_paragraph":auto_paragraph})
            headers = {"accept":"application/json",
                    "Content-Type":"application/json",
                    "x-api-key":key}
            response = requests.post(endpoint, input_json, headers=headers)
            time.sleep(5)#負荷軽減
            if response.status_code == 200:
                result = response.json()["result"]
                summary = ''
                for i in result:
                    summary += i
                return summary
        try:
            url = request.POST.get('url')
            VideoId = TakeVideoId(url)
            caption = GetCaption(VideoId)
            summary = GetSummary(caption)
            self.params['caption'] = caption
            self.params['summary'] = summary
            self.params['form'] = UserForm(request.POST)
            return render(request,'polls/index.html',self.params)
        except:
            self.params['error'] = '字幕のあるYoutubeのURLを正しく入力してください'
            return render(request,'polls/index.html',self.params)
Index = IndexView.as_view()

