import wx
import mysql.connector

class ExamplePanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent,size=(1000, 600))
		self.mydb = mysql.connector.connect(
			host="192.168.1.115",
			user="hesson",
			passwd="hesson",
			database='ebook',
			port=3306)
		self.cursor = self.mydb.cursor()
		self.pic_list = []
		self.first_time1 = True
		self.first_time2 = True
		self.pic_index1 = 0
		self.pic_index2 = 0
		self.name = wx.StaticText(self, label="Book name :", pos=(20, 30))
		self.editname = wx.TextCtrl(self, pos=(150, 30), size=(140,-1))
		self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)

		# the edit control - one line version.
		self.author = wx.StaticText(self, label="Book author :", pos=(20,60))
		self.editauthor = wx.TextCtrl(self, pos=(150, 60), size=(140,-1))
		self.Bind(wx.EVT_TEXT, self.EvtText, self.editauthor)
		
		self.chapter = wx.StaticText(self, label="Book chapter :", pos=(20,90))
		self.editchapter = wx.TextCtrl(self, pos=(150, 90), size=(140,-1))
		self.Bind(wx.EVT_TEXT, self.EvtText, self.editchapter)

		self.words = wx.StaticText(self, label="Book words :", pos=(20,120))
		self.editwords = wx.TextCtrl(self, pos=(150, 120), size=(140,-1))
		self.Bind(wx.EVT_TEXT, self.EvtText, self.editwords)
		
		
		# A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
		self.logger = wx.TextCtrl(self, pos=(320,20), size=(300,-1))
		
		self.clear_pics()
		

		# A button
		self.func1 = wx.StaticText(self, label="Find book by name, author:", pos=(20,180))
		self.button1 =wx.Button(self, label="Find", pos=(200, 175))
		self.Bind(wx.EVT_BUTTON, self.OnClick1, self.button1)
		
		self.func2 = wx.StaticText(self, label="Find pics by name, chapter:", pos=(20,220))
		self.button2 =wx.Button(self, label="Find", pos=(200, 215))
		self.Bind(wx.EVT_BUTTON, self.OnClick2, self.button2)

		self.func3 = wx.StaticText(self, label="Find pics by words:", pos=(20,260))
		self.button3 =wx.Button(self, label="Find", pos=(200, 255))
		self.Bind(wx.EVT_BUTTON, self.OnClick3, self.button3)

	##  Find book by name, author
	def OnClick1(self,event):
		name = self.editname.GetValue()
		author = self.editauthor.GetValue()
		book = self.Find_book(name, author)
		self.logger.Clear()
		self.logger.AppendText(book)

	##  Find pics by name, chapter
	def OnClick2(self,event):
		self.pic_index2 = 0
		name = self.editname.GetValue()
		chapter = self.editchapter.GetValue()
		if self.first_time1: 
			self.pic_list = self.Find_pic_by_name_chapter(name,chapter)
			self.first_time1 = False
			self.first_time2 = True
		if len(self.pic_list) == 0:
			new_image = wx.Image('default.png', wx.BITMAP_TYPE_ANY).Rescale(140, 100).ConvertToBitmap()
			self.bmp1.SetBitmap(new_image)
			self.bmp2.SetBitmap(new_image)
			self.bmp3.SetBitmap(new_image)
			return
		if self.pic_index1 >= len(self.pic_list): return 
		for i in range(3):
			if self.pic_index1 < len(self.pic_list):
				new_image = wx.Image(self.pic_list[self.pic_index1], wx.BITMAP_TYPE_ANY).Rescale(140, 100).ConvertToBitmap()
				self.pic_index1 += 1
			else:
				new_image = wx.Image('default.png', wx.BITMAP_TYPE_ANY).Rescale(140, 100).ConvertToBitmap()
			if i%3 == 0:
				self.bmp1.SetBitmap(new_image)
			if i%3 == 1:
				self.bmp2.SetBitmap(new_image)
			if i%3 == 2:
				self.bmp3.SetBitmap(new_image)
		

	##  Find pics by words, name
	def OnClick3(self,event):
		self.pic_index1 = 0
		name = self.editname.GetValue()
		words = self.editwords.GetValue()
		if self.first_time2:
			self.pic_list = self.Find_pic_by_words(name, words)
			self.first_time2 = False
			self.first_time1 = True
		if len(self.pic_list) == 0:
			new_image = wx.Image('default.png', wx.BITMAP_TYPE_ANY).Rescale(140, 100).ConvertToBitmap()
			self.bmp1.SetBitmap(new_image)
			self.bmp2.SetBitmap(new_image)
			self.bmp3.SetBitmap(new_image)
			return
		if self.pic_index2 >= len(self.pic_list): return 
		for i in range(3):
			if self.pic_index2 < len(self.pic_list):
				new_image = wx.Image(self.pic_list[self.pic_index2], wx.BITMAP_TYPE_ANY).Rescale(140, 100).ConvertToBitmap()
				self.pic_index2 += 1
			else:
				new_image = wx.Image('default.png', wx.BITMAP_TYPE_ANY).Rescale(140, 100).ConvertToBitmap()
			if i%3 == 0:
				self.bmp1.SetBitmap(new_image)
			if i%3 == 1:
				self.bmp2.SetBitmap(new_image)
			if i%3 == 2:
				self.bmp3.SetBitmap(new_image)
				
	def EvtText(self, event):
		self.pic_list = []
		self.pic_index1 = 0
		self.pic_index2 = 0
		self.first_time1 = True
		self.first_time2 = True
	
	def clear_pics(self):
		image = wx.Image('default.png', wx.BITMAP_TYPE_ANY).Rescale(140, 100).ConvertToBitmap()
		self.bmp1 = wx.StaticBitmap(self, pos=(400, 75), bitmap=image)
		self.bmp2 = wx.StaticBitmap(self, pos=(400, 180), bitmap=image)
		self.bmp3 = wx.StaticBitmap(self, pos=(400, 285), bitmap=image)
		
	def Find_book(self, name, author):
		name = name.lower().strip()
		author = author.lower().strip()
		query = "SELECT book_id FROM book_id_name WHERE book_name='%s'"%(name)
		self.cursor.execute(query)
		book_id = self.cursor.fetchall()[0][0]
		query = "SELECT book_url FROM books WHERE book_id='%s' AND author='%s'"%(book_id, author)
		self.cursor.execute(query)
		book_url = self.cursor.fetchall()[0][0]
		return book_url
		
	def Find_pic_by_name_chapter(self, name, chapter):
		name = name.lower().strip()
		query = "SELECT book_id FROM book_id_name WHERE book_name='%s'"%(name)
		self.cursor.execute(query)
		book_id = self.cursor.fetchall()[0][0]
		query = "SELECT picture_url FROM picture_book WHERE book_id='%s' AND chapter_num='%s'"%(book_id, chapter)
		self.cursor.execute(query)
		pic_urls = self.cursor.fetchall()
		result = []
		for pic_url in pic_urls:
			pic_url = pic_url[0]
			id, name = pic_url.split('/')[-4], pic_url.split('/')[-1]
			result.append("../database/pictures/" + id + "/" + name)
		return result

	def Find_pic_by_words(self, name, word):
		name = name.lower().strip()
		word = word.lower().strip()
		query = "SELECT book_id FROM book_id_name WHERE book_name='%s'"%(name)
		self.cursor.execute(query)
		book_id = self.cursor.fetchall()[0][0]
		query = """
		SELECT picture_url FROM (picture_word INNER JOIN picture_book using (picture_url))
		WHERE book_id = '%s' AND word = '%s'
 		""" % (book_id, word)
		self.cursor.execute(query)
		pic_urls = self.cursor.fetchall()
		result = []
		for pic_url in pic_urls:
			pic_url = pic_url[0]
			id, name = pic_url.split('/')[-4], pic_url.split('/')[-1]
			result.append("../database/pictures/" + id + "/" + name)
		return result



app = wx.App(False)
frame = wx.Frame(None, title="Search for book & pictures")
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()
