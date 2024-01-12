import os


class Methods:
    def __init__(self, method, parameters, ErrorLine):
        self.methods = {
            "Output": self.output,
            'Stop': self.stop,
            'System': self.system
        }
        self.method = method
        self.parameters = parameters
        self.ErrorLine = ErrorLine + 1

        for method in self.methods:
            if method == self.method:
                self.methods[method]()

    def system(self):
        os.system(self.parameters)

    def stop(self):
        print("Program Was Stopped By Method At Line ", self.ErrorLine)
        quit()

    def output(self):
        print(self.parameters)
