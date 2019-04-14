import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import Pattern
import os
from codecs import open

DEF_RE = r'(@\()(?P<text>.+?)\)'
    
class DefinitionPattern(Pattern):
    def handleMatch(self, matched):
        text = matched.group("text")
        
        filename = 'glossary.md' 
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
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns["definition"] = DefinitionPattern(DEF_RE, md)

# @(parachain) -> <span data-tooltip="xxxxxxxxxx">parachain</span> where xxxx = ./glossary.md#parachain