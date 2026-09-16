"""Build original SVG profile artwork. Pillow is needed for the avatar mosaic.
Run from the repository root: python scripts/build_assets.py
The animated signal strip is decorative, not contribution data.
"""
from pathlib import Path
from html import escape
from PIL import Image
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
BG, PANEL, LINE = '#0b1019', '#131c2a', '#29374c'
WHITE, MUTED, GOLD, CYAN = '#f0f5fc', '#a6b6ca', '#f1c77a', '#65e6cb'

def text(x,y,s,size=16,color=WHITE,weight='400',extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(s)}</text>'

def svg(w,h,title,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<style>text{{font-family:Arial,Helvetica,sans-serif}} .mono{{font-family:monospace}} @media(prefers-reduced-motion:reduce){{.motion{{display:none}}}}</style>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{BG}" stroke="{LINE}"/>{body}</svg>'''

def window(w,title):
    return f'<path d="M1 42H{w-1}" stroke="{LINE}"/>'+''.join(f'<circle cx="{23+i*19}" cy="22" r="5" fill="{c}"/>' for i,c in enumerate(['#ee797a',GOLD,CYAN]))+text(w-22,27,title,12,MUTED,extra='text-anchor="end" class="mono"')

def save(name,w,h,title,body):
    (OUT/name).write_text(svg(w,h,title,body))

body=text(28,37,'FRANCIS GYAMFI OSEI TUTU',25,WHITE,'700')+text(28,67,'SOFTWARE ENGINEERING  /  APPLIED AI  /  CREATIVE THINKING',12,GOLD,extra='letter-spacing="2"')
body+=f'<circle cx="850" cy="34" r="5" fill="{CYAN}"/>'+text(865,39,'OPEN TO INTERNSHIPS',13,CYAN,'700')
save('header.svg',1080,90,'Francis Gyamfi Osei Tutu. Open to software engineering internships.',body)

avatar=ROOT/'avatar.png'
if not avatar.exists(): urllib.request.urlretrieve('https://avatars.githubusercontent.com/u/171380191?v=4',avatar)
im=Image.open(avatar).convert('RGB').resize((36,36))
body=window(420,'francis / portrait')
for y in range(36):
    for x in range(36):
        r,g,b=im.getpixel((x,y))
        lum=(r*.2126+g*.7152+b*.0722)/255
        color=GOLD if r>g*1.25 and r>b*1.25 else CYAN
        body+=f'<rect x="{102+x*6}" y="{61+y*6}" width="5" height="5" rx="1" fill="{color}" opacity="{.12+.88*lum:.2f}"/>'
body+=f'<rect class="motion" x="99" y="61" width="220" height="2" fill="{CYAN}" opacity=".55"><animate attributeName="y" values="61;275;61" dur="8s" repeatCount="indefinite"/></rect>'
body+=text(26,318,'$ whoami',16,CYAN,extra='class="mono"')+text(26,346,'FrancisGyamfi',21,WHITE,'700')
body+=f'<rect class="motion" x="181" y="331" width="9" height="18" fill="{GOLD}"><animate attributeName="opacity" values="1;0;1" dur="1.6s" repeatCount="indefinite"/></rect>'
save('portrait-terminal.svg',420,380,'Animated pixel portrait of Francis, with terminal prompt.',body)

body=window(640,'profile.json')+text(28,79,'francis@github:~$ cat profile',17,CYAN,extra='class="mono"')
rows=[('name','Francis Gyamfi Osei Tutu'),('education','Grambling State University'),('studies','Computer Science + Information Systems'),('focus','Full-stack development + applied AI'),('experience','Break Through Tech AI / Team Anote'),('creative','Film + live production'),('seeking','Software engineering internships')]
for i,(label,value) in enumerate(rows):
    y=119+i*31
    body+=text(28,y,label,14,GOLD,extra='class="mono"')+text(146,y,value,16,CYAN if label=='seeking' else WHITE)
body+=''.join(f'<rect x="{28+i*29}" y="350" width="23" height="8" rx="2" fill="{c}"/>' for i,c in enumerate([GOLD,CYAN,'#729ced','#ae94e8','#ee797a',WHITE]))
save('profile-terminal.svg',640,380,'Profile details: Grambling State, software engineering, applied AI, and creative work.',body)

body=text(27,31,'FROM AN IDEA TO SOMETHING PEOPLE CAN USE',12,MUTED,extra='letter-spacing="2"')
for i,(label,col) in enumerate([('THINK',GOLD),('BUILD',CYAN),('REFINE','#ae94e8'),('SHARE','#729ced')]):
    x=28+i*263
    body+=text(x,68,label,19,col,'700')
    for k in range(12):
        body+=f'<rect x="{x+k*17}" y="85" width="12" height="8" rx="2" fill="{col}" opacity=".3"/>'
body+=f'<rect class="motion" x="28" y="85" width="12" height="8" rx="2" fill="{WHITE}"><animate attributeName="x" values="28;1004;28" dur="12s" repeatCount="indefinite"/></rect>'
save('creative-signal.svg',1080,117,'Decorative animation: Think, build, refine, share. Not contribution statistics.',body)

cards=[('project-ai.svg','01 / COLLABORATIVE AI','Autonomous Intelligence',['Team Anote project through Break Through Tech AI.','Explore orchestration, agents, tools, and workflows.'],'PYTHON  /  MULTI-AGENT SYSTEMS',CYAN),('project-access.svg','02 / ACCESSIBILITY','Infinity Ability Connect',['Flutter prototype exploring accessible communication.','Speech input, sign imagery, and learning screens.'],'FLUTTER  /  DART',GOLD),('project-ml.svg','03 / MACHINE LEARNING','Airbnb ML Lab',['Coursework exploring logistic regression','and model selection with Airbnb data.'],'PYTHON  /  JUPYTER','#ae94e8'),('project-classync.svg','04 / PRODUCT STORYTELLING','ClassSync',['Team-built classroom attendance app.','My role: Video Production Lead.'],'PRODUCT COMMUNICATION  /  VIDEO','#729ced')]
for name,label,title,lines,stack,color in cards:
    body=f'<rect x="25" y="27" width="4" height="27" rx="2" fill="{color}"/>'+text(42,44,label,12,color,'700',extra='letter-spacing="1"')+text(26,90,title,26,WHITE,'700')
    for i,line in enumerate(lines): body+=text(26,125+i*25,line,15,MUTED)
    body+=text(26,199,stack,12,color,'700')+text(478,201,'↗',25,color)
    save(name,530,230,title,body)

tags=['Python','Java','JavaScript','Node.js','Express','MongoDB','Flutter','Dart','Git','Figma']
body=''
for i,tag in enumerate(tags):
    x=18+i*106
    body+=f'<rect x="{x}" y="18" width="94" height="44" rx="9" fill="{PANEL}" stroke="{LINE}"/>'+text(x+47,46,tag,14,WHITE,'700',extra='text-anchor="middle"')
save('toolkit.svg',1080,80,'Python, Java, JavaScript, Node.js, Express, MongoDB, Flutter, Dart, Git, Figma.',body)
print('Built 9 SVG assets.')
