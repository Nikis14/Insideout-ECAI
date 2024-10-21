import os


class EmpUtteranceDataset:
    def __init__(
        self,
        splitname,
        data_folder,
    ):
        df = open(
            os.path.join(data_folder, f"{splitname}.csv"), encoding="utf-8"
        ).readlines()
        self.cols = df[0].strip().split(",")
        self.data = []
        self.ids = []
        for i in range(1, len(df)):
            sparts = df[i].strip().split(",")
            sent = sparts[5].replace("_comma_", ",")
            sparts[5] = sent
            self.data.append(sparts)
            self.ids.append((sparts[0], sparts[1]))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return dict(zip(self.cols, self.data[index]))

    def getid(self, index):
        return self.ids[index]


class EmpDialogsDataset:
    def __init__(self, splitname, data_folder, name_prefix="Speaker", cut_n_last=None):
        self.name_prefix = name_prefix
        self.cut_n_last = cut_n_last
        df = open(
            os.path.join(data_folder, f"{splitname}.csv"), encoding="utf-8"
        ).readlines()
        self.cols = df[0].strip().split(",")
        self.data = []
        self.ids = []
        current_dialog = []
        for i in range(1, len(df) - 1):
            sparts = df[i].strip().split(",")
            current_dialog.append(sparts)
            sent = sparts[5].replace("_comma_", ",")
            sparts[5] = sent
            if sparts[0] != df[i + 1].strip().split(",")[0]:
                self.data.append(current_dialog)
                current_dialog = []
                self.ids.append((sparts[0], sparts[1]))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index, postprocess=True):
        if postprocess:
            return self.postprocessing_add_names(self.data[index], self.name_prefix)
        return self.data[index]

    def getid(self, index):
        return self.ids[index]

    def postprocessing_add_names(self, dataset_output_value, name_prefix="Speaker"):
        phrases = [el[5] for el in dataset_output_value]
        names = [f"{name_prefix} 1: ", f"{name_prefix} 2: "] * (len(phrases) // 2 + 1)
        names = names[: len(phrases)]

        if len(phrases) > 1 and self.cut_n_last is not None:
            if len(phrases[: -self.cut_n_last]) % 2 == 0:
                cut_n_last = self.cut_n_last + 1
            else:
                cut_n_last = self.cut_n_last
            out = "\n".join(
                [name + phrase for name, phrase in zip(names, phrases)][:-cut_n_last]
            )
        else:
            out = "\n".join([name + phrase for name, phrase in zip(names, phrases)])
        return out
