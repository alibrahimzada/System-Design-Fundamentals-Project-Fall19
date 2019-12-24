class SM:
    def start(self):
        self.state = self.startState
    
    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o
    
    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs]