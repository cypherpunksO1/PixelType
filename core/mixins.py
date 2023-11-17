class SerializerMixin:
    def to_dict(self, include: list | str = '__all__', exclude: list = []):
        class_variables_dict = {}

        if exclude:
            for variable in vars(self):
                if not variable.startswith("_") and variable not in exclude:
                    try:
                        class_variables_dict[variable] = vars(self)[variable]
                    except KeyError:
                        ...

        else:
            variables = include if include != '__all__' else vars(self)
            for variable in variables:
                try:
                    class_variables_dict[variable] = vars(self)[variable]
                except KeyError:
                    ...

        return class_variables_dict
