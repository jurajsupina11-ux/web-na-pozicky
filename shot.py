from PIL import Image
import subprocess,time
E=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
for n,u in (("s1","mockup-v10-synthwave/assets/hero-art.svg"),("s2","mockup-v10-pixel/pub-investori.html")):
    p=r"C:\Users\juraj\%s.png"%n
    pr=subprocess.Popen([E,"--headless","--disable-gpu","--hide-scrollbars","--window-size=1100,800","--virtual-time-budget=8000","--screenshot="+p,"http://127.0.0.1:8765/"+u])
    time.sleep(15); pr.kill(); subprocess.run(["taskkill","/F","/IM","msedge.exe"],capture_output=True)
    im=Image.open(p).convert("RGB"); im.resize((800,int(im.height*800/im.width))).save(r"C:\Users\juraj\%sv.png"%n,optimize=True)
