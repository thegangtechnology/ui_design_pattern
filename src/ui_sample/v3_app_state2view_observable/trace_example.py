import tkinter as ti

def a(*arg):
    print('a')

def b(*arg):
    print('b')

def main():
    v = ti.StringVar()
    # this is typically called observable
    # Internally, it holds a list of callbacks for whence the action is triggered
    print(v.get(), 'before')
    v.trace_add('write', a) # if write call a
    v.trace_add('write', b) # if write call b
    v.set('hello') # write this triggers a and b
    print(v.get(), 'after')

if __name__ == '__main__':
    root = ti.Tk() # you need tk to use StringVar
    main()
