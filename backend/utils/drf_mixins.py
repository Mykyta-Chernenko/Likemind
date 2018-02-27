class SerializerFieldsMixin(object):
    include_arg_name = 'include_fields'
    exclude_atg_name = 'exclude_fields'
    delimiter = ','

    def __init__(self, *args, **kwargs):
        include_field_names = kwargs.pop('include_fields',None)
        exclude_field_names = kwargs.pop('exclude_fields',None)

        super(SerializerFieldsMixin, self).__init__(*args, **kwargs)
        try:
            request = self.context['request']
            method = request.method
        except (AttributeError, TypeError, KeyError):
            # The serializer was not initialized with request context.
            return

        if method != 'GET':
            return

        include_field_names = set(include_field_names.split(self.delimiter))

        exclude_field_names = set(exclude_field_names.split(self.delimiter))

        if not include_field_names and not exclude_field_names:
            # No user fields filtering was requested, we have nothing to do here.
            return

        serializer_field_names = set(self.fields)

        fields_to_drop = serializer_field_names & exclude_field_names
        if include_field_names:
            fields_to_drop |= serializer_field_names - include_field_names

        for field in fields_to_drop:
            self.fields.pop(field)
