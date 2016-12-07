#### 下面是三次修改中的主要修改部分(主要适用于Python3)
- unicode
```
在Python3中, 没有预定义unicode类型了,内置字符串就是str, 但是str中的字符都是unicode编码的 
Python2不必修改
Python3修改116行中的unicode改成str
```

---------------------------------------

以下是fork自wsqy/DjangoUeditor的部分的readme
============

本仓库fork自[zhangfisher](https://github.com/zhangfisher)的[DjangoUeditor](https://github.com/zhangfisher/DjangoUeditor)   

原仓库基于Django1.6和Python2,然而现在最新的django版本是1.10,两个版本差异还是较大的，所以自行fork了一份加以修改使其兼容了最新的django1.10和至于python环境经过测试兼容了Python2.7.12和python3.5.2   

#### 下面是改造过程中的主要修改部分
- long
```
python3中取消了long型，以int取代Python2中的int和long

此问题集中在 views.py和utils.py中
```

- 捕获异常
```
python2中捕获异常有两种
1. except ValueError, e
2. except ValueError as e
而python3中只保留了第二种写法

此问题集中在 views.py中
```
- 字典判断是否存在键
```
python2中 字典有has_key方法来判断字典中是否存在键,python3版本中取消了此方法，一般在python3中用 in not in来判断
此问题集中在 views.py, forms.py widgets.py中(widgets.py中的 recalc_path方法 出现的较多)

作者还采用了大量的 get(, None)来作判断
此问题集中在 views.py中
```

- utils转换数字格式的时候忘记 “111111”这种情况了
```
if oSize.isdigit():
    size_Byte = int(oSize)
```

- Fatal Python error: Cannot recover from stack overflow.
```
主要是因为@property装饰器 装饰的方法问题,
在给size赋值时改成 调用 FileSize方法
    # 返回字节为单位的值
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, newsize):
        self._size = FileSize(newsize)
```

- basejoin和urlopen方法变动
```
File "/root/Desktop/viking666/testEditor/DjangoUeditor/views.py", line 209, in UploadFile
    'url': urllib.basejoin(USettings.gSettings.MEDIA_URL, OutputPathFormat)
    
原因是：
python2中是urllib.basejoin python3中修改为urllib.request.urljoin
python2中是urllib.urlopen python3中修改为urllib.request.urlopen

此问题集中在commands.py 和views.py中
```


- 开发服务器中静态资源访问的问题：
```
在生产数据库里可以使用大型web服务器(如nginx,apache)代理静态资源,但是在开发过程中一般使用
django自带的web服务器，这是一个微型的服务器，没有静态资源访问等一系列功能，所以还是需要在
项目目录下的urls.py文件里设置好路由
在settings.py里配置：
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static").replace('\\','/')

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "upload").replace('\\','/')

STATIC_ROOT  和 MEDIA_ROOT 代表静态文件和上传文件的根路径（不能一致）
STATIC_URL 和 MEDIA_URL 对应上面的url地址  即  "/media/"能对应于os.path.join(BASE_DIR, "upload").replace('\\','/')

在项目的urls.py里的设置
在处理静态文件和上传文件的时候，正式环境可以用nginx做代理但是开发运行一般都是用自带的web服务器，这时候就要设置路由来访问到静态文件了
from . import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```
ok到此为止django-ueditor已经能够兼容1.10+python3.5了


## 以下是原作者的readme

### 由于近期均没有使用django的计划，所以DjangoUeditor停止更新，欢迎fork自行更改。

本模块帮助在Django应用中集成百度Ueditor HTML编辑器,Django是Python世界最有影响力的web框架。
Ueditor HTML编辑器是百度开源的在线HTML编辑器,功能非常强大，像表格可以直接拖动调整单元格大小等。

更新历史
============
##### [2015-1-17]     Ver:1.9.143

* Fix:当models.py中toolbars变量使用unicode字符时，编辑器无法加载的问题


##### [2014-7-8]     Ver:1.8.143

* Fix:当admin使用inlines生成多实例时widget命名不正确的问题

##### [2014-6-27]     Ver:1.7.143

* Fix:解决在admin管理后台的使用问题。
* 增加year,month,day的上传路径变量

#####[2014-6-25]

由于Ueditor从1.4版本开始，API发生了非常大的改动和不兼容，导致DjangoUeditor上一个版本的升级后上传功能不能用等，因此
本次重新设计了API，后端上传的代码几乎完全重写了。

* 更新到1.5.143，即版本号为1.5，使用了Ueditor 1.4.3版本。
* 重新设计了UeditorWidget、UeditorField。
* 新增了自定义Ueditor按钮的功能
* 注意：本次升级与之前版本不兼容，但是在使用体验上差别不大。

##### [2014-6-16]
* 更新到Ueditor 1.4.3

##### [2014-5-15]
* 增加不过滤 script,style ,不自动转div为p的脚本
* 修复在django 1.6和python2.7下的警告
* 使用 json 代替 django 中的 simplejson
* 用content_type 代替原来的 mime_type

##### [2014-5-7]
* 更新到Ueditor 1.3.6
* BUGfix:更新UEditor文件夹名字，避免在linux出现找不到静态文件问题
* 添加一种样式，besttome, 希望大家喜欢

##### [2013-2-22]
* 更新到Ueditor 1.2.5
* BUGfix:更新UEditor文件夹名字，避免在linux出现找不到静态文件问题
* BUGfix:现在支持south更新了
* 针对csrf导致上传图片失败的问题，现在默认上传视图开启了csrf_exempt装饰

---------------------------------------

使用方法
============
#### 1、安装方法

	* 方法一：将github整个源码包下载回家，在命令行运行：
		python setup.py install
	* 方法二：使用pip工具在命令行运行(推荐)：
	    pip install DjangoUeditor

#### 2、在Django中安装DjangoUeditor
     在INSTALL_APPS里面增加DjangoUeditor app，如下：
		INSTALLED_APPS = (
			#........
    		'DjangoUeditor',
		)
##### 3、配置urls
	url(r'^ueditor/',include('DjangoUeditor.urls' )),

#### 4、在models中的使用

	from DjangoUeditor.models import UEditorField
	class Blog(models.Model):
    	Name=models.CharField(,max_length=100,blank=True)
    	Content=UEditorField(u'内容	',width=600, height=300, toolbars="full", imagePath="", filePath="", upload_settings={"imageMaxSize":1204000},
                 settings={},command=None,event_handler=myEventHander(),blank=True)

*说明*

 UEditorField继承自models.TextField,因此你可以直接将model里面定义的models.TextField直接改成UEditorField即可。
定义UEditorField时除了可以直接传入models.TextFieldUEditorField提供的参数外，还可以传入UEditorField提供的额外的参数
来控制UEditorField的外观、上传路径等。
UEditorField的参数如下：

* *width，height* :编辑器的宽度和高度，以像素为单位。
* *toolbars* :配置你想显示的工具栏，取值为mini,normal,full，代表小，一般，全部。如果默认的工具栏的按钮数量不符合您的要求，您可以在settings里面配置自己的显示按钮。参见后面介绍。
* *imagePath* :图片上传后保存的路径,如"images/",实现上传到"{{MEDIA_ROOT}}/images"文件夹。
    注意：如果imagePath值只设置文件夹，则未尾要有"/"
    imagePath可以按python字符串格式化：如"images/%(basename)s_%(datetime)s.%(extname)s"。这样如果上传test.png，则文件会
    被保存为"{{MEDIA_ROOT}}/images/test_20140625122399.png"。
    imagePath中可以使用的变量有：
    * time :上传时的时间，datetime.datetime.now().strftime("%H%M%S")
    * date ：上传时的日期，datetime.datetime.now().strftime("%Y%m%d")
    * datetime ：上传时的时间和日期，datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    * year : 年
    * month : 月
    * day : 日
    * rnd : 三位随机数，random.randrange(100,999)
    * basename ： 上传的文件名称，不包括扩展名
    * extname : 上传的文件扩展名
    * filename : 上传的文件名全称
* *filePath* : 附件上传后保存的路径，设置规则与imagePath一样。
* *upload_settings* : 字典值,
 例:upload_settings={
        imagePathFormat:"images/%(basename)s_%(datetime)s.%(extname)s",
        imageMaxSize:323232
        fileManagerListPath:"files"
   }
     *  upload_settings的内容就是ueditor/php/config.json里面的配置内容，因此，你可以去看config.json或者官方文档内容来决定
            该如何配置upload_settings,基本上就是用来配置上传的路径、允许上传的文件扩展名、最大上传的文件大小之类的。
     *  上面的imagePath和filePath被单独提取出来配置，原因是因为这两个参数是最常使用到的，imagePath就相当于upload_settings里面的
                imagePathFormat，filePath就相当于upload_settings里面的filePathFormat。
     *  您upload_settings里面设置了imagePathFormat,也可以在UeditorField里面设置imagePath，效果是一样的。但是如果两者均设置，
   则imagePath优先级更高。
     *   涂鸦文件、截图、远程抓图、图片库的xxxxPathFormat如果没有配置，默认等于imagePath.
     *   远程文件库的xxxxPathFormat如果没有配置，默认等于filePath.


* *settings* : 字典值,配置项与ueditor/ueditor.config.js里面的配置项一致。
* *command* :  可以为Ueditor新增一个按钮、下拉框、对话框,例：

        Description = UEditorField(u'描述', blank=True, toolbars="full", imagePath="cool/", settings={"a": 1},
                               command=[myBtn(uiName="mybtn1", icon="d.png", title=u"1摸我", ajax_url="/ajaxcmd/"),
                                       myCombo(uiName="myCombo3",title=u"ccc",initValue="aaa")
                                        ])


以上代码可以会Ueditor增加一个按钮和一个下拉框。command是一个UEditorCommand的实例列表。如果你要在Ueditor的工具栏上增加一个
自定义按钮，方法如下：

        from DjangoUeditor.commands import UEditorButtonCommand,UEditorComboCommand
        #定义自己的按钮命令类
        class myBtn(UEditorButtonCommand):
            def onClick(self):
                return u"""
                    alert("爽!");       //这里可以写自己的js代码
                    editor.execCommand(uiName);
                """
            def onExecuteAjaxCommand(self,state):
            """  默认在command代码里面加入一段ajax代码，如果指定了ajax_url和重载本方法，则在单点按钮后
             会调用ajax_url.本方法重载是可选的。
             """
                if state=="success":
                    return u"""
                        alert("后面比较爽!"+xhr.responseText);//这里可以写ajax成功调用的js代码
                    """
                if state=="error":
                    return u"""
                        alert("讨厌，摸哪里去了！"+xhr.responseText);//这里可以写ajax错误调用的js代码
                    """

        UEditorButtonCommand有初始化参数:
                uiName:按钮名称
                title:按钮提示信息
                index:按钮显示的位置索引
                ajax_url：单击时调用的ajax url

        UEditorComboCommand可以在Ueditor上增加一个下拉框
        UEditorDialogCommand可以在Ueditor上增加一个对话框，一般与UEditorButtonCommand配合使用。暂未实现

* *event_handler* : 用来为Ueditor实例绑定事件侦听，比较当选择区改变时将按钮状态置为禁止。

        from DjangoUeditor.commands import UEditorEventHandler
        class myEventHander(UEditorEventHandler):
            def on_selectionchange(self):
                return """
                    function getButton(btnName){
                        var items=%(editor)s.ui.toolbars[0].items;
                        for(item in items){
                            if(items[item].name==btnName){
                                return items[item];
                            }
                        }
                    }
                    var btn=getButton("mybtn1");
                    var selRanage=id_Description.selection.getRange()
                    btn.setDisabled(selRanage.startOffset == selRanage.endOffset);

                """

        我们可以继承UEditorEventHandler创建自己的事件侦听类，例如上面myEventHander，然后在myEventHander中
        增加on_eventname的方法，在里面返回侦听该event的js代码。例如上例on_selectionchange,就会在前端js中
        生成id_Description.addListener('selectionchange', function () {.......});
        如果要侦听contentchange事件，就在myEventHander中增加一个on_contentchange方法，然后在该方法中返回js代码。


##5、在表单中使用非常简单，与常规的form字段没什么差别，如下：
	class TestUeditorModelForm(forms.ModelForm):
    	class Meta:
        	model=Blog
	***********************************
	如果不是用ModelForm，可以有两种方法使用：

	1: 使用forms.UEditorField

	from  DjangoUeditor.forms import UEditorField
	class TestUEditorForm(forms.Form):
	    Description=UEditorField("描述",initial="abc",width=600,height=800)

	2: widgets.UEditorWidget

	from  DjangoUeditor.widgets import UEditorWidget
	class TestUEditorForm(forms.Form):
		Content=forms.CharField(label="内容",widget=UEditorWidget(width=800,height=500, imagePath='aa', filePath='bb',toolbars={}))

	widgets.UEditorWidget和forms.UEditorField的输入参数与上述models.UEditorField一样。

    说明 关于第一种方法，需要在代码中建立相应的类（比如就在views.py中），并且需要在views.py渲染视图的时候返回到模板（template）中，对于上面的代码，具体使用可能如下（在views.py中）：

    from DjangoUeditor.forms import UEditorField class TestUEditorForm(forms.Form):
        Description=UEditorField("描述",initial="abc",width=600,height=800)

    def edit_description_view(request):
        form = TestUEditorForm()
        return render(request,'edit-description.htm',{"form": form})

    而在edit-description.htm这个模板（template）里面，只需要在模板相应位置输出form即可：
    <div class="edit-area">
        {{ form }}
    </div>

##6、Settings配置
      在Django的Settings可以配置以下参数：
            UEDITOR_SETTINGS={
                "config":{
                   #这里放ueditor.config.js里面的配置项.......
                },
                "upload":{
                   #这里放php/config.json里面的配置项.......
                }
            }
##7、在模板里面：
    <head>
        ......
        {{ form.media }}        #这一句会将所需要的CSS和JS加进来。
        ......
    </head>
    注：运行collectstatic命令，将所依赖的css,js之类的文件复制到{{STATIC_ROOT}}文件夹里面。

##8、高级运用：
     ****************
     动态指定imagePathFormat等文件路径
     ****************
     这几个路径文件用于保存上传的图片或附件，您可以直接指定路径，如：
          UEditorField('内容',imagePath="uploadimg/")
     则图片会被上传到"{{MEDIA_ROOT}}/uploadimg"文件夹，也可以指定为一个函数，如：

      def getImagePath(model_instance=None):
          return "abc/"
      UEditorField('内容',imagePath=getImagePath)
      则图片会被上传到"{{MEDIA_ROOT}}/abc"文件夹。
     ****************
     使上传路径(如imagePathFormat)与Model实例字段值相关
     ****************
        在有些情况下，我们可能想让上传的文件路径是由当前Model实例字值组名而成，比如：
        class Blog(Models.Model):
            Name=models.CharField('姓名',max_length=100,blank=True)
            Description=UEditorField('描述',blank=True,imagePath=getUploadPath,toolbars="full")

     id  |   Name    |       Description
     ------------------------------------
     1   |   Tom     |       ...........
     2   |   Jack    |       ...........

      我们想让第一条记录上传的图片或附件上传到"{{MEDIA_ROOT}}/Tom"文件夹,第2条记录则上传到"{{MEDIA_ROOT}}/Jack"文件夹。
      该怎么做呢，很简单。
      def getUploadPath(model_instance=None):
          return "%s/" % model_instance.Name
      在Model里面这样定义：
      Description=UEditorField('描述',blank=True,imagePath=getUploadPath,toolbars="full")
      这上面model_instance就是当前model的实例对象。
      还需要这样定义表单对象：
      from  DjangoUeditor.forms import UEditorModelForm
      class UEditorTestModelForm(UEditorModelForm):
            class Meta:
                model=Blog
      特别注意：
         **表单对象必须是继承自UEditorModelForm，否则您会发现model_instance总会是None。
         **同时在Admin管理界面中，此特性无效，model_instance总会是None。
         **在新建表单中，model_instance由于还没有保存到数据库，所以如果访问model_instance.pk可能是空的。因为您需要在getUploadPath处理这种情况


##9、其他事项：

    **本程序版本号采用a.b.ccc,其中a.b是本程序的号，ccc是ueditor的版本号，如1.2.122，1.2是DjangoUeditor的版本号，122指Ueditor 1.2.2.
    **本程序安装包里面已经包括了Ueditor，不需要再额外安装。
    **目前暂时不支持ueditor的插件
    **别忘记了运行collectstatic命令，该命令可以将ueditor的所有文件复制到{{STATIC_ROOT}}文件夹里面
    **Django默认开启了CSRF中间件，因此如果你的表单没有加入{% csrf_token %}，那么当您上传文件和图片时会失败
