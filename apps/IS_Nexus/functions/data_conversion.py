from django.core import serializers
import json 


def queryset_to_json(queryset):
    try:
        serialized_data = serializers.serialize('json', queryset)
        json_data_list = json.loads(serialized_data)
        return [item['fields'] for item in json_data_list]

    except Exception as e:
        return list(queryset)


def queryset_to_dict(queryset):
    result_list = []
    for instance in queryset:
        instance_dict = {}
        for field in instance._meta.fields:
            field_name = field.name
            field_value = getattr(instance, field_name)
            instance_dict[field_name] = field_value
        result_list.append(instance_dict)
    return result_list



