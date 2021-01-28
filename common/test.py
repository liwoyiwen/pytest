import json
import ast
data={
"account_id":11300272,
"adcreative_template_id":998,
"adcreative_elements":"{\"image\":\"228297837\",\"description\":\"gg\"}",
"page_type":"PAGE_TYPE_CANVAS_WECHAT",
"page_spec":"{\"override_canvas_head_option\":\"OPTION_CANVAS_OVERRIDE_CREATIVE\",\"page_id\":2008725504}",
"profile_id":135264,
"promoted_object_type":"PROMOTED_OBJECT_TYPE_ECOMMERCE",
"adcreative_name":"20210125-9_0125142944",
"site_set":"[\"SITE_SET_WECHAT\"]",
"link_page_spec":"{\"page_id\":2008725504}",
"campaign_id":3002685464,
"link_page_type":"LINK_PAGE_TYPE_CANVAS_WECHAT"
}

for k in data:
    if type(data[k]) is not str:
        data[k] = json.dumps(data[k])
print(data)


json.loads(data)
print(data)
print(ast.literal_eval("{\"end_page\":{\"end_page_desc\":\"gggg\",\"end_page_type\":\"END_PAGE_AVATAR_NICKNAME_HIGHLIGHT\"},\"corporate\":{\"corporate_img\":\"125687873\",\"corporate_name\":\"222\"},\"description\":\"ggg\",\"video\":524453442}"))