from spacy import displacy
import spacy
from spacy.training import Example
import random
from spacy.util import minibatch, compounding
from pathlib import Path
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
TRAIN_DATA = [
    ("成功大學是一所酷學校", {"entities": [(0, 4, "ORG")]}),
    ("我在成功大學上課", {"entities": [(2, 6, "ORG")]}),
    ("成功大學受到豪雨的攻擊", {"entities": [(0, 4, "ORG")]}),
    ("他去年成功考進了成功大學", {"entities": [(8, 12, "ORG")]}),
    ("他去年成功考進了成功大學", {"entities": [(3, 3, "EVE")]}),
    ("成功大學長久以來培育了各行各業無數的菁英領袖", {"entities": [(0, 4, "ORG")]}),
    ("成功大學特聘教授榮獲終生成就獎", {"entities": [(0, 4, "ORG")]}),
    ("成功大學副校長在去年退休", {"entities": [(0, 4, "ORG")]}),
    ("他今年考上成功大學的研究所", {"entities": [(5, 9, "ORG")]}),
    ("凡事只要努力不懈最後一定會成功。", {"entities": [(13, 15, "EVE")]}),
    ("失敗為成功之母", {"entities": [(3, 5, "EVE")]}),
    ("成功和失敗的人最大的差別只在於心態", {"entities": [(0, 2, "PER")]}),
    ("成功人士的正確個態度 ", {"entities": [(0, 4, "PER")]}),
    ("在成功大學讀書 ", {"entities": [(1, 5, "ORG")]}),
    ("科系減縮規模與裁併公立大學更興起併校的風潮", {"entities": [(11, 13, "ORG")]}),
    ("位於台南的成功大學的命名是從當年擊退荷蘭人並建立東寧王國的民族英雄鄭成功的名字而來", {"entities": [(5, 9, "ORG")]}),
    ("成功大學簡稱成大始位於台南市", {"entities": [(0, 4, "ORG")]}),
    ("成功大學醫學院攜手群創光電成立醫學影像中心。", {"entities": [(0, 4, "ORG")]}),
    ("校長主要負責學校日常營運和行政的決策", {"entities": [(0, 2, "PER")]}),
    ("成功大學共計有十一個校區", {"entities": [(0, 4, "ORG")]}),
    ("成功大學共計有十一個校區", {"entities": [(10, 12, "LOC")]}),
    ("台南火車站後站就在成功大學附近", {"entities": [(9, 13, "ORG")]}),
    ("成功大學附近有很多好吃的", {"entities": [(0, 4, "ORG")]}),
    ("校醫在寒假期間暫停服務", {"entities": [(0, 2, "PER")]}),
    ("校正是了解儀器器示值與標準值關係", {"entities": [(0, 2, "EVE")]}),
    ("限制服儀之校規有無存在之必要", {"entities": [(5, 7, "law")]}),
    ("座椅要調校到合適的高度", {"entities": [(3, 5, "EVE")]}),
    ("我們約在校門見面", {"entities": [(4, 6, "LOC")]}),
    ("國立成功大學學士部的大部分學系課程設計為4年", {"entities": [(2, 6, "ORG")]}),
    ("成功大學是他的第一志願", {"entities": [(0, 4, "ORG")]}),
    ("明天是表定的返校日", {"entities": [(6, 9, "EVE")]}),
    ("整理自己的學習表現幫助學生生涯探索", {"entities": [(5, 7, "EVE")]}),
    ("整理自己的學習表現幫助學生生涯探索", {"entities": [(11, 13, "PER")]}),
    ("我在這堂課中學到了很多", {"entities": [(6, 8, "EVE")]}),
    ("她是成功大學的教授", {"entities": [(2, 6, "ORG")]}),
]
text = \
    "110年全國大專校院運動會復辦為期5天6項賽事圓滿落幕，\
    今日下午在國立成功大學光復田徑場舉行熄聖火與交旗儀式。\
    教育部體育署副署長洪志昌、國立成功大學校長蘇慧貞，以及下一屆承\
    辦全大運國立體育大學校長邱炳坤皆出席與會。"
nlp = spacy.load('zh_core_web_lg')
doc = nlp(text)

doc = nlp(text)
for sent in doc.sents:
    print(">", sent)

for entity in doc.ents:
    print(entity, " ... ", entity.label_)

html = displacy.render(doc, style="ent")
output_path = Path("dependency_plot.html")  # 視覺化檔案儲存的檔名
output_path.open("w", encoding="utf-8").write(html)

pipe_exceptions = ["ner"]  # 指定我們只更新NER模型，其他的pipeline不去做變動
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# TRAINING THE MODEL
with nlp.disable_pipes(unaffected_pipes):
    # Training for 30 iterations
    for iteration in range(30):

        # shuufling examples  before every iteration
        random.shuffle(TRAIN_DATA)
        losses = {}
        # batch up the examples using spaCy's minibatch
        batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)

        example = []
        # Update the model with iterating each text
        for i in range(len(texts)):
            doc = nlp.make_doc(texts[i])
        example.append(Example.from_dict(doc, annotations[i]))

        # Update the model
        nlp.update(example, drop=0.5, losses=losses)
        print("Losses", losses)

doc = nlp(text)
print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
nlp.to_disk("./ncku_model")
