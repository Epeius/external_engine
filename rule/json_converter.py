from rule.argument_parser import ArgumentParser
class JsonConverter:
    def __int__(self):
        return

    def convert_data_to_mysql_json_object(self, data):
        if isinstance(data, dict):
            res_list = []
            for key in data.keys():
                d = data[key]
                res_list.append("'{}'".format(str(key))),
                res_list.append(self.convert_data_to_mysql_json_object(d))
            return 'JSON_OBJECT({})'.format(','.join(res_list))

        else:
            if isinstance(data, int):
                return str(data)
            elif isinstance(data, str):
                return "'{}'".format(data)
            elif isinstance(data, list):
                return 'JSON_ARRAY({})'.format(','.join([self.convert_data_to_mysql_json_object(x) for x in data]))
        return


    def is_prolog_json_string(self, arg):
        if arg.startswith("json(") and arg.endswith(")"):
            json_content= arg.lstrip("json(").rstrip(")").strip()
            if json_content.startswith("[") and json_content.strip().endswith("]"):
                return True
        return False

    def _convert_prolog_json_to_dict(self, prolog_json_string):
        if self.is_prolog_json_string(prolog_json_string):
            ret = self.convert_prolog_json_to_dict_internal(prolog_json_string)
            if isinstance(ret, str):
                return ret
            for key in ret.keys():
                value = ret[key]
                ret[key] = self._convert_prolog_json_to_dict(value)
            return ret
        else:
            if prolog_json_string.isdigit():
                return int(prolog_json_string)
            elif prolog_json_string.lower().startswith('0x'):
                return int(prolog_json_string[2:], 16)
            elif prolog_json_string.strip().startswith("[") and prolog_json_string.strip().endswith("]"):
                try:
                    return self.convert_json_list_to_list(prolog_json_string)
                except:
                    return prolog_json_string
            else:
                return prolog_json_string


    def convert_prolog_json_to_dict_internal(self, prolog_json_string):
        json_content = self.get_json_content(prolog_json_string)
        ap = ArgumentParser(json_content)
        ret = {}
        for json_content_item in ap.get_arguments():
            ap = ArgumentParser(json_content_item)
            eq_pos = json_content_item.find("=")
            if eq_pos == -1:
                return prolog_json_string
            key = json_content_item[:eq_pos].strip()
            value = json_content_item[eq_pos+1:].strip()
            ret[key] = value

        return ret

    def get_json_content(self, prolog_json_string):

        return prolog_json_string.lstrip("json(").rstrip(")").strip(" ")[1:-1]

    def convert_json_list_to_list(self, list_str):
        arg_str = list_str.strip()[1:-1]

        arg_str_len = len(arg_str)
        bracket_depth = 0
        square_bracket_depth = 0
        last_offest = 0
        args = []
        for offset in range(0, arg_str_len):
            if arg_str[offset] == '(':
                bracket_depth = bracket_depth + 1
            elif arg_str[offset] == ')':
                bracket_depth = bracket_depth - 1

            elif arg_str[offset] == '[':
                square_bracket_depth = square_bracket_depth + 1
            elif arg_str[offset] == ']':
                square_bracket_depth = square_bracket_depth - 1

            if (arg_str[
                    offset] == ',' or offset == arg_str_len - 1) and bracket_depth == 0 and square_bracket_depth == 0:
                if offset == arg_str_len - 1:

                    args.append(self.convert_item(arg_str[last_offest:].strip(',').strip()))
                else:
                    args.append(self.convert_item(arg_str[last_offest:offset].strip()))
                last_offest = offset + 1

        if bracket_depth != 0 or square_bracket_depth != 0:
            print("[*] [ArgumentParser] The bracket or square_bracket mismatch for {}".format(arg_str))
            return []
        return args

    def convert_item(self, item_string):
        if item_string.isdigit():
            return int(item_string)
        elif item_string.lower().startswith('0x'):
            return int(item_string[2:], 16)
        elif self.is_prolog_json_string(item_string):
            return self._convert_prolog_json_to_dict(item_string)
        elif item_string.strip().startswith("[") and item_string.strip().endswith("]"):
            try:
                return self.convert_json_list_to_list(item_string.strip())
            except:
                return item_string.strip().strip('"')
        else:
            return item_string.strip().strip('"')

    def convert_argument(self, arg):
        if isinstance(arg, list):
            return self.convert_data_to_mysql_json_object(arg)
        elif isinstance(arg, int):
            return arg
        elif isinstance(arg, str):
            return "'{}'".format(arg)
        elif isinstance(arg, dict):
            return self.convert_data_to_mysql_json_object(arg)
        return arg