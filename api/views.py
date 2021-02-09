from django.shortcuts import render
from .models import keywords, urls_data

# Create your views here.
def frequency(request):
    return render(request, "frequency.html")

def result(request):
    import urllib3
    from bs4 import BeautifulSoup
    import re

    url = request.POST["text"]
    status = "not"
    try:
        urlData = urls_data.objects.get(url=url)
        keywordData = keywords.objects.all().filter(urlId=urlData)
        output = keywordData
        status = "yes"
    except:    
        http = urllib3.PoolManager()
        html = http.request('GET', url)
        soup = BeautifulSoup(html.data, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()

        data = re.sub('\W+',' ', soup.text )
        data = data.split(" ")
        data = list(filter(None, data))
        commonWord = ['is', 'a', 'about', 'all', 'also', 'and', 'as', 'at', 'be', 'because', 'but', 'by', 'can', 'come', 'could', 'day', 'do', 'even', 'find', 'first', 'for', 'from', 'get', 'give', 'go', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'I', 'if', 'in', 'into', 'it', 'its', 'just', 'know', 'like', 'look', 'make', 'man', 'many', 'me', 'more', 'my', 'new', 'no', 'not', 'now', 'of', 'on', 'one', 'only', 'or', 'other', 'our', 'out', 'people', 'say', 'see', 'she', 'so', 'some', 'take', 'tell', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'thing', 'think', 'this', 'those', 'time', 'to', 'two', 'up', 'use', 'very', 'want', 'way', 'we', 'well', 'what', 'when', 'which', 'who', 'will', 'with', 'would', 'year', 'you', 'your']
        data = [x for x in data if x not in commonWord]
        output = {}
        for d in data:
            if d in output.keys():
                output[d] = output[d] + 1
            else:
                output[d] = 1
        output = dict(sorted(output.items(), key=lambda item: item[1], reverse=True))
        output = list(output.items())[:10]
        urlData = urls_data(url=url)
        urlData.save()
        for out, put in output:
            print(out, put)
            keywordData = keywords(urlId=urlData, keyword=out, frequency=put)
            keywordData.save()
    return render(request, "result.html", context={"output": output, "status": status})

    