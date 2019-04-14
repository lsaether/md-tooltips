import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from codecs import open

DEF_RE = r'(@\()(?P<text>.+?)\)'
    
class DefinitionPattern(Pattern):
    def handleMatch(self, matched):
        text = matched.group("text")
        
        filename = "docs/glossary.md"
        with open(filename, 'r') as r:
            lines = r.readlines()

        total = ''
        for i in range(len(lines)):
            if lines[i].lower().rstrip() == '## ' + text.lower():
                count = 1
                res = ''
                while not res.startswith('##') and i+count < len(lines):
                    res = lines[i+count]
                    if not res.isspace() and not res.startswith('##'):
                        total += res
                    count += 1

        if not total:
            return

        definition = total.rstrip()

        elem = markdown.util.etree.Element("span")
        elem.set("data-tooltip", definition)
        elem.text = markdown.util.AtomicString(text)
        return elem

class MdTooltip(Extension):
    def __init__(self, configs={}):
        # NOTE: config is not actually passed to anything
        self.config = {
            'glossary_path': ['docs/glossary.md', "Default location for glossary."]
        }

        for key, value in configs.items():
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns["definition"] = DefinitionPattern(DEF_RE, md)

def makeExtension(*args,**kwargs):
    return MdTooltip(kwargs)

# @(parachain) -> <span data-tooltip="xxxxxxxxxx">parachain</span> where xxxx = ./glossary.md#parachain