# text = "2.0.15终端综合     配线箱 integrated  terminal box"

# # 使用 split() 和 join() 清理多余空格
# cleaned_text = " ".join(text.split())
# print(text.split())
# print(cleaned_text)
# import re
# with open("../deeprag/knowledge_file/test.txt","r") as file:
#     content = file.read()
#     print(content)


# content_no_spaces = content.replace(' ', '')
# print(content_no_spaces)

import re
text = "2.0.5 贮藏室 storage room \n住宅套内用于贮藏并可以进入的空间\n\n   你们好"
print(text)
cleaned_text = text.replace("\n", "")
print(cleaned_text)
final_text = cleaned_text = re.sub(r'(?<=[\u4e00-\u9fff\d])\s+|\s+(?=[\u4e00-\u9fff\d])', '', cleaned_text)
print(final_text)