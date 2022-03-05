import os
import math
from jinja2 import Environment, FileSystemLoader

class File:
    
    def __init__(self, file):
        self.file = file
        self.wm_command = f"gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOutputFile=wm_{self.file} wm.ps {self.file}"

    def get_info(self):
        pages_info = f"gs -q -dNODISPLAY -dQUIET -dNOSAFER -sFileName={self.file} -c \"FileName (r) file runpdfbegin 1 1 pdfpagecount {{pdfgetpage /MediaBox get {{=print ( ) print}} forall (\\n) print}} for quit\""
        exec = os.popen(pages_info)
        out = exec.read()
        return [(float(page.split(' ')[2]), float(page.split(' ')[3])) for page in out.rstrip().split('\n')]

    def resize(self):
        resize_command = f"gs -q -o r_{self.file}  -sDEVICE=pdfwrite  -sPAPERSIZE=a4  -dPDFFitPage  -dCompatibilityLevel=1.4  {self.file}"
        os.system(resize_command)

    def watermarking(self, watermarkPath='.', transparency=0.5, text="Watermark", font="Calibri"):
        file_loader = FileSystemLoader(watermarkPath) 
        env = Environment(loader=file_loader)
        template = env.get_template("watermark_template.ps")
        
        pages_info = self.get_info()

        output_command = f"gs -q -dNOPAUSE -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOUTPUTFILE=wm_{self.file} -dBATCH "        

        for index,info in enumerate(pages_info):
            if index == 0:
                wm = f"gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -dFirstPage={index+1} -dLastPage={index+1} -sOutputFile={index}_{self.file} wm.ps {self.file}"
            else:
                wm = f"gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -dFirstPage={index+1} -dLastPage={index+1} -sOutputFile={index}_{self.file} wm.ps {self.file}"


            position = f"{info[0]//7.2} {info[1]//7.2}"

            rotate = math.degrees(math.atan(info[1]/info[0]))
            size = math.sqrt(info[0]**2 + info[1]**2)//7.2
            print(info, size, rotate, position)
            watermark = template.render(transparency=transparency, text=text, rotate=rotate, size=size, font=font, position=position)

            output_command += f"{index}_{self.file} "

            with open("wm.ps",'w') as file:
                file.write(watermark)
                file.close()

            os.system(wm)
            os.remove("wm.ps")

        os.system(output_command)

        for i in range(0,len(pages_info)):
            os.remove(f"{i}_{self.file}")
