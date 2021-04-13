# -*- coding: utf-8 -*-

"""
@Version: V1.0.0
@File: pattern
@Description: 
@CreateTime: 2021/3/27
"""
import re


class Pattern(object):
    Pattern_Orig = 0
    Pattern_Short = 1
    Pattern_Long = 2
    Pattern_Paragraph = 3
    Pattern_Page = 4
    Pattern_Single = 5
    Pattern_Short_Neighour = 6

    Short_Split = 'short'
    Long_Split = 'long'
    Paragraph_Split = 'section'
    Page_Split = 'all'
    Concept_Sign = '【'
    Concept_Sign_End = '】'
    Select_Sign = '|'
    Neighnour_Sign = '_@'
    Combine_Sign = 'combine'

    def __init__(self):
        self.parts = None
        self.targets = None
        self.type = Pattern.Pattern_Orig

    def merge(self, other):
        if not other.targets: return
        if self.targets is None: self.targets = []
        for t in other.targets:
            if t not in self.targets:
                self.targets.append(t)
        return True

    @staticmethod
    def is_combine(p):
        return p.endswith(Pattern.Combine_Sign)

    @staticmethod
    def remove_combine_sign(p):
        if not Pattern.is_combine(p): return p
        return p[0:-len(Pattern.Combine_Sign)]

    @staticmethod
    def add_neighnour_sign(c):
        if str(c).find(Pattern.Neighnour_Sign) < 0:
            c = str(c)
            c = c[0:-1] + Pattern.Neighnour_Sign + c[-1:]
        return c

    @staticmethod
    def remove_neighnour_sign(c):
        return c.replace(Pattern.Neighnour_Sign, '')

    @staticmethod
    def is_neighnour_concept(c):
        return str(c).find(Pattern.Neighnour_Sign) > 0

    @staticmethod
    def is_concept(w):
        if not w or len(w) < 2: return False
        if w[0] == Pattern.Concept_Sign and w[-1] == Pattern.Concept_Sign_End:
            if w[1:-1].find(Pattern.Concept_Sign) < 0:
                # print('PatternUtil.isConcept',w)
                return True
        return False

    @staticmethod
    def split(p):
        lastI = 0
        ps = []
        for i in range(len(p)):
            if p[i] == Pattern.Concept_Sign:
                if i > lastI:
                    ps.append(p[lastI:i])
                    lastI = i
            elif p[i] == Pattern.Concept_Sign_End:
                ps.append(p[lastI:i + 1])
                lastI = i + 1
        if len(p) > lastI:
            ps.append(p[lastI:])
        return ps

    def set_parts(self, parts):
        if len(parts[-1]) == 0:
            del parts[-1]
        self.parts = parts

    @staticmethod
    def parse_neg_word(seged_negword, pattern_type, Neg_Word_Sign='【负面词】'):
        ret = []
        pt = Pattern()
        pt.parts = []
        pt.type = pattern_type
        pt.targets = [Neg_Word_Sign]
        for w in seged_negword:
            pt.parts.append(w)
            pt2 = Pattern()
            pt2.parts = w
            pt2.targets = [w]
            pt2.type = Pattern.Pattern_Orig
            ret.append(pt2)
        ret.append(pt)
        return ret

    @staticmethod
    def parse(line):
        ret = []
        ss = re.split(r'[\t ]+', line)
        if len(ss) < 2: return ret
        part = ss[0]
        ps = part.split(Pattern.Select_Sign)
        ts = ss[1].split(Pattern.Select_Sign)
        for p in ps:
            is_combine = Pattern.is_combine(p)
            if is_combine:
                p = Pattern.remove_combine_sign(p)
            pt = Pattern()
            pt.targets = ts
            pis = None
            if p.find(Pattern.Short_Split) > 0:
                pt.type = Pattern.Pattern_Short
                pis = p.split(Pattern.Short_Split)
                pt.set_parts(pis)
            elif p.find(Pattern.Long_Split) > 0:
                pt.type = Pattern.Pattern_Long
                pis = p.split(Pattern.Long_Split)
                pt.set_parts(pis)
            elif p.find(Pattern.Paragraph_Split) > 0:
                pt.type = Pattern.Pattern_Paragraph
                pis = p.split(Pattern.Paragraph_Split)
                pt.set_parts(pis)
            elif p.find(Pattern.Page_Split) > 0:
                pt.type = Pattern.Pattern_Page
                pis = p.split(Pattern.Page_Split)
                pt.set_parts(pis)
            else:
                if p.find(Pattern.Concept_Sign) >= 0:
                    cs = Pattern.split(p)
                    if len(cs) == 1:
                        pt.type = Pattern.Pattern_Single
                        pt.parts = cs
                    else:
                        pt.type = Pattern.Pattern_Short_Neighour
                        pt.parts = cs
                        pis = cs
                else:
                    pt.type = Pattern.Pattern_Orig
                    pt.parts = p
            if is_combine and pis:
                new_pis = []
                for pi in range(len(pis) - 1, -1, -1):
                    new_pis.append(pis[pi])
                pt1 = Pattern()
                pt1.type = pt.type
                pt1.parts = new_pis
                pt1.targets = ts
                # print('reverse pt1',pt1)
                ret.append(pt1)
            ret.append(pt)
            if pt.type != Pattern.Pattern_Orig:
                for p1 in pt.parts:
                    if not Pattern.is_concept(p1):
                        pt2 = Pattern()
                        pt2.parts = p1
                        pt2.targets = [p1]
                        pt2.type = Pattern.Pattern_Orig
                        ret.append(pt2)
        return ret

    def __str__(self):
        return str(self.parts) + "=>" + str(self.targets)
