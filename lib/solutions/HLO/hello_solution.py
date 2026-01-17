class HelloSolution:
    # friend_name = unicode string
    def hello(self, friend_name):
        return "hello " + friend_name


if __name__ == "__main__":
    hs = HelloSolution
    returnStr = hs.hello(hs, "me")
    print(returnStr)

