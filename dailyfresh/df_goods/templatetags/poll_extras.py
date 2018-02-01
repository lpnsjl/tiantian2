# -*- coding: UTF-8 -*-
from django import template
import datetime
import django.template.defaulttags

# 引入标签与过滤器库，这个库里注册了所有的标签与过滤器
register = template.Library()

# 定义一个过滤器，不能抛出异常

def cut1(value,args):
    try:
        return value.replace(args[0],args[1])
    except:
        return value

def cut2(value,arg):
    return value.replace(arg,'<h1>我是html语言</h1>')

# 注册过滤器
register.filter('cut1', cut1)
register.filter('cut2', cut2)



"""
自定义模板
<p>{%current_time "%Y-%m-%d %I:%M %p"%}</p>
"""
def do_current_time(parser,token):
    try:
        tag_name,format_string=token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r 只要求一个参数'%token.contents.split()[0])
    if not (format_string[0]==format_string[-1] and format_string[0] in ('"',"'")):
        raise template.TemplateSyntaxError('%r 必须是一个整体'%tag_name)
    return CurrentTimeNode(format_string)


class CurrentTimeNode(template.Node):
    def __init__(self,format_string):
        self.format_string = format_string

    def render(self,context):
        return datetime.datetime.now().strftime(self.format_string)

register.tag('current_time',do_current_time)


############################################################################


############################################################################
def list_parse(parser,token):
    try:
        tag_name,arg,list_parse_format = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires exactly two arguements'%tag_name)
    if not(list_parse_format[0]==list_parse_format[-1] and list_parse_format[0] in ('"',"'")):
        raise template.TemplateSyntaxError('%r tags argument should be in quotes'%tag_name)

    return ListPrserFormat(arg,list_parse_format)


class ListPrserFormat(template.Node):
    def __init__(self,arg,list_parse_format):
        self.arg = arg
        self.list_parse_format = list_parse_format

    def render(self, context):
        new_arg = self.arg.split(',')
        return new_arg[0][int(new_arg[1])]

register.tag('list_parse',list_parse)
