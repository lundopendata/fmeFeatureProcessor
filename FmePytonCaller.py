from unittest.mock import patch


class FmePythonCaller(object):
    def __init__(self, class_to_process_features):
        self.ctpf = class_to_process_features

    def input(self, *features, **groupByAttr):
        if type(features[0]) is list:
            features = features[0]
        else:
            features = list(features)

        group_by = None

        def group_by_str(f, g):
            ret = ""
            for a in g:
                ret += "|☕|" + f.getAttribute(a, fallback="")
            return ret

        if 'groupBy' in groupByAttr:
            group_by = groupByAttr.get('groupBy')
            if not type(group_by) is list:
                raise Exception("groupBy must be a list")
            features.sort(key=lambda x: (group_by_str(x, group_by)))

        out = []

        def patch_pyoutput(_self, _feature):
            out.append(_feature)

        with patch.object(self.ctpf, 'pyoutput', new=patch_pyoutput):
            fp = self.ctpf()
            if group_by is None:
                for feature in features:
                    fp.input(feature)
            else:
                last_gb = ""
                for idx, feature in enumerate(features):
                    fp.input(feature)
                    this_gb = group_by_str(feature, group_by)
                    if idx != 0 and last_gb != this_gb:
                        fp.process_group()
                    last_gb = this_gb

            fp.process_group()
            fp.close()
        return out
