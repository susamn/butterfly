import json


def __get_attrib_value(val):
    elements = val.split("[].")
    return elements[0], elements[1]


def __domapping(key, full_key, val, mapdata, inside_list=False):
    if type(val) == str:
        if inside_list:
            if full_key not in mapdata:
                mapdata[full_key] = {}
            target, attrib_value = __get_attrib_value(val)
            mapdata[full_key][key] = attrib_value
            mapdata[full_key]["_target"] = target
        else:
            mapdata[full_key] = val
        return
    if type(val) == list:
        for item in val:
            __domapping(key, full_key, item, mapdata, inside_list=True)
    if type(val) == dict:
        for key, val in val.items():
            if not inside_list:
                __domapping(key, "%s.%s" % (full_key, key), val, mapdata)
            else:
                __domapping(key, full_key, val, mapdata, inside_list=True)


def __project(data, key):
    for item in str.split(key, "."):
        if item not in data:
            return
        else:
            data = data[item]
    return data


def __propagate(data, key, value, result):
    data = __project(data, key)

    if data:
        key_elements = str.split(value, ".")
        for i, datakey in enumerate(key_elements):
            if datakey not in result:
                if i == len(key_elements) - 1:
                    result[datakey] = data
                else:
                    result[datakey] = {}
            result = result[datakey]


def __facilitate(key, result):
    if key:
        key_elements = str.split(key, ".")
        for i, item in enumerate(key_elements):
            if item not in result:
                if i == len(key_elements) - 1:
                    result[item] = []
                else:
                    result[item] = {}
                result = result[item]

        return result


def lookup(data, key, value, result):
    if type(value) == dict and len(value) > 0:
        target_key = value["_target"]
        target_node = __facilitate(target_key, result)
        projecteddata = __project(data, key)
        del value["_target"]

        if type(projecteddata) != list:
            print("Please map the fields, properly, expecting list, got something else")
            return

        for item in projecteddata:
            fillto = {}
            fillup_struct(item, value, fillto)
            target_node.append(fillto)
    else:
        __propagate(data, key, value, result)


def fillup_struct(data, mapping, fillto):
    for k, v in mapping.items():
        fillto[v] = data[k]


def transform(data_file, mapping_file):
    with open(data_file) as fd:
        data = json.load(fd)
    with open(mapping_file) as fm:
        mapping = json.load(fm)
    mappeddata = {}
    for key, val in mapping.items():
        __domapping(key, key, val, mappeddata)

    result = {}
    for key, value in mappeddata.items():
        lookup(data, key, value, result)

    return result
