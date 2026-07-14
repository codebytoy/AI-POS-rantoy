import win32print

print("Default =", win32print.GetDefaultPrinter())

for p in win32print.EnumPrinters(2):
    print(p[2])