from rest_framework.renderers import JSONRenderer

class customrenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """

        :param data:
        :param accepted_media_type:
        :param renderer_context:
        :return:
        """
        if renderer_context:
            if isinstance(data,dict):    #判断返回的数据是否是字典
                msg = data.pop("msg","请求成功")    #是字典，获取msg
                code = data.pop("code",0)           #是字典，获取code
            else:
                msg = '请求成功'
                code =0
            ret = {
                "msg":msg,
                "code":code,
                "author":"aaa",
                "data":data
            } #重构数据格式
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
