import markdown
from mdtooltips import MdTooltip

txt = "@(parachain) test @(lol)"
res = markdown.markdown(txt, extensions=[MdTooltip()])
print(res)