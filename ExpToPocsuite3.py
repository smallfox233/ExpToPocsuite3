# 作者：小狐狸FM
# 版本：v0.1
# 功能：将goby的exp转换为pocsuite3

import os
import json
import argparse

class Goby():
    '''
    将goby exp转换为pocsuite3脚本\n\n
    '''
    def __init__(self,temp_pth='Template/pocsuite3_template',goby_pth="Template/goby.json",poc_folder="pocsuite"):
        '''
        :param temp_pth:模板路径
        :param goby_pth:goby脚本路径
        :param poc_pth:pocsuite3导出路径
        '''
        # 路径
        self.temp_pth = temp_pth
        self.goby_pth = goby_pth
        self.poc_folder = poc_folder
        # 变量
        self.goby = ""
        self.temp = self.__read_temp()
        self.dic = self.__read_goby()
        # 替换
        self.__replace_options()
        self.__replace_verify()
        self.__replace_basic()
        self.__replace_origin()
        # 导出
        self.export()
    def export(self):
        '''将最终的pocsuite脚本导出'''
        # 创建文件夹
        if os.path.exists(self.poc_folder) == False: #不存在该文件夹时
            os.mkdir(self.poc_folder)
        # 文件名过滤
        name_txt = self.dic["Name"].replace("/","").replace("\\","").replace(":","").replace("*","").replace("?","").replace('"',"").replace("<","").replace(">","").replace("|","")
        # 创建脚本
        f1 = open(self.poc_folder + "/" + name_txt + ".py","w",encoding='utf-8')
        f1.write(self.temp)
        f1.close()
    def __read_temp(self):
        '''读取模板文件内容，转换为字符串'''
        f2 = open(self.temp_pth,"r",encoding='utf-8')
        tmp = f2.read()
        f2.close()
        return tmp
    def __read_goby(self):
        '''读取goby脚本文件中的json，转换为字典类型'''
        f3 = open(self.goby_pth,"r",encoding='utf-8')
        self.goby = f3.read()
        txt = self.goby.replace("\n","")
        try:
            tmp = json.loads(txt)
        except:
            print(self.goby_pth)
            print(self.goby)
            print(txt)
        f3.close()
        return tmp
    def __replace_origin(self):
        '''替换pocsuite模板末尾的{$origin$}参数将原goby的poc内容写入'''
        self.temp = self.temp.replace("{$origin$}", "原goby的POC如下：\n" + self.goby)
    def __replace_html(self,tmp):
        '''
        替换字符串中的HTML标签
        :param tmp: 需要替换标签的字符串
        :return:
        '''
        tmp_txt = ""
        tmp_txt = tmp
        tmp_txt = tmp_txt.replace("<p>","").replace("</p>","") #替换p标签
        tmp_txt = tmp_txt.replace("<br>","").replace("</br>","\n") #替换br标签
        return tmp_txt
    def __replace_options(self):
        '''替换pocsuite模板中的_options方法内容'''
        pass
    def __replace_verify(self):
        '''替换pocsuite模板中的_verify方法内容'''
        # 临时变量
        header_txt = ""
        type_txt = "get"
        payload_txt = ""
        url_path_txt = ""
        # 请求头Cache-Control参数
        try: #存在该参数时
            header_txt += "Cache-Control':'" + self.dic["ScanSteps"][1]["Request"]["header"]["Cache-Control"] + "','"
        except:
            pass
        # 请求头Pragma参数
        try: #存在该参数时
            header_txt += "Pragma':'" + self.dic["ScanSteps"][1]["Request"]["header"]["Pragma"] + "','"
        except:
            pass
        # 请求头Accept-Encoding参数
        try: #存在该参数时
            header_txt += "Accept-Encoding':'" + self.dic["ScanSteps"][1]["Request"]["header"]["Accept-Encoding"] + "','"
        except:
            pass
        # 请求头Accept参数
        try: #存在该参数时
            header_txt += "Accept':'" + self.dic["ScanSteps"][1]["Request"]["header"]["Accept"] + "','"
        except:
            pass
        # 请求头Connection参数
        try: #存在该参数时
            header_txt += "Connection':'" + self.dic["ScanSteps"][1]["Request"]["header"]["Connection"] + "','"
        except:
            pass
        # 请求头Cookie参数
        try: #存在该参数时
            header_txt += "Cookie':'" + self.dic["ScanSteps"][1]["Request"]["header"]["Cookie"] + "','"
        except:
            pass
        # 请求头Charsert参数
        try: #存在该参数时
            header_txt += "Charsert':'" + self.dic["ScanSteps"][1]["Request"]["header"]["Charsert"] + "','"
        except:
            pass
        # 请求头Content-Type参数（必须是请求头字典的最后一个键值对）
        try: #存在该参数时
            header_txt += "Content-Type': '" + self.dic["ScanSteps"][1]["Request"]["header"]["Content-Type"].replace("'",'"')
        except: #不存在该参数时
            try:
                if self.dic["ScanSteps"][1]["Request"]["method"].upper() == "POST": #类型为post
                    header_txt = "Content-Type': 'application/x-www-form-urlencoded"
                else:
                    header_txt = ""
            except:
                header_txt = ""
        # 请求类型
        try: #存在该参数时
            if self.dic["ScanSteps"][1]["Request"]["method"].upper() == "POST": #类型为post时
                type_txt = "post"
        except:
            pass
        # 请求body
        try:  # 存在该参数时
            if self.dic["ScanSteps"][1]["Request"]["method"].upper() == "POST":  # 类型为post时
                payload_txt = self.dic["ScanSteps"][1]["Request"]["data"].replace("\n","\\n").replace("\r","\\r")
        except:
            pass
        # 请求路径
        try:
            url_path_txt = self.dic["ScanSteps"][1]["Request"]["uri"]
        except:
            url_path_txt = "/"
        # 替换
        self.temp = self.temp.replace("{$type$}", type_txt)
        self.temp = self.temp.replace("{$headers$}", header_txt)
        self.temp = self.temp.replace("{$payload$}",payload_txt)
        self.temp = self.temp.replace("{$url_path_verify$}", url_path_txt)

    def __replace_attack(self):
        '''替换pocsuite模板中的_attack方法内容'''
        pass
    def __replace_basic(self):
        '''替换pocsuite模板的基础信息'''
        # cve编号
        try:
            self.temp = self.temp.replace("{$vulID$}", self.dic["CVEIDs"][0])
        except:
            self.temp = self.temp.replace("{$vulID$}", "")
        # 脚本版本
        self.temp = self.temp.replace("{$version$}", "")
        # 作者名称
        try:
            self.temp = self.temp.replace("{$author$}", self.dic["Author"])
        except:
            self.temp = self.temp.replace("{$author$}", "")
        # 漏洞发现时间
        try:
            self.temp = self.temp.replace("{$vulDate$}", self.dic["DisclosureDate"])
        except:
            self.temp = self.temp.replace("{$vulDate$}", "")
        # 参考链接
        try:
            if len(self.dic["References"]) <= 1:
                self.temp = self.temp.replace("{$references$}", self.dic["References"][0])
            else:  # 含有多个参考链接时
                tmp_txt = ""
                for i in range(len(self.dic["References"])):
                    # 首个参考链接
                    if i ==0:
                        tmp_txt += self.dic["References"][i] + "',"
                    # 最后一个参考链接
                    elif i==len(self.dic["References"])-1:
                        tmp_txt += "'" + self.dic["References"][i]
                    else:
                        tmp_txt += "'" + self.dic["References"][i] + "',"
                self.temp = self.temp.replace("{$references$}", tmp_txt)
        except:
            self.temp = self.temp.replace("{$references$}", "")
        # 漏洞名称
        try:
            self.temp = self.temp.replace("{$name$}",self.dic["Name"])
        except:
            self.temp = self.temp.replace("{$name$}", "")
        # 产品官网链接
        try:
            self.temp = self.temp.replace("{$appPowerLink$}", self.dic["Homepage"])
        except:
            self.temp = self.temp.replace("{$appPowerLink$}", "")
        # 产品名称
        try:
            self.temp = self.temp.replace("{$appName$}", self.dic["Product"])
        except:
            self.temp = self.temp.replace("{$appName$}", "")
        # 产品版本
        self.temp = self.temp.replace("{$version$}", "")
        # 漏洞描述
        try:
            self.temp = self.temp.replace("{$desc$}", self.__replace_html(self.dic["Description"]))
        except:
            self.temp = self.temp.replace("{$desc$}", "")
        # 脚本使用描述
        try:
            self.temp = self.temp.replace("{$pocDesc$}", self.__replace_html(self.dic["Impact"]))
        except:
            self.temp = self.temp.replace("{$pocDesc$}", "")

def ExportAll(origin_type="goby",origin_folder='goby',export_folder='pocsuite'):
    '''
    批量导出指定文件夹下的脚本（不支持其子文件夹的脚本转换，目前仅支持goby）
    :param origin_type: 脚本类型
    :param origin_folder: 脚本存储路径
    :param export_folder: 脚本导出路径
    :return:
    '''
    # 各个脚本的路径
    goby_lis = []
    # 筛选.json后缀
    for i in os.listdir(origin_folder):
        if i.split(".")[-1]=="json" and origin_type=="goby":
            goby_lis.append(i)

    # 附加文件夹路径
    for i in range(len(goby_lis)):
        goby_lis[i] = origin_folder + "/" +goby_lis[i]
        if os.path.exists(goby_lis[i]):
            Goby(goby_pth=goby_lis[i],poc_folder=export_folder)
        else:
            print("文件"+goby_lis[i]+"不存在!")

if __name__ == '__main__':
    # 输入
    arg = argparse.ArgumentParser(description="")
    arg.add_argument('-g','--goby',help="goby脚本所在目录")
    arg.add_argument('-p','--poc',help="pocsuite脚本保存的目录")
    args = arg.parse_args() #参数解析
    # 初始化值
    pth = ""
    new_pth = "new"
    # 赋值
    pth = args.goby
    new_pth = args.poc
    # 批量导出
    try:
        ExportAll("goby",pth,new_pth)
        print("导出结束!")
    except:
        print("导出过程出错!可能的错误原因如下：\n")
        print("1. 未使用-g参数设置goby脚本所在目录")
        print("1. 未使用-p参数设置pocsuite脚本保存的目录")
