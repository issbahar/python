import psutil    
"someProgram" in (p.name() for p in psutil.process_iter())


print(p)
