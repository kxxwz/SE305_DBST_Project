import urllib.request, queue, time
import threading 

class ThreadManager():
    def __init__(self, thread_num):
        self.lock = threading.Lock()
        self.to_crawl = queue.Queue()
        self.max_count_num = 59000
        self.end_flag = False
        for i in range(self.max_count_num):
            self.to_crawl.put(i)
        for i in range(thread_num):
            t = threading.Thread(target=self.working)
            t.start()

    def working(self):
        while not self.to_crawl.empty():
            num = self.to_crawl.get()
            if num%100 == 0:
                print("handled to : ", num)
            url = "https://www.gutenberg.org/ebooks/" + str(num)
            try:
                resp=urllib.request.urlopen(url)
                html=resp.read()
                with open('raw_html/'+ str(num) + ".html", 'wb') as f:
                    f.write(html)
            except:
                pass
        if self.lock.acquire():
            self.end_flag = True
            self.lock.release()

t = ThreadManager(100)
while not t.end_flag:
    time.sleep(10)











 
