import os
import urllib.request
import urllib.request, queue, time
import threading 

class ThreadManager():
    def __init__(self, thread_num):
        self.lock = threading.Lock()
        self.to_crawl = queue.Queue()
        self.num = queue.Queue()
        self.init_queue()
        self.end_flag = False
        for i in range(thread_num):
            t = threading.Thread(target=self.working)
            t.start()
    
    def init_queue(self):
        self.url_list = []
        with open("Pictures1.txt", 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                try:
                    pic_url = line.split('\t')[2].strip()
                    self.url_list.append(pic_url)
                except:
                    print("fuccck")

        with open("Pictures2.txt", 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                try:
                    pic_url = line.split('\t')[2].strip()
                    self.url_list.append(pic_url)
                except:
                    print("FFFFFFuuuccckk")
        
        count = 1
        for pic_url in set(self.url_list):
            self.to_crawl.put(pic_url)
            self.num.put(count)
            count += 1

    def working(self):
        while not self.to_crawl.empty():
            pic_url = self.to_crawl.get()
            num = self.num.get()
            if num%100 == 0:
                print("handled to : ", num)
            try:
                id, name = pic_url.split('/')[-4], pic_url.split('/')[-1]
                file_path = "./pictures/" + id 
                if not os.path.exists(file_path):
                    os.mkdir(file_path)
                urllib.request.urlretrieve(pic_url,filename=file_path + "/" + name)
            except:
                pass
        if self.lock.acquire():
            self.end_flag = True
            self.lock.release()

t = ThreadManager(300)
while not t.end_flag:
    time.sleep(10)