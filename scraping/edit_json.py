import json


with open(rf"C:\temp\gp_raj_dist_1.json", encoding="utf8") as file:
    list_ = json.load(file)


list_ = [{k: v for k, v in dict_.items() if k != "Election_duration"} for dict_ in list_]

with open("../json/data1.json", "w", encoding="utf-8") as raj_updated_GP:
    json.dump(list_, raj_updated_GP,ensure_ascii=False , indent=4)

# # Write the updated JSON data back to the file
# with open(f"C:\temp", "w") as raj_updated_GP:
#     json.dump(dict_, raj_updated_GP, indent=4)





    # for item in dict_.copy():
    #    if not dict_[item]:
    #         del_item = dict_.pop('Election_duration', None)
    #         print(del_item)
    #         print(dict_)





    # for key, value in i.items():
    #     if key=='Election_duration':
    #         # key.pop('Election_duration', None)
    #

            # del i['Election_duration']