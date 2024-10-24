import re
import json
from eval.extracter.extracter import Extracter


class NERExtracter(Extracter):
    def __init__(self, language="zh", NAN="NAN", prefix = "输入中包含的实体是：\n", Reject="No entity found."):
        super().__init__(language, NAN, prefix, Reject)

    def post_process(self, result):  
        try:      
            rst = json.loads(result)
        except json.decoder.JSONDecodeError:
            print("json decode error", result)  # 如果Json格式错误在这里就会输出，并返回False和[]
            return False, []
        if type(rst) != dict:
            print("type(rst) != dict", result)
            return False, []
        new_record = []
        for key, values in rst.items(): # 'Group', ['Republican', 'Democratic']
            if type(key) != str or type(values) != list:
                print("type(key) != str or type(values) != list", result)
                continue
            for iit in values:
                if type(iit) != str:
                    print("type(iit) != str", result)
                    continue
                new_record.append((iit, key))   #[('Republican', 'Group'), ('Democratic', 'Group')]
        return True, new_record

