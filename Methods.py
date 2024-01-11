class Methods:
    def __init__(self,method, parameters, ErrorLine):
        self.methods = {
            "output": self.output,
        }
        self.method = method
        self.parameters = parameters
        self.ErrorLine = ErrorLine + 1

        for method in self.methods:
            if method == self.method:
                self.methods[method]()

    def output(self):
        print(self.parameters)
