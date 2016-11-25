import re
import os
import codecs
import jieba
import jieba.posseg
import time

def strip_tags():
	"""Basic regexp based HTML / XML tag stripper function
	For serious HTML/XML preprocessing you should rather use an external
	library such as lxml or BeautifulSoup.
	"""
	#t0 = time()
	left_a = 3
	right_b = 3
	tag_name = "张伟"
	with codecs.open('人名数据\\张伟.txt', 'r', 'utf-8')as f_corpus, codecs.open('中文停用词表.txt', 'r', 'utf-8') as f_stop:
		raw = f_corpus.read()
		f_stopwords = f_stop.read()
	#print(raw)
	raw = raw.replace("\n","")  #正则匹配无法对换行进行处理
	aw = raw.replace("\r","")  #正则匹配无法对换行进行处理
	filelist_string = [re.compile(r"<([^>]+)>", flags=re.UNICODE).sub(" ", word) 
					for word in raw.split("<doc>") if len(word)>0] 
	#print(file_string[:1])
	'''
	for index, file_string in enumerate(filelist_string):
		with codecs.open('news\\'+("%04d" % index), 'w', 'utf-8')as f:
			f.write(file_string)
	'''
	stopwords = [w for w in f_stopwords]
	#s = re.compile(r"<([^>]+)>", flags=re.UNICODE).sub(" ", file_string)
	#中文分词
	categories_list = []
	filelist_tokens = []
	file_namelist = []
	temp_tag = []
	#print(filelist_string[:2])
	for raw_file in filelist_string[:80]:
		categories_list.append(raw_file[1])	#获得类型，由于前面有个空格
		f_cutandtag = jieba.posseg.cut(raw_file)	#分词标记
		for i in f_cutandtag:
			if i.word not in stopwords:
				temp_tag.append((i.word, i.flag))
		#print(len(temp_tag))
		#print(temp_tag)	
		temp_name = list(set([w[0] for w in temp_tag if w[1] == "nr" and len(w[0])>1]))
		#print(temp_name)
		file_namelist.append(temp_name)		#找出人名
		temp_tag.clear()
	#print(file_namelist[:2])
		
	#同名聚到一个类中
	same_name = []
	for index, name in enumerate(file_namelist):
		if tag_name in name:
			same_name.append([str(index), name])	#index_list为同类文件集合
	
	print(same_name[:3])
	
	c_result= []
	c_result.append(same_name[0])
	print("##################################")
	#print(c_result)
	print("##################################")
	#print(len(same_name))
	print("##################################")
	flag = 0
	#分类：如果有相同社会关系（人名）聚为一类
	del same_name[0]
	while(len(same_name)):
		for index_j, j in enumerate(same_name):
			for index_i, i in enumerate(c_result):
				if len([x for x in j[1] if x in i[1]]) > 2:
					#print(len([x for x in j[1] if x in i[1]]))
					c_result[index_i][1].extend(same_name[index_j][1])
					c_result[index_i][1] = list(set(c_result[index_i][1]))	#关系合并
					c_result[index_i][0] +=	" "+same_name[index_j][0] #聚为同一类
					flag = 1
					break
			if flag == 0:
				c_result.append(j)
			else:
				flag = 0
			same_name.remove(j)
	#print(len(c_result))
	[print(num[0]) for num in c_result]
	
	print("##################################")
	#根据上下文分类以上的聚类结果
	same_name_file = []		#以上聚类到相同类别的文件的内容
	attr_list_afile = []	#人物社会属性
	attr_a_cate = []		#同个类别所有人物的属性列表
	attr_all_cates = []		#所有类别的人物属性表
	#f_tag = []
	for index in c_result:
		name_num = index[0].split(' ')
		#print("####")
		if len(name_num)>1:
			#print(name_num)
			#print("######")
			attr_a_cate = []
			same_name_file = []
			#读取类别全部文档
			for i in name_num:						
				with codecs.open('news\\'+("%04d" % int(i)), 'r', 'utf-8') as f:
					f_string = f.read()
					same_name_file.append((i ,f_string))
					
			#print(same_name_file)
			#取出一个类别的每个文件对应的上下文属性列
			for i, f in same_name_file:
				#f_tag = [w for w in list(jieba.cut(f)) if w not in stopwords]	#分词标记
				temp_tag=[]
				f_cutandtag = jieba.posseg.cut(f)	#分词标记
				for p in f_cutandtag:
					if p.word not in stopwords:
						temp_tag.append((p.word, p.flag))
				#print(len(temp_tag))
				#print(temp_tag)	
				f_tag = [w[0] for w in temp_tag if re.match(r'^n.*', w[1])]
				#print(temp_name)
				temp_tag.clear()
				attr_list_afile = []
				#取出一篇中上下文
				for ind ex, tokens in enumerate(f_tag):
					if tokens == tag_name:
						try:
							if (index - left_a) > 0 and (index + right_b) < len(f_tag):
								left = index - left_a
								right = index + right_b
								attr_list_afile.extend(f_tag[left : right])
							else:
								print('上下文超出范围')
						except Exception as e:  
							print("上下文超出范围")
					#print(attr_list_afile)
				attr_list_afile = list(set(attr_list_afile))
				#print(attr_list_afile)
				attr_a_cate.append((i, attr_list_afile))
				#print(attr_a_cate)
			#print(attr_a_cate)
			attr_all_cates.append(attr_a_cate)			
		
		#break
	#print("time: %0.3fs" % time() - t0)
	print(attr_all_cates)
strip_tags()